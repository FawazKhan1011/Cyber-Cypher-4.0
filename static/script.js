function showSection(event, sectionId) {
    if (event) event.preventDefault(); // Prevent default link behavior

    // Hide all feature sections
    document.querySelectorAll(".feature-section").forEach(section => {
        section.style.display = "none";
    });

    // Show the selected feature section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = "block";
    }

    // Update active tab styling (underline + blue text)
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });

    const activeLink = document.querySelector(`.nav-link[data-section='${sectionId}']`);
    if (activeLink) {
        activeLink.classList.add("active");
    }

    // Store selected feature in sessionStorage
    sessionStorage.setItem('selectedFeature', sectionId);
}

document.addEventListener("DOMContentLoaded", function () {
    const selectedFeature = sessionStorage.getItem('selectedFeature') || 'idea-validator'; // Default to Idea Validator
    showSection(null, selectedFeature); // Open the correct section
});