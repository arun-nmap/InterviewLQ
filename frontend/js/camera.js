async function startCamera() {
  const video = document.getElementById("camera");
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
}
