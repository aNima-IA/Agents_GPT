// Wrapper to generate QR codes using a CDN-loaded library
export async function generateQR(canvas, text) {
  const { default: QRCode } = await import('https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.mjs');
  try {
    await QRCode.toCanvas(canvas, text, { margin: 1 });
  } catch (err) {
    console.error(err);
  }
}
