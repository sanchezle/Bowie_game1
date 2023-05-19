document.addEventListener('DOMContentLoaded', function() {
  const dog = document.getElementById('dog');
  const container = document.getElementById('container');
  const bgMusic = document.getElementById('bg-music');
  const muteButton = document.getElementById('mute-button');
  const scoreDisplay = document.getElementById('score');
  const timeDisplay = document.getElementById('time-display');
  const ball = document.getElementById('ball');
  const arrowButtons = document.getElementById('arrow-buttons');



  let time = 60; // Set the initial time in seconds
  let score = 0; // Initialize the score variable
  let bottom = 0;
  let gravity = 0.9;
  let isJumping = false;
  let isGoingLeft = false;
  let isGoingRight = false;
  let left = 0;
  let leftTimerId;
  let rightTimerId;


  function jump(){
    if(isJumping) return;
    let timerId =setInterval(function(){
      if(bottom > 400){
      clearInterval(timerId)
        let timerDownId = setInterval(function(){
          if(bottom < 0){
            clearInterval(timerDownId)
            isJumping = false;
          }
          bottom -= 10
          dog.style.bottom = bottom + 'px';
        }, 20);
      }
      isJumping = true;
      bottom += 50;
      bottom = bottom * gravity;
      console.log(bottom)
      dog.style.bottom = bottom + 'px';
      }, 20);
  }
 
  function slideLeft(){
      if (isGoingRight) {
        clearInterval(rightTimerId);
        isGoingRight = false;
      }
      isGoingLeft = true;
      leftTimerId = setInterval(function(){
        left -= 5; 
        console.log('going left')
        dog.style.left = left + 'px';
      }, 20);
  }

  function slideRight(){
      if (isGoingLeft) {
        clearInterval(leftTimerId);
        isGoingLeft = false;
      }
      isGoingRight = true;
      rightTimerId = setInterval(function(){
        left += 5;
        console.log('going right')
        dog.style.left = left + 'px';
      }, 20);
  }

  function stopSliding(){
      console.log('stop sliding')
      clearInterval(leftTimerId);
      clearInterval(rightTimerId);
      isGoingLeft = false;
      isGoingRight = false;
  }

  function control(e){
      if(e.keyCode === 32){
        jump();
    } else if(e.keyCode === 37){
        slideLeft();//if you want to slide left
    } else if(e.keyCode === 39){
        slideRight();//if you want to slide right
    } else if(e.keyCode === 40){
      stopSliding();//if you want to stop sliding
    }
  }
  document.addEventListener('keydown', control);
  // Event listener for the jump function
  // create a function for arrows to triger jump, slide left, slide right functions.
  document.querySelectorAll('.arrow-button').forEach(button => {
    button.addEventListener('click', function(event) {
      const direction = event.target.getAttribute('id');
    
        if (direction === "up") {
        // call the jump function when the up arrow is clicked
        jump(); 
      } else if (direction === "down") {
        
          stopSliding();

      } else if (direction === "left") {
          
          slideLeft();

      } else if (direction === "right") {
        
          slideRight();
      }
    });
  });

  // Rest of your code...
 //q: why the arrow buttons are not working?
  //a: because the arrow buttons are not in the container div
  //q: why the dog is not moving?
  //a: because the dogPosition is not updated
  //q: why the dog is not moving when the arrow buttons are clicked?  
  //a: because the arrow buttons are not in the container div
  //q: which cointainer div?

  bgMusic.volume = 0.5; // Set the volume of the background music (0 to 1)

  muteButton.addEventListener('click', function() {
    if (bgMusic.muted) {
      bgMusic.muted = false;
      muteButton.textContent = 'Mute';
    } else {
      bgMusic.muted = true;
      muteButton.textContent = 'Unmute';
      }
  });
    // q: why do the arrows button not work?
    // a: because the arrow buttons are not in the container div

  //CHECK
  //create a score counter that adds 1 every time the dog is clicked"

  function sendScoreToFlask(score) {
    fetch('/update_score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({score: score})
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Score sent to Flask:', data);
    })
    .catch(error => {
      console.error('Error sending score to Flask:', error);
    });
  }


  function updateTimer() {
    timeDisplay.textContent = `Time: ${time}`;

    // Check if time is up
    if (time <= 0) {
      //timesUp();
      return;
    }

    // Decrease time by 1 second
    time--;

    // Call the updateTimer function again after 1 second
    setTimeout(updateTimer, 1000);
  }

  // Call the updateTimer function to start the countdown
  updateTimer();

  // Function to handle when time is up
  function timesUp() {
    // Perform actions when the time is up

    console.log('Time is up!');
    // Add your desired code here
      // Send user's score to the /game route
  fetch('/game', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ score: score })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.redirect) {
        // Redirect the user to the index page
        window.location.href = data.redirect;
      }
    })
    .catch(error => {
      console.error('Error sending score to Flask:', error);
    });
  }


});

