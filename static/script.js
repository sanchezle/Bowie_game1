document.addEventListener('DOMContentLoaded', function() {
  // Your entire JavaScript code here


  const dog = document.getElementById('dog');
  const container = document.getElementById('container');
  const bgMusic = document.getElementById('bg-music');
  const muteButton = document.getElementById('mute-button');

  let time = 60;
  let score = 0;

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
      else if( keydown === 's' || keydown == 'S') {
        score += 1;
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
    if (time >= 0) {
        timeDisplay.textContent = `Time: ${time}`;
        time--;
        setTimeout(updateTimer, 1000);
    } else {
        timeDisplay.textContent = 'Time\'s up!';

        // Send user's score to the /update_score route
        sendScoreToFlask(score);

        // Send timer ended event to Flask
        fetch('/game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({timerEnded: true})
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
            console.error('Error sending timer ended event to Flask:', error);
        });
    }
}

  function resetGame() {
    time = 60;
    score = 0;
    updateTimer();
    document.getElementById('score-display').textContent = `Score: ${score}`;
  }

  document.getElementById('play-button').addEventListener('click', function() {
    resetGame();
  });

    function resetAnotherElement() {
      time = 60;
      score = 0;
      updateTimer();
      document.getElementById('elementID').textContent = `Score: ${score}`;
    }

  document.getElementById('another-reset-button').addEventListener('click', function() {
    resetAnotherElement();
  });

  updateTimer();

});