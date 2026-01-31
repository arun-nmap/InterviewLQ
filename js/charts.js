let radar;

function initRadar() {
  const ctx = document.getElementById("radarChart");
  radar = new Chart(ctx, {
    type: "radar",
    data: {
      labels: [
        "Communication",
        "Confidence",
        "Leadership",
        "Sociability",
        "Professionalism"
      ],
      datasets: [{
        label: "AI Score",
        data: [70, 65, 60, 75, 80],
        backgroundColor: "rgba(99,102,241,0.2)",
        borderColor: "#6366f1",
        pointBackgroundColor: "#6366f1"
      }]
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}
