// Wait for the DOM to completely load
document.addEventListener('DOMContentLoaded', () => {
    const reportForm = document.getElementById('reportForm');

    if (reportForm) {
        reportForm.addEventListener('submit', (event) => {
            // Simple validation confirmation or logging
            console.log("Submitting report form...");
            alert("Thank you! Your submission is processing and sending to USIU Security.");
        });
    }
});