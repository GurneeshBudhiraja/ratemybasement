const likeButton = document.querySelectorAll('.material-symbols-outlined');
let cross = document.querySelector('.cross');
let hamburgerMenu = document.querySelector('.hamburger-menu');
let menuButton = document.querySelector('.menu');
let crossClickable = false;
const sentences = ["Real Reviews for Real Renters.","Choose the Right Rental.","Choose Better with Renter Reviews.","Shape Our Community with Your Reviews."];
let typingElement = document.querySelector('#index-motto'); // typing effect div
const searchButton = document.querySelector('#index-search-review');
// index page elements
let searchButtonClicked = false; //to check whether button is clicked or not
const typingText = document.querySelector('#typing-text');
const onImage = document.querySelector('#on-image');
const onHouse = document.querySelector('#on-house');
// copy button
const copyDiv = document.querySelector(".copy-div");
const copyBtn = document.querySelector(".copy-btn");
const copyValue = document.querySelector(".copy-link");
const copyCross = document.querySelector(".copy-cross");
const copyAlert = document.querySelector(".link-copied");

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
// removing the menu 
cross.addEventListener('click',()=>{
  if (crossClickable) {
    hamburgerMenu.style.display = 'none';
    crossClickable=false;
  }
});


// typewriter effect
var typewriter = new Typewriter(typingElement, {
    loop: true,
    autoStart: true,
    delay:75
});
for (sentence of sentences) {
  typewriter.typeString(sentence)
      .pauseFor(150)
      .deleteAll()
      .start()
}

// for displaying the search bar
searchButton.addEventListener('click',()=> {
  if (!searchButtonClicked) {
    typingText.style.display='none';
    onImage.style.top='10%';
    onImage.style.left='5%';
    onHouse.style.display='flex';
    searchButton.style.border="0.1rem solid black";
    searchButtonClicked=true;
  } else {
    typingText.style.display='flex';
    onImage.style.top='25%';
    onImage.style.left='8%';
    searchButton.style.border="none";
    onHouse.style.display='none';
    searchButtonClicked=false;
  }
});
// copying elements on the clipboard
copyBtn.addEventListener('click',async ()=>{
  try {
    await navigator.clipboard.writeText(copyValue.value);
    copyAlert.style.display="flex";
  } catch (error) {
    console.log(error)
  }
})
//remove copy div
copyCross.addEventListener('click',()=>{
  copyDiv.style.display="none";
})
async function copyDivDisplay() {
  const showingDiv= await showCopyDiv(); //showing copy div
  const removingDiv = await removeCopyDiv(); // copy div
}
copyDivDisplay();
function showCopyDiv() {
  return new Promise((resolve)=>{
    setTimeout(() => {
      copyDiv.style.display="flex";
      resolve("display set to flex");
    }, 1000);
  });
}
function removeCopyDiv() {
  return new Promise((resolve)=>{

    setTimeout(() => {
        copyDiv.style.display="none";
        copyAlert.style.display="none";
      resolve("display set to none");
    }, 5000);
  });
}
