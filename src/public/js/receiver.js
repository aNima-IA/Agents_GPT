let pc, ws;
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
  const connectBtn = document.getElementById('connectBtn');
  const status = document.getElementById('status');
  const video = document.getElementById('remoteVideo');

  const hash = location.hash.match(/roomId=([^&]+)/);
  if (hash) roomInput.value = decodeURIComponent(hash[1]);

  connectBtn.addEventListener('click', () => {
    const roomId = roomInput.value.trim();
    if (!roomId) {
      alert('roomId requerido');
      return;
    }
    connect(roomId, video, status);
  });
});

async function connect(roomId, video, status) {
  const { wsPath, iceServers } = config;
  pc = new RTCPeerConnection({ iceServers });

  pc.onicecandidate = (e) => {
    if (e.candidate) send({ type: 'ice', candidate: e.candidate, roomId, from: 'receiver' });
  };

  pc.ontrack = (e) => {
    video.srcObject = e.streams[0];
  };
  video.setAttribute('playsinline', '');

  ws = new WebSocket(`${location.origin.replace('http', 'ws')}${wsPath}`);
  ws.onopen = () => {
    send({ type: 'join', roomId, role: 'receiver' });
    status.textContent = 'Esperando oferta...';
  };
  ws.onmessage = async (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'offer') {
      await pc.setRemoteDescription(msg.sdp);
      const answer = await pc.createAnswer();
      await pc.setLocalDescription(answer);
      send({ type: 'answer', sdp: answer, roomId });
      status.textContent = 'Conectado';
    } else if (msg.type === 'ice') {
      await pc.addIceCandidate(msg.candidate);
    } else if (msg.type === 'error') {
      console.error(msg.message);
    }
  };
  ws.onclose = () => {
    status.textContent = 'WS cerrado';
  };
}

