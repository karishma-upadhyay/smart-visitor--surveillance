let totalVisitors = 0;
let activeVisitors = 0;
let avgDuration = 0;

function addVisitor() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const location = document.getElementById("location").value;
    const purpose = document.getElementById("purpose").value.trim();

    // Validate input
    if (!name || !email || !location || !purpose) {
        alert("⚠️ Please fill in all the fields before adding a visitor.");
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("❌ Please enter a valid email address.");
        return;
    }

    // Update stats
    totalVisitors++;
    activeVisitors++;
    avgDuration = Math.floor(Math.random() * 60) + 20;

    document.getElementById("total-visitors").innerText = totalVisitors;
    document.getElementById("active-visitors").innerText = activeVisitors;
    document.getElementById("avg-duration").innerText = avgDuration;

    alert("✅ Visitor Added Successfully!");

    // Reset form
    document.getElementById("visitor-form").reset();
}

// Add Face button event
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("addFaceBtn").addEventListener("click", () => {
        alert("📸 Add Face functionality coming soon!");
    });
});
document.getElementById("addFaceBtn").addEventListener("click", function () {
    fetch('http://localhost:5000/run_face_recognition')
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Optional: show confirmation
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Failed to start face recognition.");
        });
});
