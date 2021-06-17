function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

const updateSavedBtns = [...document.getElementsByClassName("update-saved")];

updateSavedBtns.forEach((item) =>
  item.addEventListener("click", function () {
    var movieId = this.dataset.movie;
    var action = this.dataset.action;
    console.log("movieId", movieId);
    console.log("action", action);
    if (user === "AnonymousUser") {
      console.log("user is not authenticated");
    } else {
      updateSaved(movieId, action, item);
    }
  })
);

function updateSaved(movieId, action, item) {
  var url = "/update-saved/";

  fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ movieId: movieId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      updateIcon(item, data);
      console.log("data:", data);
    })
    .catch((error) => console.error(error));
}

function updateIcon(icon, response) {
  action = response.response_action;
  if (action === "added") {
    icon.classList.remove("bx-bookmark-alt");
    icon.classList.add("bxs-bookmark-alt");
  } else {
    icon.classList.remove("bxs-bookmark-alt");
    icon.classList.add("bx-bookmark-alt");
  }
}
