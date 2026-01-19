document.addEventListener("DOMContentLoaded", () => {
  console.log("editmed.js loaded ✅");

  const medId = document.getElementById("med-id")?.value?.trim();
  if (!medId) {
    alert("Missing medication id. Fix editmed.html hidden input to use med._id.");
    return;
  }

  const debug = document.getElementById("debug-med-id");
  if (debug) debug.textContent = medId;

  const nameEl = document.getElementById("med-name");
  const doseEl = document.getElementById("med-dose");
  const unitEl = document.getElementById("med-unit");
  const timeEl = document.getElementById("med-time");

  // Load medication
  loadMed();

  async function loadMed() {
    try {
      const res = await fetch(`/med/api/meds/${medId}`);
      const med = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(med.error || `Failed to load medication (status ${res.status})`);
      }

      nameEl.value = med.name ?? "";

      const doseNum = parseInt(String(med.dose ?? "").replace(/\D/g, ""), 10);
      const unit = String(med.dose ?? "").replace(/[0-9]/g, "").trim() || "mg";

      doseEl.value = Number.isFinite(doseNum) ? doseNum : "";
      unitEl.value = unit;

      timeEl.value = convertTimeToInput(med.time);
    } catch (err) {
      console.error(err);
      alert(err.message || "Failed to load medication.");
    }
  }

  function convertTimeToInput(t) {
    if (!t) return "";
    const s = String(t).trim();

    // Already HH:MM
    if (!s.includes("AM") && !s.includes("PM")) return s;

    const [time, periodRaw] = s.split(" ");
    const period = (periodRaw || "").toUpperCase();

    let [h, m] = time.split(":");
    let hour = parseInt(h, 10);

    if (Number.isNaN(hour) || !m) return "";

    if (period === "PM" && hour !== 12) hour += 12;
    if (period === "AM" && hour === 12) hour = 0;

    return `${String(hour).padStart(2, "0")}:${m}`;
  }

  // UPDATE
  document.getElementById("save-btn")?.addEventListener("click", async () => {
    console.log("Update clicked ✅");

    const payload = {
      name: (nameEl.value || "").trim(),
      dose: parseInt((doseEl.value || "").trim(), 10),
      unit: (unitEl.value || "").trim(),
      time: (timeEl.value || "").trim(),
    };

    if (!payload.name || Number.isNaN(payload.dose) || !payload.unit || !payload.time) {
      alert("Please fill all fields.");
      return;
    }

    try {
      const res = await fetch(`/med/api/meds/${medId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.error || `Update failed (status ${res.status})`);
      }

      if (data.ok) {
        alert("Medication updated successfully!");
        window.location.href = "/med/medlist";
      } else {
        alert("Update failed: server did not return ok.");
      }
    } catch (err) {
      console.error(err);
      alert(err.message || "Update failed.");
    }
  });

  // DELETE
  document.getElementById("delete-btn")?.addEventListener("click", async () => {
    console.log("Delete clicked ✅");

    if (!confirm("Are you sure you want to delete this medication?")) return;

    try {
      const res = await fetch(`/med/api/meds/${medId}`, { method: "DELETE" });
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.error || `Delete failed (status ${res.status})`);
      }

      if (data.ok) {
        alert("Medication deleted.");
        window.location.href = "/med/medlist";
      } else {
        alert("Delete failed: server did not return ok.");
      }
    } catch (err) {
      console.error(err);
      alert(err.message || "Delete failed.");
    }
  });
});
