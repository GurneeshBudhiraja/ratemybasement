const likeButton = document.querySelectorAll('.material-symbols-outlined');
let cross = document.querySelector('.cross');
let hamburgerMenu = document.querySelector('.hamburger-menu')
let menuButton = document.querySelector('.menu')
let crossClickable= false;

// like button feature
for (const button of likeButton) {
  let buttonClicked = false;
  button.addEventListener('click',()=>{
    if (!buttonClicked) {
      button.style.setProperty('font-variation-settings',"'FILL' 1,'wght' 600,'GRAD' 0, 'opsz' 24");
      buttonClicked = true;
    } else {
      button.style.setProperty('font-variation-settings',"'FILL' 0,'wght' 600,'GRAD' 0, 'opsz' 24");
      buttonClicked=false;
    }
  });
}

// bringing the menu on the screen
menuButton.addEventListener('click',()=> {
  if (!crossClickable) {
    hamburgerMenu.style.display = 'flex';
    crossClickable=true;
  }
});

cross.addEventListener('click',()=>{
  if (crossClickable) {
    hamburgerMenu.style.display = 'none';
    crossClickable=false;
  }
});