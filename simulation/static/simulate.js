// static/simulate.js

let currentUserId = null;
let currentArm = null;
let running = false;

document.getElementById("previewNudgeBtn").addEventListener("click", async () => {
  const userId = currentUserId || document.getElementById("userIdSim").value;
  if (!userId) {
    alert("No user ID available. Run a simulation first.");
    return;
  }

  const res = await fetch(`/generate_nudge_payload/${userId}`);
  const data = await res.json();
  const previewBox = document.getElementById("nudgePreview");
  previewBox.textContent = JSON.stringify(data, null, 2);
  previewBox.style.display = "block";
});

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function startSimulation() {
  if (running) return;

  running = true;
  const iterations = parseInt(document.getElementById("iterations").value);
  const delayMs = parseInt(document.getElementById("delay").value);

  const userIdInput = document.getElementById("userIdSim").value;
  if (userIdInput) {
    currentUserId = userIdInput;
  } else {
    const metadata = {
      consent_flag: document.getElementById("consentCheck").checked,
      age_range: document.getElementById("ageRange").value,
      gender: document.getElementById("gender").value,
      ethnicity: document.getElementById("ethnicity").value
    };

    const regRes = await fetch("/register_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(metadata)
    });

    const regData = await regRes.json();
    if (!regData.user_id) {
      alert("User registration failed.");
      running = false;
      return;
    }

    currentUserId = regData.user_id;
  }

  for (let i = 0; i < iterations; i++) {
    if (!running) break;
    await triggerNudge();
    await delay(delayMs);
  }

  running = false;
}

async function triggerNudge() {
  const res = await fetch("/notify_user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: currentUserId })
  });

  const data = await res.json();
  if (!data || data.error) {
    log("Nudge error: " + (data.error || "unknown"));
    return;
  }

  currentArm = data.recommended_arm;

  // Show modal
  const modal = document.getElementById("simModal");
  const title = document.getElementById("simTitle");
  const body = document.getElementById("simBody");
  modal.style.display = "flex";

  title.textContent = `Try this: Action #${data.recommended_arm}`;
  body.textContent = `System suggests this nudge. Engagement: ${data.engagement} | Reward: ${data.reward}`;

  log(`⏳ Nudge #${data.recommended_arm} at ${data.timestamp}`);
}

function respondSim(accepted) {
  const modal = document.getElementById("simModal");
  modal.style.display = "none";

  fetch("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: currentUserId,
      arm: currentArm,
      accepted: accepted
    })
  }).then(res => res.json()).then(data => {
    log(`✅ Response: ${accepted ? "Accepted" : "Dismissed"} | Logged at ${data.timestamp}`);
  }).catch(err => {
    log("❌ Feedback error: " + err.message);
  });
}

function log(msg) {
  const logArea = document.getElementById("logArea");
  logArea.textContent += msg + "\n";
  logArea.scrollTop = logArea.scrollHeight;
}
