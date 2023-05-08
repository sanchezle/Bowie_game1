document.addEventListener('DOMContentLoaded', function () {
    const dog = document.getElementById('dog');
    const ball = document.getElementById('ball');
    const startBtn = document.getElementById('start-btn');
    const restartBtn = document.getElementById('restart-btn');
    const muteBtn = document.getElementById('mute-btn');
    const timerElement = document.getElementById('timer');
    const gameOverElement = document.getElementById('game-over');
    const audio = document.getElementById('background-music');
    let timer;
  });


    function startGame() {
      dog.classList.remove('hidden');
      ball.classList.remove('hidden');
      dog.style.left = '0';
      dog.style.top = '0';
      moveBall();
      startBtn.classList.add('hidden');
      restartBtn.classList.remove('hidden');
      startTimer();
    }

    function restartGame() {
      timerElement.textContent = 60;
      gameOverElement.classList.add('hidden');
      startGame();
    }

    function startTimer() {
jbk      timer = setInterval(function ());
    }
// Add this code after the startTimer() function in script.js
function moveDog(e) {
    const dogRect = dog.getBoundingClientRect();
    const gameContainerRect = document.querySelector('.game-container').getBoundingClientRect();
    const stepSize = 10;
    switch (e.key) {
      case 'ArrowUp':
        if (dogRect.top > gameContainerRect.top) {
          dog.style.top = (parseInt(dog.style.top) - stepSize) + 'px';
        }
        break;
      case 'ArrowDown':
        if (dogRect.bottom < gameContainerRect.bottom) {
          dog.style.top = (parseInt(dog.style.top) + stepSize) + 'px';
        }
        break;
      case 'ArrowLeft':
        if (dogRect.left > gameContainerRect.left) {
          dog.style.left = (parseInt(dog.style.left) - stepSize) + 'px';
        }
        break;
      case 'ArrowRight':
        if (dogRect.right < gameContainerRect.right) {
          dog.style.left = (parseInt(dog.style.left) + stepSize) + 'px';
        }
        break;
    }
  }

  function toggleMute() {
    audio.muted = !audio.muted;
    muteBtn.textContent = audio.muted ? 'Unmute' : 'Mute';
  }

  document.addEventListener('keydown', moveDog);
  muteBtn.addEventListener('click', toggleMute);
  startBtn.addEventListener('click', startGame);
  restartBtn.addEventListener('click', restartGame);
