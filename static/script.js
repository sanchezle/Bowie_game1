document.addEventListener('DOMContentLoaded', function() {
  // Your entire JavaScript code here
  const dog = document.getElementById('dog');
  const container = document.getElementById('container');
  const bgMusic = document.getElementById('bg-music');
  const muteButton = document.getElementById('mute-button');
  const scoreDisplay = document.getElementById('score');
  const timeDisplay = document.getElementById('time-display');

  let time = 60; // Set the initial time in seconds
  let score = 0; // Initialize the score variable


  let dogPosition = {
      top: 0,
      left: 0,
  };

  function updateDogPosition() {
      dog.style.top = dogPosition.top + 'px';
      dog.style.left = dogPosition.left + 'px';
  }


  document.addEventListener('keydown', function(event) {
    const stepSize = 10;

    if (event.key === 'ArrowUp') {
        dogPosition.top -= stepSize;
    } else if (event.key === 'ArrowDown') {
        dogPosition.top += stepSize;
    } else if (event.key === 'ArrowLeft') {
        dogPosition.left -= stepSize;
    } else if (event.key === 'ArrowRight') {
        dogPosition.left += stepSize;
    }
    else if (event.key === 's' || event.key === 'S') {
      score += 1;
      scoreDisplay.textContent = `Score: ${score}`;
    }
   
    updateDogPosition();
  });


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
  }
});