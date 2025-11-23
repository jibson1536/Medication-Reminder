// static/js/scripts.js

document.addEventListener("DOMContentLoaded", () => {

  // -------------------------------------
  // MED LIST (medlist.html)
  // -------------------------------------
  const medListEl = document.getElementById("med-list-js");

  if (medListEl) {
    // Optional: show loading state
    medListEl.innerHTML = `<p>Loading medications...</p>`;

    fetch("/api/meds")       // <-- requires @med_bp.route('/api/meds') in med_routes.py
      .then(res => {
        if (!res.ok) throw new Error("Failed to load medications");
        return res.json();
      })
      .then(meds => {
        medListEl.innerHTML = "";

        meds.forEach(med => {
          medListEl.innerHTML += `
            <div class="med-item d-flex align-items-center justify-content-between mb-3">
              <div class="d-flex align-items-center gap-3">
                <div class="icon-box bg-blue">
                  <i class="bi bi-capsule"></i>
                </div>
                <div>
                  <div class="med-title">${med.name}</div>
                  <div class="med-sub">${med.dose} • ${med.freq}</div>
                </div>
              </div>
              <i class="bi bi-three-dots-vertical more-icon"></i>
            </div>
          `;
        });
      })
      .catch(err => {
        console.error(err);
        medListEl.innerHTML = `<p class="text-danger">Could not load medications.</p>`;
      });
  }



  // -------------------------------------
  // HISTORY (history.html)
  // -------------------------------------
  const historyWrapper = document.getElementById("history-js");

  if (historyWrapper) {
    historyWrapper.innerHTML = `<p>Loading history...</p>`;

    fetch("/api/history")    // <-- matches @profile_bp.route('/api/history')
      .then(res => {
        if (!res.ok) throw new Error("Failed to load history");
        return res.json();
      })
      .then(items => {
        historyWrapper.innerHTML = "";

        items.forEach(item => {
          const statusClass = item.status.toLowerCase(); // "taken", "missed", etc.

          historyWrapper.innerHTML += `
            <div class="history-card shadow-sm mb-3 p-3 d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center gap-3">
                <div class="hist-icon ${statusClass}">
                  ${
                    item.status === "Taken"
                      ? '<i class="bi bi-check-circle-fill"></i>'
                      : '<i class="bi bi-x-circle-fill"></i>'
                  }
                </div>
                <div class="med-info">
                  <div class="med-name">${item.name}</div>
                  <div class="med-details">${item.dose} • ${item.time}</div>
                </div>
              </div>
              <span class="status ${statusClass}">${item.status}</span>
            </div>
          `;
        });
      })
      .catch(err => {
        console.error(err);
        historyWrapper.innerHTML = `<p class="text-danger">Could not load history.</p>`;
      });
  }



  // -------------------------------------
  // DASHBOARD (dashboard.html)
  // -------------------------------------
  // DASHBOARD (dashboard.html)
const dashSchedule = document.getElementById("dashboard-schedule-js");

const takenTodayEl = document.getElementById("taken-today-js");
const upcomingEl   = document.getElementById("upcoming-js");
const totalTodayEl = document.getElementById("total-today-js");

if (dashSchedule) {
  dashSchedule.innerHTML = `<p>Loading today’s schedule...</p>`;

  fetch("/api/dashboard")
    .then(res => {
      if (!res.ok) throw new Error("Failed to load dashboard data");
      return res.json();
    })
    .then(data => {
      const meds = data.meds || [];
      const stats = data.stats || {};

      // Fill stats if elements exist
      if (takenTodayEl && typeof stats.taken_today !== "undefined") {
        takenTodayEl.textContent = stats.taken_today;
      }
      if (upcomingEl && typeof stats.upcoming !== "undefined") {
        upcomingEl.textContent = stats.upcoming;
      }
      if (totalTodayEl && typeof stats.total_today !== "undefined") {
        totalTodayEl.textContent = stats.total_today;
      }

      dashSchedule.innerHTML = "";
      meds.forEach(med => {
        dashSchedule.innerHTML += `
          <div class="schedule-card d-flex justify-content-between align-items-center mb-3 p-3">
            <div class="d-flex align-items-center gap-3">
              <i class="bi bi-capsule med-icon"></i>
              <div>
                <div class="med-name">${med.name}</div>
                <div class="med-meta">${med.dose} • ${med.time}</div>
              </div>
            </div>
            <button class="btn btn-outline-light schedule-take-btn">Take</button>
          </div>
        `;
      });
    })
    .catch(err => {
      console.error(err);
      dashSchedule.innerHTML = `<p class="text-danger">Could not load schedule.</p>`;
    });
}



  // -------------------------------------
  // NOTIFICATIONS (notifications.html / notificationsettings.html)
  // -------------------------------------
  const notifWrapper = document.getElementById("notifications-js");

  if (notifWrapper) {
    notifWrapper.innerHTML = `<p>Loading notification settings...</p>`;

    fetch("/api/notifications")   // <-- matches @notify_bp.route('/api/notifications')
      .then(res => {
        if (!res.ok) throw new Error("Failed to load notifications");
        return res.json();
      })
      .then(items => {
        notifWrapper.innerHTML = "";

        items.forEach(item => {
          notifWrapper.innerHTML += `
            <div class="setting-row d-flex justify-content-between align-items-center mb-3">
              <div>
                <div class="setting-title">${item.name}</div>
                <div class="setting-desc">${item.desc}</div>
              </div>
              <div>
                <label class="switch">
                  <input type="checkbox" ${item.enabled ? "checked" : ""}>
                  <span class="slider round"></span>
                </label>
              </div>
            </div>
          `;
        });
      })
      .catch(err => {
        console.error(err);
        notifWrapper.innerHTML = `<p class="text-danger">Could not load notifications.</p>`;
      });
  }

});
