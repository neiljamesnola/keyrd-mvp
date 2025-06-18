document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("get-nudge");
  const display = document.getElementById("nudge-display");

  button?.addEventListener("click", () => {
    fetch("/nudge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: display.dataset.state })
    })
    .then(response => response.json())
    .then(data => {
      const nudge = document.createElement("div");
      nudge.id = "nudge";
      nudge.textContent = `🧠 Nudge: ${data.text}`;
      display.innerHTML = ""; // Clear previous nudge
      display.appendChild(nudge);

      setTimeout(() => {
        nudge.remove();
      }, 5000);
    });
  });
});
