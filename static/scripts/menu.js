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

var hamburger = document.querySelector(".hamburger");
hamburger.addEventListener("click", function() {
  hamburger.classList.toggle("is-active");
});
