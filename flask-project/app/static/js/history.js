// -------------------------------------
  // HISTORY (history.html)
  // -------------------------------------
  document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ history.js loaded");
  
    const weekAdhEl = document.getElementById("week-adherence");
    const weekTakenEl = document.getElementById("week-taken");
    const weekMissedEl = document.getElementById("week-missed");
    const todayListEl = document.getElementById("today-history-list");
  
    if (!weekAdhEl || !weekTakenEl || !weekMissedEl || !todayListEl) {
      console.warn("History elements not found in HTML.");
      return;
    }
  
    todayListEl.innerHTML = `<p class="text-muted">Loading...</p>`;
  
    fetch("/profile/api/history?days=7")
      .then(async (res) => {
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || "Failed to load history");
        return data;
      })
      .then((data) => {
        console.log("✅ history data:", data);
  
        // Week summary
        weekAdhEl.textContent = `${data.week?.adherence ?? 0}%`;
        weekTakenEl.textContent = data.week?.taken ?? 0;
        weekMissedEl.textContent = data.week?.missed ?? 0;
  
        // Today list
        const items = data.today || [];
  
        if (items.length === 0) {
          todayListEl.innerHTML = `<p class="text-muted">No medications found.</p>`;
          return;
        }
  
        todayListEl.innerHTML = items.map((item) => {
          const status = (item.status || "upcoming").toLowerCase();
  
          const icon =
            status === "taken"
              ? `<i class="bi bi-check-circle-fill"></i>`
              : status === "missed"
                ? `<i class="bi bi-x-circle-fill"></i>`
                : `<i class="bi bi-clock-fill"></i>`;
  
          const label =
            status === "taken" ? "Taken" :
            status === "missed" ? "Missed" :
            "Upcoming";
  
          return `
            <div class="history-card shadow-sm">
              <div class="d-flex align-items-center gap-3">
                <div class="hist-icon ${status}">
                  ${icon}
                </div>
  
                <div class="med-info">
                  <div class="med-name">${escapeHtml(item.name)}</div>
                  <div class="med-details">${escapeHtml(item.dose)} • ${escapeHtml(item.time)}</div>
                </div>
              </div>
  
              <span class="status ${status}">${label}</span>
            </div>
          `;
        }).join("");
      })
      .catch((err) => {
        console.error("❌ history fetch error:", err);
        todayListEl.innerHTML = `<p class="text-danger">Failed to load history.</p>`;
        weekAdhEl.textContent = "--%";
        weekTakenEl.textContent = "--";
        weekMissedEl.textContent = "--";
      });
  
    function escapeHtml(str) {
      return String(str ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }
  });
  
  