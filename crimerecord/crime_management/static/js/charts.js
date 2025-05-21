// Charts.js - Charting functionality for Crime Record Management System

// Crime Type Distribution Chart
function fetchAndRenderCrimeTypeChart() {
    fetch('/api/crime-type-distribution/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('crimeTypeChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Number of Crimes',
                        data: data.values,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                            'rgba(255, 159, 64, 0.7)',
                            'rgba(199, 199, 199, 0.7)',
                            'rgba(83, 102, 255, 0.7)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(199, 199, 199, 1)',
                            'rgba(83, 102, 255, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching crime type data:', error));
}

// Criminal Gender Distribution Chart
function fetchAndRenderCriminalGenderChart() {
    fetch('/api/criminal-gender-distribution/')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('genderChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Male', 'Female', 'Other'],
                    datasets: [{
                        data: data.values,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(255, 206, 86, 0.7)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching gender data:', error));
}

// Monthly Crime Statistics Chart
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
                        label: 'Number of Crimes',
                        data: data.values,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching monthly data:', error));
}

// Initialize all charts when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if the charts exist on the page before trying to render
    if (document.getElementById('crimeTypeChart')) {
        fetchAndRenderCrimeTypeChart();
    }
    
    if (document.getElementById('genderChart')) {
        fetchAndRenderCriminalGenderChart();
    }
    
    if (document.getElementById('monthlyChart')) {
        fetchAndRenderMonthlyCrimeChart();
    }
});