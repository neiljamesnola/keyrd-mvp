async function fetchData() {
    const res = await fetch('/dashboard/data');
    const data = await res.json();
    return data;
}

function updateCharts(data, charts) {
    const { labels, engagement, rewards, arms } = data;

    charts.engagementChart.data.labels = labels;
    charts.engagementChart.data.datasets[0].data = engagement;

    charts.rewardChart.data.labels = labels;
    charts.rewardChart.data.datasets[0].data = rewards;

    const counts = [0, 0, 0];
    arms.forEach(a => counts[a]++);
    charts.armChart.data.datasets[0].data = counts;

    Object.values(charts).forEach(c => c.update());
}

function setupCharts() {
    const engagementChart = new Chart(document.getElementById('engagementChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{ label: 'Engagement', data: [], borderColor: 'blue', fill: false }]
        }
    });

    const rewardChart = new Chart(document.getElementById('rewardChart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{ label: 'Reward', data: [], borderColor: 'green', fill: false }]
        }
    });

    const armChart = new Chart(document.getElementById('armChart'), {
        type: 'bar',
        data: {
            labels: ['Arm 0', 'Arm 1', 'Arm 2'],
            datasets: [{
                label: 'Selections',
                data: [0, 0, 0],
                backgroundColor: ['#3498db', '#2ecc71', '#e74c3c']
            }]
        }
    });

    return { engagementChart, rewardChart, armChart };
}

window.onload = async () => {
    const charts = setupCharts();
    const refresh = async () => {
        const data = await fetchData();
        updateCharts(data, charts);
    };
    await refresh();
    setInterval(refresh, 15000); // refresh every 15 seconds
};
