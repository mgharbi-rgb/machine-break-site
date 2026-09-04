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
      var icon = p.reseau === 'Instagram' ? 'fe-instagram' : 'fe-linkedin';
      return '<div class="col-12 col-md-4 d-flex">' +
        '<a class="card shadow-light-lg lift mb-6 mb-md-0 w-100" href="' + esc(p.url) + '" target="_blank" rel="noopener noreferrer">' +
          '<img src="' + esc(p.image) + '" class="card-img-top" alt="' + esc(p.texte) + '" loading="lazy">' +
          '<div class="card-body">' +
            '<p class="text-uppercase text-success font-weight-bold font-size-sm mb-2"><i class="fe ' + icon + ' mr-1"></i>' + esc(p.reseau) + (p.date ? ' · ' + esc(p.date) : '') + '</p>' +
            '<p class="text-muted mb-0">' + esc(p.texte) + '</p>' +
          '</div></a></div>';
    }).join('');
    section.hidden = false;
  }).catch(function () { /* section reste masquée */ });
})();
