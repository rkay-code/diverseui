var banner = document.querySelector('.banner');
var closeBtn = document.querySelector('.close-banner');

if (closeBtn && banner) {
  closeBtn.addEventListener('click', function() {
    if (banner.className.indexOf('remember-close') > -1) {
      document.cookie = 'dismissed=true';
    }

    banner.parentNode.removeChild(banner);
  });
}
