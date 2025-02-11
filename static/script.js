document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("mobile-menu-button");
    const menu = document.getElementById("mobile-menu");
    const menuIcon = document.getElementById("menu-icon");
    const closeIcon = document.getElementById("close-icon");

    menuButton.addEventListener("click", function () {
        const isHidden = menu.classList.contains("hidden");
        menu.classList.toggle("hidden");
        menuIcon.classList.toggle("hidden", !isHidden);
        closeIcon.classList.toggle("hidden", isHidden);
    });

    // Optional: Close menu when clicking outside
    document.addEventListener("click", function (event) {
        if (!menu.contains(event.target) && !menuButton.contains(event.target)) {
            menu.classList.add("hidden");
            menuIcon.classList.remove("hidden");
            closeIcon.classList.add("hidden");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("pulseChart").getContext("2d");
    
    let pulseChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: Array(10).fill(""),  // Empty labels (dynamic)
            datasets: [{
                label: "Pulse Rate",
                data: [],
                borderColor: "#1E90FF",  // Sky blue
                backgroundColor: "rgba(30, 144, 255, 0.2)",  // Light sky blue
                borderWidth: 2,
                tension: 0.3, // Smooth line
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 50, max: 150 },
            },
        }
    });

    function updateChart() {
        fetch(`/api/pulse/${dogId}`)
            .then(response => response.json())
            .then(data => {
                pulseChart.data.labels = Array(data.length).fill("");  // Reset labels
                pulseChart.data.datasets[0].data = data;
                pulseChart.update();
            });
    }

    setInterval(updateChart, 3000);  // Refresh every 3 seconds
});


