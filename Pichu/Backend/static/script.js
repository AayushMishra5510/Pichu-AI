// Vanilla JS ClickSpark for any element

const sparkAudio = new Audio(sparkAudioUrl || "static/audio/spark.mp3");

function createClickSpark({
  sparkColor = "#fff",
  sparkSize = 10,
  sparkRadius = 15,
  sparkCount = 8,
  duration = 400,
  easing = "ease-out",
  extraScale = 1.0,
  targetSelector = "html" // changed from "body" to "html"
} = {}) {
  const target = document.querySelector(targetSelector);
  if (!target) return;

  // Create a full-page canvas
  let canvas = document.getElementById("clickspark-canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.id = "clickspark-canvas";
    canvas.style.position = "absolute"; 
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.width = "100vw";
    canvas.style.height = "100vh";
    canvas.style.pointerEvents = "none";
    canvas.style.zIndex = "9999";
    document.body.appendChild(canvas);
  }
  const ctx = canvas.getContext("2d");

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  let sparks = [];

  function easeFunc(t) {
    switch (easing) {
      case "linear": return t;
      case "ease-in": return t * t;
      case "ease-in-out": return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      default: return t * (2 - t);
    }
  }

  function draw(now) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    sparks = sparks.filter(spark => {
      const elapsed = now - spark.startTime;
      if (elapsed >= duration) return false;
      const progress = elapsed / duration;
      const eased = easeFunc(progress);
      const distance = eased * sparkRadius * extraScale;
      const lineLength = sparkSize * (1 - eased);

      const x1 = spark.x + distance * Math.cos(spark.angle);
      const y1 = spark.y + distance * Math.sin(spark.angle);
      const x2 = spark.x + (distance + lineLength) * Math.cos(spark.angle);
      const y2 = spark.y + (distance + lineLength) * Math.sin(spark.angle);

      ctx.strokeStyle = sparkColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();

      return true;
    });
    if (sparks.length > 0) {
      requestAnimationFrame(draw);
    }
  }

  target.addEventListener("click", function(e) {
    // Play sound
    if (sparkAudio) {
      sparkAudio.currentTime = 0;
      sparkAudio.play();
    }
    const x = e.clientX;
    const y = e.clientY;
    const now = performance.now();
    for (let i = 0; i < sparkCount; i++) {
      sparks.push({
        x,
        y,
        angle: (2 * Math.PI * i) / sparkCount,
        startTime: now
      });
    }
    requestAnimationFrame(draw);
  });
}

// Initialize ClickSpark on the whole page
document.addEventListener("DOMContentLoaded", function() {
  createClickSpark({
    sparkColor: "#fff",
    sparkSize: 10,
    sparkRadius: 15,
    sparkCount: 8,
    duration: 400,
    targetSelector: "html" // Use "html" to cover the entire viewport
    
  });
});


// Clear chat history (if you want this here)
document.getElementById('clearBtn').addEventListener('click', function() {
  document.getElementById('chat').innerHTML = '';
});



