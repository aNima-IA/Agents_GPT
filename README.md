# iPhone Webcam via WebRTC

Proyecto de ejemplo que usa un iPhone como webcam mediante WebRTC. Incluye:

- Servidor Node.js con Express y WebSocket para señalización.
- PWA mínima como emisor (móvil) y página de receptor (desktop).
- Soporta múltiples salas (`roomId`).

## Requisitos

- Node.js 18+
- iPhone con iOS 13+ (Safari)

## Configuración

1. Copia `.env.example` a `.env` y ajusta según tus necesidades.

```bash
cp .env.example .env
```

Variables relevantes:

- `PORT`: puerto del servidor HTTP/WS.
- `WS_PATH`: path del WebSocket de señalización.
- `ICE_SERVERS`: lista JSON de servidores STUN/TURN.
- `USE_HTTPS`, `TLS_KEY`, `TLS_CERT`: activa HTTPS local (ver más abajo).

Instala dependencias:

```bash
npm install
```

## Ejecución

- Desarrollo con recarga:

```bash
npm run dev
```

- Producción:

```bash
npm start
```

El servidor sirve los archivos estáticos desde `src/public` y el WebSocket en `WS_PATH`.

## HTTPS opcional con mkcert

Safari iOS puede exigir HTTPS para autoplay. Puedes generar un certificado local usando [mkcert](https://github.com/FiloSottile/mkcert):

```bash
mkcert -install
mkcert localhost
```

Coloca las rutas del `.pem` generado en `TLS_KEY` y `TLS_CERT`, y establece `USE_HTTPS=true`.

## Uso

1. Arranca el servidor en tu PC.
2. Abre `http://IP_DEL_PC:PORT/sender.html` en el iPhone.
3. Introduce un `roomId` y pulsa **Iniciar cámara**. Comparte el QR con el botón correspondiente.
4. En el PC abre `http://IP_DEL_PC:PORT/receiver.html#roomId=EL_ID` o introduce el ID manualmente y pulsa **Conectar**.
5. Deberías ver el video del iPhone en el navegador de escritorio.

## Troubleshooting iOS

- Asegúrate de conceder permisos de cámara.
- El primer gesto de usuario es necesario para `getUserMedia`.
- Algunas redes móviles pueden bloquear WebSockets.

## Licencia

MIT
