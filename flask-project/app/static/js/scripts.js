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
const dashSchedule    = document.getElementById("dashboard-schedule-js");
const takenTodayEl    = document.getElementById("taken-today-js");
const upcomingEl      = document.getElementById("upcoming-js");
const totalTodayEl    = document.getElementById("total-today-js");
const heroGreetingEl  = document.getElementById("hero-greeting-js");
const heroNameEl      = document.getElementById("hero-name-js");
const notifySoundEl   = document.getElementById("notifySound");

// --- Notification state (prevents spam) ---
const sent = new Set();              // medId|YYYY-MM-DD|type
const lastMissedNotify = new Map();  // medId -> ms timestamp
const MISSED_REPEAT_MS = 2 * 60 * 1000; // 2 minutes

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function onceKey(medId, type) {
  return `${medId}|${todayKey()}|${type}`;
}

function playSound() {
  if (!notifySoundEl) return;
  notifySoundEl.currentTime = 0;
  notifySoundEl.play().catch(() => {
    // Browser may block until user interacts once
  });
}

function sendNotification(title, body) {
  // Popup (if allowed)
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(title, { body });
  }
  // Sound
  playSound();
}

async function ensureNotificationPermission() {
  if (!("Notification" in window)) return;
  if (Notification.permission === "default") {
    try { await Notification.requestPermission(); } catch (_) {}
  }
}

// Parse "HH:MM" into a Date object for today
function timeToDateToday(hhmm) {
  const s = String(hhmm || "").trim();
  if (s.length !== 5 || !s.includes(":")) return null;
  const [h, m] = s.split(":").map(Number);
  if (Number.isNaN(h) || Number.isNaN(m)) return null;
  const d = new Date();
  d.setHours(h, m, 0, 0);
  return d;
}

function updateGreeting() {
  if (!heroGreetingEl) return;
  const hour = new Date().getHours();
  let greeting;
  if (hour < 12) greeting = "Good morning";
  else if (hour < 18) greeting = "Good afternoon";
  else greeting = "Good evening";
  heroGreetingEl.textContent = greeting;
}

function updateHeroNameFallback() {
  // Your API doesn't currently return data.user, so keep existing template text.
  // If you later add user to /med/api/dashboard, you can set it here.
  if (!heroNameEl) return;
}

function evaluateAndNotify(meds) {
  const now = new Date();

  meds.forEach(med => {
    const medId = med._id;
    const status = String(med.status || "upcoming").toLowerCase();
    const medTime = timeToDateToday(med.time);
    if (!medId || !medTime) return;

    // If taken, stop missed repeats
    if (status === "taken") {
      lastMissedNotify.delete(medId);
      return;
    }

    const diffMin = Math.floor((medTime.getTime() - now.getTime()) / 60000);

    // 10 minutes before
    if (diffMin === 10 && !sent.has(onceKey(medId, "before10"))) {
      sendNotification("Medication Reminder",
        `${med.name} (${med.dose}) in 10 minutes (${med.time})`);
      sent.add(onceKey(medId, "before10"));
    }

    // 5 minutes before
    if (diffMin === 5 && !sent.has(onceKey(medId, "before5"))) {
      sendNotification("Medication Reminder",
        `${med.name} (${med.dose}) in 5 minutes (${med.time})`);
      sent.add(onceKey(medId, "before5"));
    }

    // On time (within the current minute)
    if (diffMin === 0 && !sent.has(onceKey(medId, "ontime"))) {
      sendNotification("Time to take your medication",
        `${med.name} (${med.dose}) now (${med.time})`);
      sent.add(onceKey(medId, "ontime"));
    }

    // Missed logic: after time and not taken → repeat every 2 minutes
    if (now.getTime() > medTime.getTime()) {
      const last = lastMissedNotify.get(medId) || 0;
      if (now.getTime() - last >= MISSED_REPEAT_MS) {
        sendNotification("Missed Dose Alert",
          `You missed ${med.name} (${med.dose}) at ${med.time}. Please mark as Taken.`);
        lastMissedNotify.set(medId, now.getTime());
      }
    }
  });
}

function loadDashboard() {
  if (!dashSchedule) return;

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
      if (takenTodayEl) takenTodayEl.textContent = stats.taken_today ?? "--";
      if (upcomingEl) upcomingEl.textContent     = stats.upcoming ?? "--";
      if (totalTodayEl) totalTodayEl.textContent = stats.total_today ?? "--";

      updateGreeting();
      updateHeroNameFallback();

      // Auto-detect missed meds (based on today's date + HH:MM)
      const now = new Date();
      meds.forEach(med => {
        const t = timeToDateToday(med.time);
        if (t && String(med.status).toLowerCase() === "upcoming" && t < now) {
          med.status = "missed";
        }
      });

      // 🔔 Trigger notifications based on meds state
      evaluateAndNotify(meds);

      // Sort: upcoming → missed → taken
      const order = { upcoming: 0, missed: 1, taken: 2 };
      meds.sort((a, b) => {
        const sa = String(a.status || "upcoming").toLowerCase();
        const sb = String(b.status || "upcoming").toLowerCase();
        if (order[sa] !== order[sb]) return order[sa] - order[sb];
        return String(a.time || "").localeCompare(String(b.time || ""));
      });

      // Render list
      dashSchedule.innerHTML = "";

      let missedSection = "";
      let takenSection = "";

      meds.forEach(med => {
        const status = String(med.status || "upcoming").toLowerCase();
        const isTaken = status === "taken";
        const isMissed = status === "missed";

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
              <button class="btn btn-success take-btn" data-id="${med._id}">
                Mark as Taken
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

            <button class="btn btn-outline-light take-btn" data-id="${med._id}">
              Take
            </button>
          </div>
        `;
      });

      if (missedSection) {
        dashSchedule.innerHTML += `
          <hr class="my-4" />
          <h6 class="text-danger mb-3">Missed</h6>
          ${missedSection}
        `;
      }

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
  // Prevent duplicate listeners by using event delegation could be better,
  // but keeping your approach for simplicity.
  document.querySelectorAll(".take-btn").forEach(btn => {
    btn.addEventListener("click", () => handleMedAction(btn.dataset.id, "take"));
  });

  document.querySelectorAll(".miss-btn").forEach(btn => {
    btn.addEventListener("click", () => handleMedAction(btn.dataset.id, "missed"));
  });
}

function handleMedAction(medId, action) {
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
  // Ask permission + unlock audio after first click
  ensureNotificationPermission();

  document.addEventListener("click", () => {
    if (!notifySoundEl) return;
    notifySoundEl.play().then(() => {
      notifySoundEl.pause();
      notifySoundEl.currentTime = 0;
    }).catch(() => {});
  }, { once: true });

  // Load immediately and poll every 30 seconds
  loadDashboard();
  setInterval(loadDashboard, 30000);
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
