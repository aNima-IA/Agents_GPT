require('dotenv').config();
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const express = require('express');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 3000;
const WS_PATH = process.env.WS_PATH || '/ws';
const ICE_SERVERS = process.env.ICE_SERVERS ? JSON.parse(process.env.ICE_SERVERS) : [
  { urls: 'stun:stun.l.google.com:19302' }
];

const app = express();
app.use(express.static(path.join(__dirname, 'src/public')));

// Expose config to clients
app.get('/config', (req, res) => {
  res.json({ wsPath: WS_PATH, iceServers: ICE_SERVERS });
});

function log(roomId, msg) {
  const time = new Date().toISOString();
  console.log(`[${time}]${roomId ? ' [room:' + roomId + ']' : ''} ${msg}`);
}

let server;
if (process.env.USE_HTTPS === 'true') {
  const options = {
    key: fs.readFileSync(process.env.TLS_KEY),
    cert: fs.readFileSync(process.env.TLS_CERT)
  };
  server = https.createServer(options, app);
} else {
  server = http.createServer(app);
}

const wss = new WebSocketServer({ server, path: WS_PATH });
const rooms = new Map(); // roomId -> { senders:Set, receivers:Set }

function getRoom(id) {
  if (!rooms.has(id)) {
    rooms.set(id, { senders: new Set(), receivers: new Set() });
  }
  return rooms.get(id);
}

function cleanupRoom(id) {
  const room = rooms.get(id);
  if (room && room.senders.size === 0 && room.receivers.size === 0) {
    rooms.delete(id);
    log(id, 'room deleted');
  }
}

wss.on('connection', (ws) => {
  ws.isAlive = true;
  ws.on('pong', () => (ws.isAlive = true));
  ws.lastMessage = 0;

  ws.on('message', (data) => {
    const now = Date.now();
    if (now - ws.lastMessage < 20) {
      log(ws.roomId, 'rate limit exceeded');
      return;
    }
    ws.lastMessage = now;

    let msg;
    try {
      msg = JSON.parse(data);
    } catch (e) {
      return;
    }

    const { type, roomId } = msg;
    if (!type || !roomId) return;
    if (String(roomId).length > 64) {
      ws.send(JSON.stringify({ type: 'error', message: 'roomId too long' }));
      return;
    }
    const room = getRoom(roomId);

    switch (type) {
      case 'join':
        ws.role = msg.role;
        ws.roomId = roomId;
        if (ws.role === 'sender') room.senders.add(ws);
        else room.receivers.add(ws);
        log(roomId, `${ws.role} joined`);
        break;
      case 'offer':
        room.receivers.forEach((r) => r.send(JSON.stringify(msg)));
        log(roomId, 'offer forwarded');
        break;
      case 'answer':
        room.senders.forEach((s) => s.send(JSON.stringify(msg)));
        log(roomId, 'answer forwarded');
        break;
      case 'ice':
        if (msg.from === 'sender') {
          room.receivers.forEach((r) => r.send(JSON.stringify(msg)));
        } else {
          room.senders.forEach((s) => s.send(JSON.stringify(msg)));
        }
        break;
      default:
        ws.send(JSON.stringify({ type: 'error', message: 'unknown type' }));
    }
  });

  ws.on('close', () => {
    const { roomId, role } = ws;
    if (roomId && rooms.has(roomId)) {
      const room = rooms.get(roomId);
      if (role === 'sender') room.senders.delete(ws);
      if (role === 'receiver') room.receivers.delete(ws);
      cleanupRoom(roomId);
      log(roomId, `${role} disconnected`);
    }
  });
});

setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

server.listen(PORT, () => {
  log(null, `Server listening on port ${PORT}`);
  log(null, `WebSocket path ${WS_PATH}`);
});
