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

  todayListEl.innerHTML = `<p class="text-muted mb-0">Loading...</p>`;

  fetch("/profile/api/history?days=7")
    .then(async (res) => {
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || "Failed to load history");
      return data;
    })
    .then((data) => {
      console.log("✅ history data:", data);

      // ---- Week summary ----
      const week = data.week || {};
      weekAdhEl.textContent = `${week.adherence ?? 0}%`;
      weekTakenEl.textContent = week.taken ?? 0;
      weekMissedEl.textContent = week.missed ?? 0;

      // ---- Today list ----
      const items = Array.isArray(data.today) ? data.today : [];

      if (items.length === 0) {
        todayListEl.innerHTML = `<p class="text-muted mb-0">No medications found for today.</p>`;
        return;
      }

      // Optional: sort by time if format is HH:MM
      items.sort((a, b) => timeToMinutes(a?.time) - timeToMinutes(b?.time));

      todayListEl.innerHTML = items.map(renderTodayItem).join("");
    })
    .catch((err) => {
      console.error("❌ history fetch error:", err);
      todayListEl.innerHTML = `<p class="text-danger mb-0">Failed to load history.</p>`;
      weekAdhEl.textContent = "--%";
      weekTakenEl.textContent = "--";
      weekMissedEl.textContent = "--";
    });

  function renderTodayItem(item) {
    const status = normalizeStatus(item?.status);

    const label =
      status === "taken" ? "Taken" :
      status === "missed" ? "Missed" :
      "Upcoming";

    const icon =
      status === "taken" ? `<i class="bi bi-check-lg"></i>` :
      status === "missed" ? `<i class="bi bi-x-lg"></i>` :
      `<i class="bi bi-clock"></i>`;

    const name = escapeHtml(item?.name || "Medication");
    const dose = escapeHtml(item?.dose || "");
    const time = escapeHtml(item?.time || "");

    const meta = [dose, time].filter(Boolean).join(" • ");

    // IMPORTANT: class is today-item (matches your CSS)
    return `
      <div class="today-item">
        <div class="today-left">
          <div class="today-icon ${status}">
            ${icon}
          </div>

          <div class="today-text">
            <p class="today-name">${name}</p>
            <p class="today-meta">${meta || "—"}</p>
          </div>
        </div>

        <span class="today-pill ${status}">${label}</span>
      </div>
    `;
  }

  function normalizeStatus(raw) {
    const s = String(raw || "upcoming").toLowerCase().trim();

    // Accept different words from backend
    if (s === "taken" || s === "done" || s === "completed") return "taken";
    if (s === "missed" || s === "missing" || s === "skipped") return "missed";

    return "upcoming";
  }

  function timeToMinutes(t) {
    // expects "HH:MM" - returns big number if invalid so it goes last
    const str = String(t || "").trim();
    const match = str.match(/^(\d{1,2}):(\d{2})$/);
    if (!match) return 99999;
    const hh = Number(match[1]);
    const mm = Number(match[2]);
    if (Number.isNaN(hh) || Number.isNaN(mm)) return 99999;
    return hh * 60 + mm;
  }

  function escapeHtml(str) {
    return String(str ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
});
