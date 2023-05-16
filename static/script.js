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
  let isJumping = false; // Track if the dog is currently jumping

  let dogPosition = {
    top: 0,
    left: 0,
  };

  function updateDogPosition() {
    dog.style.top = dogPosition.top + 'px';
    dog.style.left = dogPosition.left + 'px';
  }

  function jump() {
    if (isJumping) return;

    isJumping = true;

    let jumpInterval = setInterval(function() {
      if (bottom >= jumpHeight) {
        clearInterval(jumpInterval);

        let fallInterval = setInterval(function() {
          if (bottom <= 0) {
            clearInterval(fallInterval);
            bottom = 0;
            isJumping = false;
          } else {
            bottom -= 5;
            dog.style.bottom = bottom + 'px';
          }
        }, 20);
      } else {
        bottom += 5;
        dog.style.bottom = bottom + 'px';
      }
    }, 20);
  }

  document.addEventListener('keydown', function(event) {
    const stepSize = 15;
      if (event.key === 'ArrowUp') {
        dogPosition.top -= stepSize;
    } else if (event.key === 'ArrowDown') {
      dogPosition.top += stepSize;
    } else if (event.key === 'ArrowLeft') {
      dogPosition.left -= stepSize;
    } else if (event.key === 'ArrowRight') {
      dogPosition.left += stepSize;
    }

    updateDogPosition();
  });

  // Move the dog based on arrow button clicks
  document.querySelectorAll('.arrow-button').forEach(button => {
    button.addEventListener('click', function(event) {
      const direction = event.target.getAttribute('id');
      const stepSize = 15;

      if (direction === 'up') {
        dogPosition.top -= stepSize;
      } else if (direction === 'down') {
        dogPosition.top += stepSize;
      } else if (direction === 'left') {
        dogPosition.left -= stepSize;
      } else if (direction === 'right') {
        dogPosition.left += stepSize;
      }

      updateDogPosition();
    });
  });

  // Event listener for the jump function

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

