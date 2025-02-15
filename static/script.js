// Function to toggle sections
function showSection(sectionId) {
    document.querySelectorAll(".feature-section").forEach((section) => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
    
    const buttons = document.querySelectorAll(".nav-tabs .nav-link");
    buttons.forEach(button => {
        button.classList.remove("active");
    });
    document.querySelector(`.nav-tabs .nav-link[data-target="${sectionId}"]`).classList.add("active");
}
