document.addEventListener('DOMContentLoaded', function() {
    const dog = document.getElementById('dog');
    const container = document.getElementById('container');
    const bgMusic = document.getElementById('bg-music');
    const muteButton = document.getElementById('mute-button');
    const scoreDisplay = document.getElementById('score');
    const timeDisplay = document.getElementById('time-display');
    const ball = document.getElementById('ball');
  
    let time = 60; // Set the initial time in seconds
    let score = 0; // Initialize the score variable
    let bottom = 0; // Initialize the bottom variable
    let gravity = 0.9; // Set the gravity variable
    let jumpHeight = 300; // Set the jump height variable
    let isJumping = false; // Track if the dog is currently jumpin





    function jump(){

        bottom +=30
        dog.style.bottom = bottom + 'px'
    }
    jump()
});

//assign functions to keycodes
function control(e){
    if(e.keyCode === 32){
        jump()
    }
}
document.addEventListener('keydown', control)