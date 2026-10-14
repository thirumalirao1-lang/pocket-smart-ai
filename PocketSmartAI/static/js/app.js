const $ = (id) => document.getElementById(id);

document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    $(btn.dataset.tab).classList.add("active");
    $("status").innerHTML = "";
  });
});

let roomCount = 0;

function addRoom() {
  roomCount++;
  const wrapper = document.createElement("div");
  wrapper.className = "room";
  wrapper.dataset.room = roomCount;
  wrapper.innerHTML = `
    <div class="room-title">
      <input class="room-name" placeholder="Room name (e.g. Living Room)" required>
      <button type="button" class="remove" onclick="this.closest('.room').remove()">Remove</button>
    </div>
    <input class="room-items" placeholder="Items, comma separated (e.g. sofa, TV unit, curtains)">
  `;
  $("rooms").appendChild(wrapper);
}
window.addRoom = addRoom;
$("addRoom").addEventListener("click", addRoom);
addRoom();

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}

function safeUrl(value) {
  try {
    const u = new URL(value);
    return ["http:", "https:"].includes(u.protocol) ? u.href : "#";
  } catch { return "#"; }
}

function showStatus(message, error=false) {
  $("status").innerHTML = `<div class="${error ? "alert error" : "alert"}">${esc(message)}</div>`;
}

function renderResult(data) {
  $("results").classList.remove("hidden");
  $("resultTitle").textContent = data.planner;
  $("aiBadge").textContent = data.ai_powered ? "AI Powered" : "Demo / Mock Mode";

  $("allocation").innerHTML = Object.entries(data.allocation || {}).map(([key, value]) => `
    <div class="allocation-item">
      <span>${esc(key.replaceAll("_"," "))}</span>
      <strong>₹${Number(value).toLocaleString("en-IN")}</strong>
    </div>
  `).join("");

  $("recommendations").innerHTML = (data.recommendations || []).map(item => `
    <article class="recommendation">
      <div>
        <h4>${esc(item.name)}</h4>
        <p>${esc(item.category)} • ${esc(item.platform)}</p>
        <p>${esc(item.reason)}</p>
      </div>
      <div class="price">₹${Number(item.estimated_price || 0).toLocaleString("en-IN")}</div>
      ${safeUrl(item.url) !== "#" ? `<a target="_blank" rel="noopener" href="${safeUrl(item.url)}">View</a>` : ""}
    </article>
  `).join("");

  $("notes").innerHTML = (data.notes || []).map(n => `<li>${esc(n)}</li>`).join("");
  $("results").scrollIntoView({behavior:"smooth"});
}

async function postJSON(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(body)
  });
  const json = await res.json();
  if (!res.ok || !json.success) throw new Error(json.error || "Request failed");
  return json.data;
}

$("homeForm").addEventListener("submit", async e => {
  e.preventDefault();
  showStatus("Generating home plan...");
  const rooms = [...document.querySelectorAll(".room")].map(r => ({
    name: r.querySelector(".room-name").value.trim(),
    items: r.querySelector(".room-items").value.split(",").map(x => x.trim()).filter(Boolean)
  })).filter(r => r.name);

  try {
    renderResult(await postJSON("/api/generate-home", {
      budget: $("homeBudget").value, rooms
    }));
    showStatus("Home plan generated successfully.");
  } catch (err) { showStatus(err.message, true); }
});

$("partyForm").addEventListener("submit", async e => {
  e.preventDefault();
  showStatus("Generating party plan...");
  try {
    renderResult(await postJSON("/api/generate-party", {
      budget: $("partyBudget").value,
      guests: $("guests").value,
      event_type: $("eventType").value,
      venue: $("venue").value
    }));
    showStatus("Party plan generated successfully.");
  } catch (err) { showStatus(err.message, true); }
});

$("jewelryForm").addEventListener("submit", async e => {
  e.preventDefault();
  showStatus("Generating jewelry plan...");
  const fd = new FormData();
  fd.append("budget", $("jewelryBudget").value);
  fd.append("occasion", $("occasion").value);
  fd.append("style", $("style").value);
  if ($("outfitImage").files[0]) fd.append("outfit_image", $("outfitImage").files[0]);

  try {
    const res = await fetch("/api/generate-jewelry", {method:"POST", body:fd});
    const json = await res.json();
    if (!res.ok || !json.success) throw new Error(json.error || "Request failed");
    renderResult(json.data);
    showStatus("Jewelry plan generated successfully.");
  } catch (err) { showStatus(err.message, true); }
});
