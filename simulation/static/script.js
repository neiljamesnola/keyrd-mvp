let charts = {};

function setupCharts() {
  charts.engagementChart = new Chart(document.getElementById('engagementChart'), {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Engagement',
        data: [],
        borderColor: '#3498db',
        borderWidth: 2,
        fill: false
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, max: 1 }
      }
    }
  });

  charts.rewardChart = new Chart(document.getElementById('rewardChart'), {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Reward',
        data: [],
        borderColor: '#2ecc71',
        borderWidth: 2,
        fill: false
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, max: 1 }
      }
    }
  });

  charts.armChart = new Chart(document.getElementById('armChart'), {
    type: 'bar',
    data: {
      labels: ['Arm 0', 'Arm 1', 'Arm 2'],
      datasets: [{
        label: 'Selections',
        data: [0, 0, 0],
        backgroundColor: ['#3498db', '#2ecc71', '#e74c3c']
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      scales: {
        x: { beginAtZero: true }
      }
    }
  });
}

async function loadUserData() {
  const userId = document.getElementById('userSelect').value.trim();
  const status = document.getElementById('statusMsg');
  if (!userId) {
    status.innerText = "Please enter a user ID.";
    return;
  }

  try {
    const res = await fetch(`/dashboard/data?user_id=${userId}`);
    if (!res.ok) throw new Error(`Server responded with ${res.status}`);
    const { labels, engagement, rewards, arms } = await res.json();

    charts.engagementChart.data.labels = labels;
    charts.engagementChart.data.datasets[0].data = engagement;

    charts.rewardChart.data.labels = labels;
    charts.rewardChart.data.datasets[0].data = rewards;

    const counts = [0, 0, 0];
    arms.forEach(a => counts[a]++);
    charts.armChart.data.datasets[0].data = counts;

    Object.values(charts).forEach(chart => chart.update());
    status.innerText = `Loaded data for ${userId}`;
  } catch (err) {
    console.error(err);
    status.innerText = `Error loading data.`;
  }
}

window.onload = () => setupCharts();
