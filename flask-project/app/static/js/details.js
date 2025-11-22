document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("details-js");
    if (!container) return;

    const medId = container.dataset.id;

    // Fetch updated med info
    fetch(`/med/api/med/${medId}`)
        .then(res => res.json())
        .then(med => {
            document.getElementById("med-name").textContent = med.name;
            document.getElementById("med-type").textContent = `${med.dose} • ${med.freq}`;

            const timePill = document.getElementById("time-pill");
            timePill.innerHTML = `<span class="time-pill">${med.time}</span>`;
        });

    // Delete button
    document.getElementById("delete-btn").addEventListener("click", () => {
        alert("Medication deleted (dummy — no real delete yet)");
        window.location.href = "/med/medlist";
    });
});
