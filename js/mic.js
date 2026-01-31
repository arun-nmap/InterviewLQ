let recorder;

async function startMic(ws) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  recorder.start();

  recorder.ondataavailable = e => {
    const reader = new FileReader();
    reader.onloadend = () => {
      ws.send(JSON.stringify({
        audio: reader.result
      }));
    };
    reader.readAsDataURL(e.data);
  };

  setTimeout(() => recorder.stop(), 10000);
}
