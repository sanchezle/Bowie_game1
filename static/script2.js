document.addEventListener('DOMContentLoaded', function() {
   const dog = document.getElementById('dog');

    let bottom = 10;
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
      if(bottom > 300){
      clearInterval(timerId)
        let timerDownId = setInterval(function(){
          if(bottom < 10){
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
      if (isGoingRight){
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
      isGoingLeft = false;
      isGoingRight = false;
      clearInterval(leftTimerId);
      clearInterval(rightTimerId);
   }
//why stopSliding() is not working at some point?
//a:

   function control(e){
        if(e.keyCode === 40){
        stopSliding();//if you want to stop sliding
      } else if(e.keyCode === 32){
          jump();
      } else if(e.keyCode === 37){
          slideLeft();//if you want to slide left
      } else if(e.keyCode === 39){
          slideRight();//if you want to slide right
      } 
   }
  document.addEventListener('keydown', control);

  });
  
   