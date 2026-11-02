const map = L.map('map', { zoomControl: true }).setView([61.5, 96], 3);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  subdomains: 'abcd', maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
}).addTo(map);

const labels = {
  info: 'Информация',
  warning: 'Предупреждение',
  all_clear: 'Отбой',
  unknown: 'Неизвестно'
};

async function loadData() {
  const [statusRes, eventsRes] = await Promise.all([
    fetch('/api/status'), fetch('/api/events')
  ]);
  const statuses = await statusRes.json();
  const events = await eventsRes.json();

  const statusList = document.getElementById('status-list');
  statusList.innerHTML = statuses.length ? statuses.map(x => `
    <article class="status-card">
      <div><div class="region">${escapeHtml(x.region)}</div>
      <div class="meta">${escapeHtml(x.title)}</div></div>
      <div class="status">${labels[x.status] || labels.unknown}</div>
    </article>`).join('') : '<div class="empty">Нет опубликованных региональных статусов.</div>';

  const eventList = document.getElementById('events');
  eventList.innerHTML = events.length ? events.map(x => `
    <article class="event-card">
      <div class="event-title">${escapeHtml(x.title)}</div>
      <div class="meta">${escapeHtml(x.region)} · ${escapeHtml(x.source)} · ${escapeHtml(x.published_at || '')}</div>
      ${x.source_url ? `<div class="meta"><a href="${safeUrl(x.source_url)}" target="_blank" rel="noopener">Открыть первоисточник ↗</a></div>` : ''}
    </article>`).join('') : '<div class="empty">Публикаций пока нет.</div>';
}
function escapeHtml(v){return String(v ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function safeUrl(v){try{const u=new URL(v);return ['https:'].includes(u.protocol)?u.href:'#'}catch{return '#'}}
loadData().catch(()=>{document.getElementById('status-list').textContent='Не удалось загрузить данные.'});
setInterval(()=>loadData().catch(()=>{}),60000);
