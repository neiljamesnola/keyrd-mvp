document.getElementById("sendPushBtn").addEventListener("click", async () => {
  const userId = document.getElementById("userIdSim").value.trim();
  if (!userId) {
    alert("User ID required.");
    return;
  }

  try {
    const res = await fetch(`/generate_nudge_payload/${userId}`);
    if (!res.ok) throw new Error("Failed to fetch nudge.");

    const data = await res.json();
    window.currentNudge = data;

    // Populate modal
    document.getElementById("pushProduct").textContent = data.suggestion.product;
    document.getElementById("pushModal").style.display = "flex";
  } catch (err) {
    alert("Push nudge failed.");
    console.error(err);
  }
});

function logPushAction(action) {
  const { user_id, nudge_id } = window.currentNudge;

  fetch("/log_push_interaction", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, nudge_id, action })
  })
    .then(res => {
      if (!res.ok) throw new Error("Log failed");
    })
    .catch(err => console.error("Logging error:", err));

  closePushModal();
}

function closePushModal() {
  document.getElementById("pushModal").style.display = "none";
}
