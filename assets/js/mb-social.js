/* Section « Sur les réseaux » : lit /social.json (édité dans /admin/) et affiche jusqu'à 3 cartes. Aucune dépendance, aucun script tiers. */
(function () {
  'use strict';
  var section = document.getElementById('reseaux');
  var grid = document.getElementById('reseaux-cartes');
  if (!section || !grid || !window.fetch) return;
  function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  fetch('/social.json', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
    var posts = (data && data.posts) ? data.posts.filter(function (p) { return p && p.url && p.image; }).slice(0, 3) : [];
    if (!posts.length) return;
    grid.innerHTML = posts.map(function (p) {
      return '<a href="' + esc(p.url) + '" target="_blank" rel="noopener noreferrer">' +
        '<img src="' + esc(p.image) + '" alt="' + esc(p.texte) + '" loading="lazy">' +
        '<div><span class="k">' + esc(p.reseau) + (p.date ? ' · ' + esc(p.date) : '') + '</span><p>' + esc(p.texte) + '</p></div></a>';
    }).join('');
    section.hidden = false;
  }).catch(function () { /* section reste masquée */ });
})();
