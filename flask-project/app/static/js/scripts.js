// static/js/scripts.js

document.addEventListener("DOMContentLoaded", () => {
// -------------------------------------
// MED LIST (medlist.html)
// -------------------------------------
const medListEl = document.getElementById("med-list-js");

if (medListEl) {
  medListEl.innerHTML = `<p>Loading medications...</p>`;

  fetch("/med/api/meds")   // ✅ Correct URL
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
          <div class="med-title">${escapeHtml(med.name)}</div>
          <div class="med-sub">${escapeHtml(med.dose)} • ${escapeHtml(med.freq)}</div>
        </div>
      </div>

      <!-- Three-dot dropdown -->
      <div class="dropdown">
        <button class="btn btn-sm btn-light"
                type="button"
                data-bs-toggle="dropdown"
                aria-expanded="false">
          <i class="bi bi-three-dots-vertical"></i>
        </button>

        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <a class="dropdown-item" href="/med/editmed/${med._id}">
              <i class="bi bi-pencil me-2"></i>Edit
            </a>
          </li>
          <li>
            <button class="dropdown-item text-danger" type="button"
                    onclick="deleteMed('${med._id}')">
              <i class="bi bi-trash me-2"></i>Delete
            </button>
          </li>
        </ul>
      </div>
    </div>
  `;
});
// Delete medication via API, then reload the list
window.deleteMed = async function (medId) {
  if (!confirm("Delete this medication?")) return;

  const res = await fetch(`/med/api/meds/${medId}`, { method: "DELETE" });
  const data = await res.json().catch(() => ({}));

  if (res.ok && data.ok) {
    location.reload(); // simplest refresh
  } else {
    alert(data.error || "Delete failed");
  }
};

// Basic escaping to avoid HTML injection
function escapeHtml(str) {
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

    })
    .catch(err => {
      console.error(err);
      medListEl.innerHTML = `<p class="text-danger">Could not load medications.</p>`;
    });
}



  

  // -------------------------------------
  // DASHBOARD (dashboard.html)
 // -------------------------------------
// -------------------------------------
// DASHBOARD (dashboard.html)
// -------------------------------------
const dashSchedule = document.getElementById("dashboard-schedule-js");
const takenTodayEl = document.getElementById("taken-today-js");
const upcomingEl   = document.getElementById("upcoming-js");
const totalTodayEl = document.getElementById("total-today-js");
const heroGreetingEl = document.getElementById("hero-greeting-js");
const heroNameEl = document.getElementById("hero-name-js");

function loadDashboard() {
  dashSchedule.innerHTML = `<p>Loading today’s schedule...</p>`;

  fetch("/med/api/dashboard")
    .then(async res => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Dashboard HTTP ${res.status}: ${text}`);
      }
      return res.json();
    })
    .then(data => {
      const meds = data.meds || [];
      const stats = data.stats || {};

      // Update stats
      takenTodayEl.textContent  = stats.taken_today ?? "--";
      upcomingEl.textContent    = stats.upcoming ?? "--";
      totalTodayEl.textContent  = stats.total_today ?? "--";

      const now = new Date();

                // Dynamic greeting + logged in user name
    const hour = new Date().getHours();
    let greeting;

    if (hour < 12) greeting = "Good morning";
    else if (hour < 18) greeting = "Good afternoon";
    else greeting = "Good evening";

    heroGreetingEl.textContent = greeting;

    // Set first name only
    if (data.user?.name) {
      const firstName = data.user.name.split(" ")[0];
      heroNameEl.textContent = firstName;
    }

      

      // Auto-detect missed meds
      meds.forEach(med => {
        const medTime = new Date(`${med.date}T${med.time}:00`);
        if (med.status === "upcoming" && medTime < now) {
          med.status = "missed";
        }
      });

      // Sort: upcoming → missed → taken (each by time)
      const order = { upcoming: 0, missed: 1, taken: 2 };
      meds.sort((a, b) => {
        if (order[a.status] !== order[b.status])
          return order[a.status] - order[b.status];
        return a.time.localeCompare(b.time);
      });

      dashSchedule.innerHTML = "";

      let missedSection = "";
      let takenSection = "";

      meds.forEach(med => {
        const isTaken = med.status === "taken";
        const isMissed = med.status === "missed";

        if (isTaken) {
          takenSection += `
            <div class="schedule-card d-flex justify-content-between align-items-center mb-2 p-2 opacity-50 small">
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-check-circle-fill text-success"></i>
                <div>
                  <div class="med-name small">${med.name}</div>
                  <div class="med-meta small">${med.dose} • ${med.time}</div>
                </div>
              </div>
            </div>
          `;
          return;
        }

        if (isMissed) {
          missedSection += `
            <div class="schedule-card d-flex justify-content-between align-items-center mb-2 p-2 bg-danger-subtle">
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-exclamation-circle-fill text-danger"></i>
                <div>
                  <div class="med-name small">${med.name}</div>
                  <div class="med-meta small">${med.dose} • ${med.time}</div>
                </div>
              </div>
              <button class="btn btn-outline-light miss-btn" data-id="${med._id}">
                Mark Missed
              </button>
            </div>
          `;
          return;
        }

        // Upcoming meds
        dashSchedule.innerHTML += `
          <div class="schedule-card d-flex justify-content-between align-items-center mb-3 p-3">
            <div class="d-flex align-items-center gap-3">
              <i class="bi bi-capsule med-icon"></i>
              <div>
                <div class="med-name">${med.name}</div>
                <div class="med-meta">${med.dose} • ${med.time}</div>
              </div>
            </div>

            <button class="btn btn-outline-light take-btn"
                    data-id="${med._id}">
              Take
            </button>
          </div>
        `;
      });

      // Missed section
      if (missedSection) {
        dashSchedule.innerHTML += `
          <hr class="my-4" />
          <h6 class="text-danger mb-3">Missed</h6>
          ${missedSection}
        `;
      }

      // Taken section
      if (takenSection) {
        dashSchedule.innerHTML += `
          <hr class="my-4" />
          <h6 class="text-secondary mb-3">Taken Today</h6>
          ${takenSection}
        `;
      }

      attachButtonEvents();
    })
    .catch(err => {
      console.error("Dashboard error:", err);
      dashSchedule.innerHTML = `<p class="text-danger">Could not load schedule.</p>`;
    });
}

function attachButtonEvents() {
  // TAKE button
  document.querySelectorAll(".take-btn").forEach(btn => {
    btn.addEventListener("click", () => handleMedAction(btn.dataset.id, "take"));
  });

  // MISSED button
  document.querySelectorAll(".miss-btn").forEach(btn => {
    btn.addEventListener("click", () => handleMedAction(btn.dataset.id, "missed"));
  });
}

function handleMedAction(medId, action) {
  console.log("Updating med:", medId, "Action:", action);

  fetch(`/med/api/meds/${medId}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  })
    .then(async res => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`${action} HTTP ${res.status}: ${text}`);
      }
      return res.json();
    })
    .then(() => loadDashboard())
    .catch(err => {
      console.error(err);
      alert(`Could not mark medication as ${action}. Check console.`);
    });
}

if (dashSchedule) {
  loadDashboard();
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
