// Main JavaScript file for Crime Record Management System

// Initialize DataTables
function initializeDataTables() {
    // Apply DataTables to all tables with the datatable class
    $('.datatable').each(function() {
        $(this).DataTable({
            responsive: true,
            pageLength: 10,
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]]
        });
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize search functionality
function initializeSearch() {
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $(".searchable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
}

// Initialize delete confirmations
function initializeDeleteConfirmations() {
    $('.delete-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
}

// Show alert message
function showAlert(message, type = 'success') {
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    if (alertPlaceholder) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        alertPlaceholder.appendChild(wrapper);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(wrapper.querySelector('.alert'));
            alert.close();
        }, 5000);
    }
}

// Toggle sidebar on mobile
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
    document.querySelector('.content').classList.toggle('active');
}

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components if jQuery is available
    if (typeof $ !== 'undefined') {
        initializeDataTables();
        initializeSearch();
        initializeDeleteConfirmations();
    }
    
    // Initialize Bootstrap components
    initializeTooltips();
    
    // Add event listener for sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        if (currentLocation.includes(link.getAttribute('href'))) {
            link.parentElement.classList.add('active');
        }
    });
});