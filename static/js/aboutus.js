//JS for scroll animation
    document.addEventListener("DOMContentLoaded", function () {
        const sections = document.querySelectorAll(".scroll-reveal");
        function revealOnScroll() {
            sections.forEach(section => {
                const sectionTop = section.getBoundingClientRect().top;
                if (sectionTop < window.innerHeight * 0.85) {
                    section.classList.add("scroll-active");
                }
            });
        }
        window.addEventListener("scroll", revealOnScroll);
        revealOnScroll();
    });


// Data for the incidents chart
    const incidentsData = {
      labels: ['2015', '2018', '2021', '2024'],
      datasets: [
        {
          label: 'Road Accidents',
          data: [12000, 18000, 25000, 34000],
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 2,
          fill: true
        },
        {
          label: 'Reported Health Issues',
          data: [30000, 42000, 57000, 75000],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 2,
          fill: true
        }
      ]
    };

    // Revised data for the monitoring effectiveness chart
    const monitoringData = {
      labels: ['2017', '2019', '2021', '2023'],
      datasets: [
        {
          label: 'Early Disease Detection Rate (%)',
          data: [15, 28, 45, 62],
          borderColor: '#22c55e',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderWidth: 2,
          fill: true
        },
        {
          label: 'Vaccination Coverage (%)',
          data: [22, 35, 58, 73],
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          borderWidth: 2,
          fill: true
        },
        {
          label: 'Treatment Success Rate (%)',
          data: [40, 52, 68, 81],
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          borderWidth: 2,
          fill: true
        }
      ]
    };

    // Custom tooltip for both charts
    const customTooltip = (context) => {
      if (context.tooltip.dataPoints) {
        const year = context.tooltip.dataPoints[0].label;
        let content = `<div class="bg-white p-3 border rounded shadow">
          <div class="font-bold mb-2">Year: ${year}</div>`;
        
        context.tooltip.dataPoints.forEach(dataPoint => {
          content += `<div style="color: ${dataPoint.dataset.borderColor}">
            ${dataPoint.dataset.label}: ${dataPoint.raw.toLocaleString()}${dataPoint.dataset.label.includes('%') ? '%' : ''}
          </div>`;
        });

        if (context.tooltip.dataPoints[0].datasetIndex === 0 && context.chart.canvas.id === 'incidentsChart') {
          const accidents = context.tooltip.dataPoints[0].raw;
          const healthIssues = context.tooltip.dataPoints[1]?.raw;
          if (accidents && healthIssues) {
            const ratio = (healthIssues / accidents).toFixed(2);
            content += `<div class="text-gray-600 mt-2">Health Issues to Accidents Ratio: ${ratio}</div>`;
          }
        }

        content += '</div>';
        return content;
      }
      return false;
    };

    // Common chart options
    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          enabled: false,
          external: function(context) {
            let tooltipEl = document.getElementById('chartjs-tooltip');
            
            if (!tooltipEl) {
              tooltipEl = document.createElement('div');
              tooltipEl.id = 'chartjs-tooltip';
              document.body.appendChild(tooltipEl);
            }

            if (context.tooltip.opacity === 0) {
              tooltipEl.style.opacity = 0;
              return;
            }

            tooltipEl.innerHTML = customTooltip(context);
            tooltipEl.style.position = 'absolute';
            tooltipEl.style.left = context.tooltip.caretX + 'px';
            tooltipEl.style.top = context.tooltip.caretY + 'px';
            tooltipEl.style.opacity = 1;
            tooltipEl.style.pointerEvents = 'none';
          }
        },
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    };

    // Initialize the incidents chart
    new Chart(document.getElementById('incidentsChart'), {
      type: 'line',
      data: incidentsData,
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y: {
            ...commonOptions.scales.y,
            title: {
              display: true,
              text: 'Number of Cases'
            }
          }
        }
      }
    });

    // Initialize the monitoring effectiveness chart
    new Chart(document.getElementById('monitoringChart'), {
      type: 'line',
      data: monitoringData,
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y: {
            ...commonOptions.scales.y,
            title: {
              display: true,
              text: 'Percentage (%)'
            },
            max: 100
          }
        }
      }
    });