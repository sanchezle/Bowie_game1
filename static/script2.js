document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('game-canvas');
  const container = document.getElementById('container');
  const context = canvas.getContext('2d');
  const bgMusic = document.getElementById('bg-music');
  const muteButton = document.getElementById('mute-button');
  const scoreDisplay = document.getElementById('score');
  const timeDisplay = document.getElementById('time-display');
  const elementsToMove = ['floor', 'dog', 'ball', 'left', 'up', 'down', 'right'];
  
  // Set canvas size to match background image
  const backgroundImage = new Image();
  backgroundImage.src = 'static/images/background.png';

  elementsToMove.forEach(elementId => {
    const element = document.getElementById(elementId);
    canvas.appendChild(element);
  });




  let time = 60; // Set the initial time in seconds
  let score = 0; // Initialize the score variable

  // Function to update the score
  function updateScore() {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
  }
  updateScore();

  // Function to update the timer
  function updateTimer() {
    timeDisplay.textContent = `Time: ${time}`;

    // Check if time is up
    if (time <= 0) {
      timesUp();
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
    console.log('Time is up!');
    // Perform actions when the time is up

    // Send the user's score to the /game route
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

  // Event listener for the mute button
  muteButton.addEventListener('click', function() {
    if (bgMusic.muted) {
      bgMusic.muted = false;
      muteButton.textContent = 'Mute';
    } else {
      bgMusic.muted = true;
      muteButton.textContent = 'Unmute';
    }
  });

  // Dog variables
  const dogWidth = 100;
  const dogHeight = 100;
  let dogX = canvas.width / 2 - dogWidth / 2;
  let dogY = canvas.height - dogHeight;
  let dogSpeed = 5;

  // Arrow button variables
  const arrowButtonSize = 50;

  // Function to draw the dog on the canvas
  function drawDog() {
    context.fillStyle = 'brown';
    context.fillRect(dogX, dogY, dogWidth, dogHeight);
  }

  // Function to handle keydown event
  function handleKeyDown(event) {
    if (event.key === 'ArrowLeft') {
      moveDogLeft();
    } else if (event.key === 'ArrowRight') {
      moveDogRight();
    }
  }

  // Function to handle keyup event
  function handleKeyUp(event) {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      stopDog();
    }
  }

  // Function to move the dog to the left
  function moveDogLeft() {
    dogX -= dogSpeed;
    if (dogX < 0) {
      dogX = 0;
    }
  }

});