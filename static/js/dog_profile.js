let pulseChart;
let lastPulse;
let pulseData = [];
const dogHealthStatus = "{{ dog.health_status }}";
let oxygenLevel;

// Configure pulse and oxygen values based on health status
function configureVitalsForHealthStatus() {
    // Set appropriate ranges based on health status
    let minPulse, maxPulse, pulseVariation;
    
    if (dogHealthStatus === 'Healthy') {
        minPulse = 70;
        maxPulse = 100;
        pulseVariation = 3;  // Small variation for healthy dogs
        oxygenLevel = Math.floor(Math.random() * (100 - 95) + 95); // 95-100% for healthy
    } else if (dogHealthStatus === 'At Risk') {
        minPulse = 60;
        maxPulse = 120;
        pulseVariation = 5;  // Medium variation for at-risk dogs
        oxygenLevel = Math.floor(Math.random() * (94 - 90) + 90); // 90-94% for at-risk
    } else {
        // Danger status
        minPulse = 40;
        maxPulse = 150;
        pulseVariation = 8;  // Large variation for dogs in danger
        oxygenLevel = Math.floor(Math.random() * (89 - 75) + 75); // 75-89% for danger
    }
    
    // Set initial pulse value
    lastPulse = Math.floor(Math.random() * (maxPulse - minPulse) + minPulse);
    
    // Set oxygen level in UI
    document.getElementById('oxygenBadge').textContent = `${oxygenLevel}%`;
    document.getElementById('spo2Value').textContent = oxygenLevel;
    
    return { minPulse, maxPulse, pulseVariation };
}

function generateInitialPulseData() {
    const { minPulse, maxPulse, pulseVariation } = configureVitalsForHealthStatus();
    
    for (let i = 0; i < 10; i++) {
        let newPulse = lastPulse + Math.floor(Math.random() * (pulseVariation * 2) - pulseVariation);
        newPulse = Math.max(minPulse, Math.min(maxPulse, newPulse));
        pulseData.push(newPulse);
        lastPulse = newPulse;
    }
    document.getElementById('currentPulse').textContent = `${lastPulse} BPM`;
    return pulseData;
}

function getNextPulseReading() {
    const { minPulse, maxPulse, pulseVariation } = configureVitalsForHealthStatus();
    let newPulse = lastPulse + Math.floor(Math.random() * (pulseVariation * 2) - pulseVariation);
    newPulse = Math.max(minPulse, Math.min(maxPulse, newPulse));
    lastPulse = newPulse;
    return newPulse;
}

function getCurrentTimeLabels() {
    let labels = [];
    let now = new Date();
    
    for (let i = 9; i >= 0; i--) {
        let time = new Date(now.getTime() - i * 5000);
        let minutes = time.getMinutes().toString().padStart(2, '0');
        let seconds = time.getSeconds().toString().padStart(2, '0');
        labels.push(`${minutes}:${seconds}`);
    }
    
    return labels;
}

function updateChart() {
    // Shift existing data and add new reading
    pulseData.shift();
    pulseData.push(getNextPulseReading());
    
    // Update display
    document.getElementById('currentPulse').textContent = `${lastPulse} BPM`;
    
    // Update chart with new data and labels
    pulseChart.data.labels = getCurrentTimeLabels();
    pulseChart.data.datasets[0].data = pulseData;
    pulseChart.update('active');
    
    // Occasionally update oxygen reading
    if (Math.random() < 0.2) {  // 20% chance to update the oxygen reading
        let variation = dogHealthStatus === 'Healthy' ? 1 : (dogHealthStatus === 'At Risk' ? 2 : 3);
        oxygenLevel = oxygenLevel + Math.floor(Math.random() * (variation * 2) - variation);
        
        // Apply appropriate bounds based on health status
        if (dogHealthStatus === 'Healthy') {
            oxygenLevel = Math.max(95, Math.min(100, oxygenLevel));
        } else if (dogHealthStatus === 'At Risk') {
            oxygenLevel = Math.max(90, Math.min(94, oxygenLevel));
        } else {
            oxygenLevel = Math.max(75, Math.min(89, oxygenLevel));
        }
        
        document.getElementById('oxygenBadge').textContent = `${oxygenLevel}%`;
        document.getElementById('spo2Value').textContent = oxygenLevel;
    }
}

function renderChart() {
    const ctx = document.getElementById('pulseChart').getContext('2d');
    
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.3)');
    gradient.addColorStop(1, 'rgba(236, 72, 153, 0.1)');
    
    pulseData = generateInitialPulseData();
    
    // Set y-axis scale based on health status
    let yAxisConfig = {};
    if (dogHealthStatus === 'Healthy') {
        yAxisConfig = { min: 60, max: 110 };
    } else if (dogHealthStatus === 'At Risk') {
        yAxisConfig = { min: 50, max: 130 };
    } else {
        yAxisConfig = { min: 30, max: 160 };
    }
    
    pulseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getCurrentTimeLabels(),
            datasets: [{
                label: 'Pulse Rate',
                data: pulseData,
                borderColor: dogHealthStatus === 'Healthy' ? 'rgb(56, 189, 248)' : 
                             (dogHealthStatus === 'At Risk' ? 'rgb(234, 179, 8)' : 'rgb(239, 68, 68)'),
                borderWidth: 3,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: 'white',
                pointBorderColor: dogHealthStatus === 'Healthy' ? 'rgb(56, 189, 248)' : 
                                  (dogHealthStatus === 'At Risk' ? 'rgb(234, 179, 8)' : 'rgb(239, 68, 68)'),
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    ...yAxisConfig,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        stepSize: 20,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
    
    setInterval(updateChart, 5000);
}

document.addEventListener('DOMContentLoaded', renderChart);