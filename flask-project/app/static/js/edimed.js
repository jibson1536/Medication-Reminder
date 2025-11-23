document.addEventListener("DOMContentLoaded", () => {

    const medId = document.getElementById("med-id")?.value;

    if (!medId) return;

    // -------- Load medication data --------
    fetch(`/med/api/med/${medId}`)
        .then(res => res.json())
        .then(med => {

            document.getElementById("med-name").value = med.name;
            document.getElementById("med-dose").value = parseInt(med.dose);
            document.getElementById("med-unit").value = med.dose.replace(/[0-9]/g, "");
            document.getElementById("med-time").value = convertTimeToInput(med.time);

        });


    // -------- Convert 08:00 AM → 08:00 --------
    function convertTimeToInput(t) {
        const [time, period] = t.split(" ");
        let [h, m] = time.split(":");
        if (period === "PM" && h !== "12") h = (parseInt(h) + 12).toString();
        if (period === "AM" && h === "12") h = "00";
        return `${h}:${m}`;
    }


    // -------- Save button --------
    document.getElementById("save-btn")?.addEventListener("click", () => {
        alert("Medication updated (dummy mode)");
        window.location.href = "/med/medlist";
    });

    // -------- Delete button --------
    document.getElementById("delete-btn")?.addEventListener("click", () => {
        if (confirm("Are you sure you want to delete this medication?")) {
            alert("Medication deleted (dummy)");
            window.location.href = "/med/medlist";
        }
    });

});
