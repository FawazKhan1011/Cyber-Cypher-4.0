function showSection(event, sectionId) {
    event.preventDefault(); // Prevent page reload issues

    // Hide all sections
    document.querySelectorAll('.feature-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';

    // Remove "active" class from all tabs
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.classList.remove('active');
    });

    // Add "active" class to the clicked tab
    event.target.classList.add('active');
}
