const stars = document.querySelectorAll(".rt-btn");
const form = document.getElementById("rate-form");
const csrf = getCookie('csrftoken');
let score = 0;
let movie = null;
stars.forEach(star => {
  star.addEventListener("mouseover", function () {
    const value = this.getAttribute("data-value");
    for (let i = 0; i < stars.length; i++) {
      if (i < value) {
        stars[i].classList.add("filled");
      } else {
        stars[i].classList.remove("filled");
      }
    }
  });

  star.addEventListener("mouseout", function () {
    for (let i = 0; i < stars.length; i++) {
      if (i < score) {
        stars[i].classList.add("filled");
      } else {
        stars[i].classList.remove("filled");
      }
    }
  });

  star.addEventListener("click", function () {
    score = this.getAttribute("data-value");
  });
});


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function openPopup(movie, rating) {
  mov_id = movie;
  score = rating;
  for (let i = 0; i < stars.length; i++) {
    if (i < score) {
      stars[i].classList.add("filled");
    } else {
      stars[i].classList.remove("filled");
    }
  }
  document.getElementById("ratingPopup").style.display = "block";
  document.getElementById("popupOverlay").style.display = "block";
}

function closePopup() {
  console.log(mov_id, score)
  document.getElementById("ratingPopup").style.display = "none";
  document.getElementById("popupOverlay").style.display = "none";
  // score = 0;
}


function submitRating() {
  console.log(score, mov_id)
  if (score==0){
    showError(message="The minimum score is 1 star")
  }
  else{
    $.ajax({
      type: 'POST',
      url: '/rate-movie',
      data: {
          'csrfmiddlewaretoken': csrf,
          'mov_id': mov_id,
          'score': score,
      },
      success: function(response){
          console.log(response)
          console.log("movie_text-" + mov_id)
          document.getElementById("movie_text-" + mov_id).textContent= " " + score;
      },
      error: function(error){
          console.log(error)
      }
    })
    closePopup();
  }
}

function toggleWatchLater(movieId) {
  const icon = document.getElementById(`watch_later_icon-${movieId}`);
  const isWatchingLater = icon.style.color === 'gold';

  // Send AJAX request to toggle "Watch Later" status
  $.ajax({
      type: 'POST',
      url: '/watch-later',
      data: {
          'csrfmiddlewaretoken': csrf,
          'mov_id': movieId,
      },
      success: function(response){
          if (response.success === "true") {
              // Toggle the color
              icon.style.color = isWatchingLater ? 'gray' : 'gold';
              console.log(`Toggled movie ID ${movieId}. Now watching later: ${!isWatchingLater}`);
          } else {
              console.log('Failed to toggle Watch Later status');
          }
      },
      error: function(error){
          console.log('Error:', error);
      }
  });
}

function redir_register() {
  window.location.href = "/signup";
}

function showError(message, duration = 10000) {
  const errorPopup = document.getElementById("errorPopup");
  const errorMessage = document.getElementById("errorMessage");

  errorMessage.textContent = message;

  errorPopup.style.display = "block";

  setTimeout(() => {
    errorPopup.style.display = "none";
  }, duration);
}






