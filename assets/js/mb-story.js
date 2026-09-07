/* Machine Break · histoires animées au défilement (voir assets/css/mb-story.css).
 * - Ajoute html.mb-scroll (+ mb-native ou mb-js) selon le navigateur ; rien si « réduire les animations ».
 * - Pour chaque .mb-story : calcule la plage de défilement [a, b] où l'histoire se joue
 *   (desktop : pendant l'épinglage du bloc ; mobile : pendant l'épinglage de la machine à 12vh)
 *   et la publie en variables CSS (--mb-a / --mb-b) pour le mode natif, ou pilote les keyframes en mode script.
 * À charger dans <head> (synchrone, ~1 Ko) pour éviter un saut de mise en page. #mbjs dans l'URL force le mode script (test).
 */
(function () {
  var d = document.documentElement;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var native = !!(window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()')) && location.hash !== '#mbjs';
  d.classList.add('mb-scroll'); d.classList.add(native ? 'mb-native' : 'mb-js');

  function setup() {
    var stories = [].slice.call(document.querySelectorAll('.mb-story'));
    if (!stories.length) return;
    var items = stories.map(function (st) {
      return { el: st, col: st.querySelector('.mb-machine-col') || st, anim: [].slice.call(st.querySelectorAll('.mb-anim')), a: 0, b: 1 };
    });
    function range() {
      var vh = window.innerHeight, y = window.scrollY || window.pageYOffset;
      items.forEach(function (it) {
        if (window.innerWidth >= 992) { it.a = it.el.getBoundingClientRect().top + y; }
        else { it.a = it.col.getBoundingClientRect().top + y - 0.12 * vh; }
        it.b = it.a + 0.85 * vh;
        it.el.style.setProperty('--mb-a', Math.round(it.a) + 'px');
        it.el.style.setProperty('--mb-b', Math.round(it.b) + 'px');
      });
    }
    function update() {
      if (native) return;
      var y = window.scrollY || window.pageYOffset;
      items.forEach(function (it) {
        var p = (y - it.a) / (it.b - it.a); p = Math.max(0, Math.min(1, p));
        for (var i = 0; i < it.anim.length; i++) it.anim[i].style.animationDelay = (-p) + 's';
      });
    }
    range(); update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', function () { range(); update(); });
    window.addEventListener('load', function () { range(); update(); });
    window.__mbUpdate = update;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup); else setup();
})();
