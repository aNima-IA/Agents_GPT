import { generateQR } from './qrcode.js';

let pc, ws, localStream;
let config = { wsPath: '/ws', iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };

async function loadConfig() {
  try {
    const res = await fetch('/config');
    config = await res.json();
  } catch (e) {
    console.error('config load failed', e);
  }
}

function send(msg) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(msg));
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadConfig();
  const roomInput = document.getElementById('roomId');
  const startBtn = document.getElementById('startBtn');
  const shareBtn = document.getElementById('shareBtn');
  const status = document.getElementById('status');
  const video = document.getElementById('localVideo');
  const camSelect = document.getElementById('cameraSelect');
  const qrCanvas = document.getElementById('qrCanvas');

  video.setAttribute('playsinline', '');
  video.muted = true;

  startBtn.addEventListener('click', async () => {
    const roomId = roomInput.value.trim();
    if (!roomId) {
      alert('roomId requerido');
      return;
    }
    status.textContent = 'Solicitando cámara...';
    await initMedia();
    status.textContent = 'Conectando...';
    await initConnection(roomId);
  });

  shareBtn.addEventListener('click', () => {
    const roomId = roomInput.value.trim();
    if (!roomId) {
      alert('roomId requerido');
      return;
    }
    const url = `${location.origin}/receiver.html#roomId=${encodeURIComponent(roomId)}`;
    generateQR(qrCanvas, url);
    if (navigator.share) {
      navigator.share({ url }).catch(() => {});
    }
  });

  camSelect.addEventListener('change', async () => {
    if (!pc) return;
    const deviceId = camSelect.value;
    const newStream = await navigator.mediaDevices.getUserMedia({
      video: { deviceId: { exact: deviceId }, width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false
    });
    const newTrack = newStream.getVideoTracks()[0];
    const sender = pc.getSenders().find((s) => s.track && s.track.kind === 'video');
    sender.replaceTrack(newTrack);
    localStream.getTracks().forEach((t) => t.stop());
    localStream = newStream;
    video.srcObject = localStream;
  });
});

async function initMedia() {
  const constraints = {
    video: {
      facingMode: 'user',
      width: { ideal: 1280 },
      height: { ideal: 720 }
    },
    audio: false
  };
  localStream = await navigator.mediaDevices.getUserMedia(constraints);
  const video = document.getElementById('localVideo');
  video.srcObject = localStream;
  await video.play();
  await listCameras();
}

async function listCameras() {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const select = document.getElementById('cameraSelect');
  select.innerHTML = '';
  devices
    .filter((d) => d.kind === 'videoinput')
    .forEach((d) => {
      const opt = document.createElement('option');
      opt.value = d.deviceId;
      opt.text = d.label || `Camara ${select.length + 1}`;
      select.appendChild(opt);
    });
}

async function initConnection(roomId) {
  const { wsPath, iceServers } = config;
  pc = new RTCPeerConnection({ iceServers });
  localStream.getTracks().forEach((track) => pc.addTrack(track, localStream));

  pc.onicecandidate = (e) => {
    if (e.candidate) send({ type: 'ice', candidate: e.candidate, roomId, from: 'sender' });
  };

  ws = new WebSocket(`${location.origin.replace('http', 'ws')}${wsPath}`);

  ws.onopen = async () => {
    send({ type: 'join', roomId, role: 'sender' });
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    send({ type: 'offer', sdp: offer, roomId });
  };

  ws.onmessage = async (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'answer') {
      await pc.setRemoteDescription(msg.sdp);
      document.getElementById('status').textContent = 'Conectado';
    } else if (msg.type === 'ice') {
      await pc.addIceCandidate(msg.candidate);
    } else if (msg.type === 'error') {
      console.error(msg.message);
    }
  };

  ws.onclose = () => {
    document.getElementById('status').textContent = 'WS cerrado';
  };
}

