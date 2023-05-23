document.addEventListener('DOMContentLoaded', function() {
  const dog = document.getElementById('dog');
  const container = document.getElementById('container');
  const bgMusic = document.getElementById('bg-music');
  const muteButton = document.getElementById('mute-button');
  const scoreDisplay = document.getElementById('score');
  const timeDisplay = document.getElementById('time-display');
  const ball = document.getElementById('ball');
  const arrowButtons = document.getElementById('arrow-buttons');
  const heightDisplay = document.getElementById('heightDisplay');
  const bark = document.getElementById('bark');


  let time = 60; // Set the initial time in seconds
  let score = 0; // Initialize the score variable
  let bottom = 0;
  // jump variables
  let gravity = 0.9;
  let isJumping = false;
  let currentHeight = 0;
  let maxHeight = 399;
  let heightTimerId;
  // slide variables
  let isGoingLeft = false;
  let isGoingRight = false;
  let left = 0;
  let leftTimerId;
  let rightTimerId;
  let movingTimerId;
  
  //update score function
  function updateScore() {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
  }
  
  // Update score function
  function updateScore() {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
  }


 //increase height function
   function increaseHeight() {

    //stops the interval when the currentHeight is equal to the maxHeight and current height stops increasing
    if (currentHeight >= maxHeight) {
      bark.play();
      currentHeight = maxHeight;
      clearInterval(heightTimerId);  
    } 
    // play bark.mp3 just once when the height reach 80% of the maxHeight;
  
      
    // Increase the height by 20px
    currentHeight += 20;

    // Update the height of the element with percentage value
    heightDisplay.style.height = currentHeight + 'px';
  
    // Update the height display
    heightDisplay.textContent = 'J U M P';
    
    return currentHeight; 
  }

  function keydownHandler(event) {
    if (event.keyCode === 32) { // Spacebar key code
      clearInterval(heightTimerId);
      heightTimerId = setInterval(increaseHeight, 20);
      console.log("intervalId: " + heightTimerId);  
    }
    
  }

  function keyupHandler(event) {
    if (event.keyCode === 32) {
       // Spacebar key code
      
      jump();
    }
  }
  document.addEventListener('keydown', keydownHandler);
  document.addEventListener('keyup', keyupHandler);
  
  // why does the height keeps increassing after the spacebar is released?
  // because the keydownHandler is still running
  // how to stop the keydownHandler?
  // use clearInterval to stop the interval
  // how to stop the interval?
  // where should i put the clearInterval?


  function jump() {
    clearInterval(heightTimerId); 
    // Clear the interval when jump is called
    // Your jump logic here;
    //
    if (isJumping) return;
    let timerId = setInterval(function () {
      if (bottom > currentHeight || bottom > 400) {
        clearInterval(timerId);
        let timerDownId = setInterval(function () {
          if (bottom < 0) {
            clearInterval(timerDownId);
            isJumping = false;
            currentHeight = 0;
          }
          bottom -= 10;
          dog.style.bottom = bottom + 'px';
          heightDisplay.style.height = bottom + 'px';
        }, 20);
      }
      isJumping = true;
      bottom += 50;
      bottom = bottom * gravity;
      console.log(bottom);
      dog.style.bottom = bottom + 'px';
    }, 20);
  }

 

  function slideLeft() {
    if (isGoingRight) {
      clearInterval(rightTimerId);
      isGoingRight = false;
    }
    if (left > -105) {
      clearInterval(movingTimerId); // Clear the previous moving timer
      isGoingLeft = true;
      movingTimerId = setInterval(function () {
      left -= 5;
      console.log('going left');
        if (left < -105) {
          left = -105;
        }
        dog.style.left = left + 'px';
      }, 20);
    }
    
  }
  
  function slideRight() {
    if (isGoingLeft) {
      clearInterval(leftTimerId);
      isGoingLeft = false;
    }
    if (left < 250) {
      clearInterval(movingTimerId); // Clear the previous moving timer
      isGoingRight = true;
      movingTimerId = setInterval(function () {
      left += 5;
      console.log('going right');
        if (left > 260) {
          left = 260;
        }
        dog.style.left = left + 'px';
      }, 20);
    }
  }
  
  function stopSliding() {
    console.log('stop sliding');
    clearInterval(movingTimerId); // Clear the current moving timer
    isGoingLeft = false;
    isGoingRight = false;
  }
  
  // Event listener for the jump function and the arrow keys
  function control(e) {
    if (e.keyCode === 37) {
      slideLeft(); // If you want to slide left
    } else if (e.keyCode === 39) {
      slideRight(); // If you want to slide right
    } else if (e.keyCode === 40) {
      stopSliding(); // If you want to stop sliding
    } else if (e.keyCode === 83) {
      console.log('s pressed');
      updateScore(); // If you want to add score
    }
  }
  document.addEventListener('keydown', control);
  
  document.querySelectorAll('.arrow-buttons').forEach(button => {
    button.addEventListener('pointerdown', (event) => {
      const direction = event.target.getAttribute('id');
      if (direction === "up") {
        clearInterval(heightTimerId);
        heightTimerId = setInterval(increaseHeight, 20);
        console.log("intervalId: " + heightTimerId);
      }
    });
  
    button.addEventListener('pointerup', (event) => {
      const direction = event.target.getAttribute('id');
      if (direction === "up") {
        jump();
      }
    });
  });
  // create a function for arrows to triger jump, slide left, slide right functions.
  document.querySelectorAll('.arrow-button').forEach(button => {
    button.addEventListener('click', function(event) {
      const direction = event.target.getAttribute('id');
    
        if (direction === "down") {
        
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

