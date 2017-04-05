var menuButton = document.querySelector('.mobile-menu-button');

if (menuButton) {
  menuButton.addEventListener('click', function() {
    if (document.body.className === 'site') {
      document.body.className = 'site open';
    } else {
      document.body.className = 'site';
    }
  });
}
