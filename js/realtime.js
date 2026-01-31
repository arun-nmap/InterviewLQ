let ws = null;
let resumeUploaded = false;

/* ========= RADAR ========= */
let radarChart;
let radarScores = {
  Communication: 50,
  Confidence: 50,
  Leadership: 50,
  Sociability: 50,
  Professionalism: 50
};

/* ========= EMOTION ========= */
let emotionChart;
let emotionIndex = 0;
const emotionMap = { confident: 80, neutral: 50, nervous: 30 };

/* ========= INIT ========= */
function initRadar() {
  radarChart = new Chart(document.getElementById("radarChart"), {
    type: "radar",
    data: {
      labels: Object.keys(radarScores),
      datasets: [{
        data: Object.values(radarScores),
        backgroundColor: "rgba(99,102,241,.2)",
        borderColor: "#6366f1"
      }]
    },
    options: { scales: { r: { min: 0, max: 100 } } }
  });
}

function initEmotionChart() {
  emotionChart = new Chart(document.getElementById("emotionChart"), {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        data: [],
        borderColor: "#22c55e",
        fill: true
      }]
    },
    options: {
      scales: { y: { min: 0, max: 100 } },
      plugins: { legend: { display: false } }
    }
  });
}

/* ========= UPDATE ========= */
function updateRadar(scores) {
  radarScores = { ...radarScores, ...scores };
  radarChart.data.datasets[0].data = Object.values(radarScores);
  radarChart.update();
}

function updateEmotionTimeline(emotion) {
  emotionIndex++;
  emotionChart.data.labels.push("T" + emotionIndex);
  emotionChart.data.datasets[0].data.push(emotionMap[emotion] ?? 50);
  emotionChart.update();
}

/* ========= RESUME ========= */
function uploadResume() {
  const f = document.getElementById("resume").files[0];
  if (!f) return alert("Select resume");

  const fd = new FormData();
  fd.append("resume", f);

  fetch("http://localhost:8000/upload_resume", {
    method: "POST",
    body: fd
  }).then(() => {
    resumeUploaded = true;
    alert("Resume uploaded");
  });
}

/* ========= INTERVIEW ========= */
function startInterview() {
  if (!resumeUploaded) return alert("Upload resume first");

  startCamera();
  ws = new WebSocket("ws://localhost:8000/ws/interview");

  ws.onopen = () => {
    startMic(ws);
    document.getElementById("waveform").style.display = "flex";
  };

  ws.onmessage = e => {
    const d = JSON.parse(e.data);

    if (d.question) question.innerText = d.question;
    if (d.confidence !== undefined) confidence.innerText = d.confidence + "%";

    if (d.emotion) {
      emotion.innerText = d.emotion;
      updateEmotionTimeline(d.emotion);
    }

    if (d.difficulty) difficulty.innerText = d.difficulty;
    if (d.transcript) transcript.innerText += "\n" + d.transcript;
    if (d.radar) updateRadar(d.radar);

    // ✅ BACKEND CONFIRMED STOP
    if (d.end) {
      stopInterview(false);
      alert("Interview stopped");
    }
  };
}

/* ========= STOP (FIXED) ========= */
function stopInterview(user = true) {
  if (!ws) return;

  if (user) {
    // 1️⃣ Send stop request ONLY
    ws.send(JSON.stringify({ type: "stop" }));
    return; // ❗ DO NOT close yet
  }

  // 2️⃣ Backend confirmed → cleanup
  ws.close();
  ws = null;

  if (typeof stopMic === "function") stopMic();

  const wf = document.getElementById("waveform");
  if (wf) wf.style.display = "none";
}

/* ========= REPORT ========= */
function downloadReport() {
  window.open("http://localhost:8000/report", "_blank");
}

/* ========= LOAD ========= */
window.onload = () => {
  initRadar();
  initEmotionChart();
};
