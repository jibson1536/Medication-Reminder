// static/js/scripts.js

document.addEventListener("DOMContentLoaded", () => {

    // ---------- MED LIST (medlist.html) ----------
    const medListEl = document.getElementById("med-list-js");
    if (medListEl) {
      fetch("/med/api/meds")
        .then(res => res.json())
        .then(meds => {
          medListEl.innerHTML = "";
          meds.forEach(med => {
            medListEl.innerHTML += `
              <div class="med-item">
                <div class="icon-box bg-blue">
                  <i class="bi bi-capsule"></i>
                </div>
                <div>
                  <div class="med-title">${med.name}</div>
                  <div class="med-sub">${med.dose} • ${med.freq}</div>
                </div>
                <i class="bi bi-three-dots-vertical more-icon"></i>
              </div>
            `;
          });
        });
    }
  
    // ---------- HISTORY (history.html) ----------
    const historyWrapper = document.getElementById("history-js");
    if (historyWrapper) {
      fetch("/profile/api/history")
        .then(res => res.json())
        .then(items => {
          historyWrapper.innerHTML = "";
          items.forEach(item => {
            const statusClass = item.status.toLowerCase();
            historyWrapper.innerHTML += `
              <div class="history-card shadow-sm">
                <div class="d-flex align-items-center gap-3">
                  <div class="hist-icon ${statusClass}">
                    ${item.status === "Taken"
                      ? '<i class="bi bi-check-circle-fill"></i>'
                      : '<i class="bi bi-x-circle-fill"></i>'}
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
        });
    }
  
    // ---------- DASHBOARD (dashboard.html) ----------
    const dashSchedule = document.getElementById("dashboard-schedule-js");
    if (dashSchedule) {
      fetch("/med/api/dashboard")
        .then(res => res.json())
        .then(data => {
          const meds = data.meds || [];
          dashSchedule.innerHTML = "";
          meds.forEach(med => {
            dashSchedule.innerHTML += `
              <div class="schedule-card">
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
        });
    }
  
    // ---------- NOTIFICATIONS ----------
    const notifWrapper = document.getElementById("notifications-js");
    if (notifWrapper) {
      fetch("/notify/api/notifications")
        .then(res => res.json())
        .then(items => {
          notifWrapper.innerHTML = "";
          items.forEach(item => {
            notifWrapper.innerHTML += `
              <div class="setting-row">
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
        });
    }
  
  });
  