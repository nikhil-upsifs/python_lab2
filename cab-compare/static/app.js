// CabCompare front-end logic

const form = document.getElementById("trip-form");
const statusEl = document.getElementById("status");
const summaryEl = document.getElementById("summary");
const resultsEl = document.getElementById("results");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const pickup = document.getElementById("pickup").value.trim();
  const drop = document.getElementById("drop").value.trim();
  if (!pickup || !drop) return;

  setLoading(true);
  showStatus("Resolving locations and calculating distance…");

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pickup, drop }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong");
    render(data);
  } catch (err) {
    showError(err.message);
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  submitBtn.disabled = on;
  submitBtn.textContent = on ? "Comparing…" : "Compare Prices";
}

function showStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.classList.toggle("error", isError);
  statusEl.classList.remove("hidden");
  if (!isError) {
    summaryEl.classList.add("hidden");
    resultsEl.classList.add("hidden");
  }
}

function showError(msg) {
  showStatus(msg, true);
}

function render(data) {
  statusEl.classList.add("hidden");
  summaryEl.classList.remove("hidden");
  resultsEl.classList.remove("hidden");

  summaryEl.innerHTML = `
    <h2>Trip: ${escapeHtml(data.pickup_text)} → ${escapeHtml(data.drop_text)}</h2>
    <p>Distance ≈ ${data.distance_km} km · Estimated travel time ≈ ${data.route_duration_min} min</p>
    <p style="margin-top:8px">Cheapest overall: <strong class="cheapest">${escapeHtml(data.best.platform)}</strong>
    at ₹${data.best.price} <span style="color:var(--muted)">(lowest across all ride types — often a bike ride)</span></p>
  `;

  resultsEl.innerHTML = "";
  for (const [rideType, entries] of Object.entries(data.results)) {
    const block = document.createElement("div");
    block.className = "ride-type";
    const title = document.createElement("h3");
    title.textContent = rideType;
    block.appendChild(title);

    const cards = document.createElement("div");
    cards.className = "cards";
    for (const entry of entries) {
      cards.appendChild(cardHtml(entry));
    }
    block.appendChild(cards);
    resultsEl.appendChild(block);
  }
}

function cardHtml(entry) {
  const card = document.createElement("div");
  card.className = "card" + (entry.cheapest ? " cheapest" : "");
  card.innerHTML = `
    ${entry.cheapest ? '<span class="badge">CHEAPEST</span>' : ""}
    <div class="platform">${escapeHtml(entry.platform)}</div>
    <div class="ride-name">${escapeHtml(entry.name)}</div>
    <div class="price">${entry.price}</div>
    <div class="meta">
      ETA ≈ ${entry.eta_min} min
      ${entry.surge > 1 ? `<span class="surge"> · ${entry.surge}× surge</span>` : ""}
    </div>
  `;
  return card;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
