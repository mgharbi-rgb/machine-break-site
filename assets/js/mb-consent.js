/*
 * Machine Break — consentement cookies + mesure d'audience (GA4, Google Ads).
 * Aucune dépendance. Rien n'est chargé ni déposé avant le consentement (CNIL / RGPD).
 *
 * Événements envoyés à GA4 après consentement :
 *   - page_view (automatique)
 *   - generate_lead        : affichage de /merci (envoi du formulaire), + conversion Google Ads
 *   - tel_click            : clic sur un lien tel:
 *   - cta_diagnostic_click : clic sur le CTA « Mon diagnostic pause en 1 minute »
 *
 * Pour rouvrir le bandeau : un lien avec la classe .js-cookie-settings (pied de page).
 */
(function () {
  'use strict';

  var CONFIG = {
    ga4Id: 'G-YK9MDPBNX3',             // GA4 (fourni par le client le 2026-09-04)
    adsId: 'AW-10786145165',           // tag Google Ads déjà en place sur le site
    adsLeadLabel: '7cy0COidpO0aEI2Hnpco', // conversion Ads « Form rempli » (déplacée de /contact vers /merci)
    storageKey: 'mb_consent',
    validityDays: 180,                 // durée de validité du choix (la CNIL impose 13 mois maximum)
    policyUrl: '/politique-de-confidentialite'
  };

  var loaded = false;

  /* ---------------------------------------------------------------- stockage */
  function readConsent() {
    try {
      var raw = window.localStorage.getItem(CONFIG.storageKey);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.status || !c.at) return null;
      if (Date.now() - c.at > CONFIG.validityDays * 86400000) return null;
      return c.status; // 'granted' | 'denied'
    } catch (e) { return null; }
  }
  function saveConsent(status) {
    try { window.localStorage.setItem(CONFIG.storageKey, JSON.stringify({ status: status, at: Date.now() })); } catch (e) { /* stockage indisponible */ }
  }

  /* ---------------------------------------------------------------- gtag */
  function gtag() { window.dataLayer.push(arguments); }

  function loadGtag() {
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || gtag;
    window.gtag('consent', 'default', {
      ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted', analytics_storage: 'granted'
    });
    window.gtag('js', new Date());
    var primary = CONFIG.ga4Id || CONFIG.adsId;
    if (!primary) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(primary);
    document.head.appendChild(s);
    if (CONFIG.ga4Id) window.gtag('config', CONFIG.ga4Id);
    if (CONFIG.adsId) window.gtag('config', CONFIG.adsId);
    trackConversionPage();
  }

  function track(name, params) {
    if (!loaded || typeof window.gtag !== 'function') return;
    window.gtag('event', name, params || {});
  }

  function trackConversionPage() {
    var path = window.location.pathname.replace(/\/+$/, '');
    if (path === '/merci' || path === '/merci.html') {
      track('generate_lead', { method: 'formulaire_contact' });
      if (CONFIG.adsId && CONFIG.adsLeadLabel) {
        window.gtag('event', 'conversion', { send_to: CONFIG.adsId + '/' + CONFIG.adsLeadLabel, value: 1.0, currency: 'EUR' });
      }
    }
  }

  /* ---------------------------------------------------------------- événements */
  function closest(el, selector) {
    while (el && el.nodeType === 1) {
      if (el.matches ? el.matches(selector) : false) return el;
      el = el.parentNode;
    }
    return null;
  }

  document.addEventListener('click', function (e) {
    var a = closest(e.target, 'a');
    if (!a) return;
    if (closest(e.target, '.js-cookie-settings')) {
      e.preventDefault();
      showBanner();
      return;
    }
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) {
      track('tel_click', { link_url: href, page_location: window.location.href });
    }
    if (a.classList.contains('cta-diagnostic')) {
      track('cta_diagnostic_click', { link_text: (a.textContent || '').trim(), page_location: window.location.href });
    }
  }, true);

  /* ---------------------------------------------------------------- bandeau */
  function showBanner() {
    if (document.getElementById('mb-cookie-banner')) return;
    var b = document.createElement('div');
    b.id = 'mb-cookie-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-live', 'polite');
    b.setAttribute('aria-label', 'Gestion des cookies');
    b.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:1080;background:#161c2d;color:#fff;padding:1rem 1.25rem;box-shadow:0 -0.5rem 1.5rem rgba(22,28,45,.25);font-size:.9375rem;line-height:1.5;';
    b.innerHTML =
      '<div style="max-width:1140px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1.5rem;">' +
        '<p style="flex:1 1 320px;margin:0;">Ce site utilise des cookies de mesure d’audience (Google Analytics) et de suivi publicitaire (Google Ads) <strong>uniquement avec votre accord</strong>. ' +
        'Aucun cookie non essentiel n’est déposé avant votre choix. ' +
        '<a href="' + CONFIG.policyUrl + '" style="color:#fff;text-decoration:underline;">En savoir plus</a></p>' +
        '<div style="display:flex;gap:.5rem;flex-wrap:wrap;">' +
          '<button type="button" id="mb-cookie-deny" class="btn btn-sm btn-outline-light">Refuser</button>' +
          '<button type="button" id="mb-cookie-accept" class="btn btn-sm btn-success">Accepter</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(b);
    document.getElementById('mb-cookie-accept').addEventListener('click', function () { saveConsent('granted'); hideBanner(); loadGtag(); });
    document.getElementById('mb-cookie-deny').addEventListener('click', function () { saveConsent('denied'); hideBanner(); });
  }
  function hideBanner() {
    var b = document.getElementById('mb-cookie-banner');
    if (b && b.parentNode) b.parentNode.removeChild(b);
  }

  /* ---------------------------------------------------------------- init */
  function init() {
    var status = readConsent();
    if (status === 'granted') loadGtag();
    else if (status === null) showBanner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
