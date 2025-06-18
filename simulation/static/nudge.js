// static/nudge.js

document.addEventListener("DOMContentLoaded", function () {
  const userIdInput = document.getElementById("userId");
  const nudgeContent = document.getElementById("nudgeContent");
  const acceptBtn = document.getElementById("acceptBtn");
  const dismissBtn = document.getElementById("dismissBtn");
  const feedback = document.getElementById("feedback");

  async function getNudge(user_id) {
    try {
      const res = await fetch("/get_nudge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id })
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      return data;
    } catch (err) {
      nudgeContent.textContent = `Error: ${err.message}`;
      return null;
    }
  }

  async function sendFeedback(user_id, arm, accepted) {
    try {
      const res = await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, arm, accepted })
      });
      const data = await res.json();
      feedback.textContent = `Response logged: ${accepted ? "Accepted" : "Dismissed"}`;
    } catch (err) {
      feedback.textContent = `Error logging feedback.`;
    }
  }

  async function showNudge() {
    const user_id = userIdInput.value.trim();
    if (!user_id) {
      feedback.textContent = "Please enter a valid user ID.";
      return;
    }

    feedback.textContent = "";
    const data = await getNudge(user_id);
    if (!data) return;

    nudgeContent.textContent = `Try Arm ${data.recommended_arm} — Engagement: ${data.engagement}`;

    acceptBtn.onclick = () => sendFeedback(user_id, data.recommended_arm, true);
    dismissBtn.onclick = () => sendFeedback(user_id, data.recommended_arm, false);
  }

  // Auto-fetch nudge on load (optional)
  // showNudge();

  // Button trigger (if desired)
  document.getElementById("acceptBtn").addEventListener("click", (e) => e.preventDefault());
  document.getElementById("dismissBtn").addEventListener("click", (e) => e.preventDefault());

  // Fetch on Enter key
  userIdInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") showNudge();
  });
});
