// Initialize charts when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the dashboard page
    if (document.getElementById('crimesChart')) {
        fetchAndRenderCrimeTypeChart();
        fetchAndRenderCriminalGenderChart();
        fetchAndRenderMonthlyCrimeChart();
    }
});

// Fetch and render crime type chart
function fetchAndRenderCrimeTypeChart() {
    fetch('/api/crime-stats/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('crimesChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Number of Crimes',
                        data: data.data,
                        backgroundColor: 'rgba(13, 71, 161, 0.7)',
                        borderColor: 'rgba(13, 71, 161, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Crime Types Distribution',
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching crime type data:', error));
}

// Fetch and render criminal gender chart
function fetchAndRenderCriminalGenderChart() {
    fetch('/api/criminal-stats/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('criminalsChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            'rgba(13, 71, 161, 0.7)',
                            'rgba(211, 47, 47, 0.7)',
                            'rgba(67, 160, 71, 0.7)'
                        ],
                        borderColor: [
                            'rgba(13, 71, 161, 1)',
                            'rgba(211, 47, 47, 1)',
                            'rgba(67, 160, 71, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Criminal Gender Distribution',
                            font: {
                                size: 16
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching criminal gender data:', error));
}

// Fetch and render monthly crime chart
function fetchAndRenderMonthlyCrimeChart() {
    fetch('/api/monthly-crime-stats/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('monthlyChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Number of FIRs',
                        data: data.data,
                        fill: false,
                        backgroundColor: 'rgba(13, 71, 161, 0.7)',
                        borderColor: 'rgba(13, 71, 161, 1)',
                        tension: 0.1,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly FIR Reports',
                            font: {
                                size: 16
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching monthly crime data:', error));
}
