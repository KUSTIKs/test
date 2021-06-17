const swiper = new Swiper(".swiper-container", {
  keyboard: {
    enabled: true,
    onlyInViewport: true,
    pageUpDown: true,
  },
  slideToClickedSlide: true,
  slidesPerView: "auto",
  spaceBetween: 15,
  freeMode: true,
  watchOverflow: true,
});

const commentFieldToggles = [
  ...document.getElementsByClassName("comment-field-toggle"),
];
const btnAndField = [...commentFieldToggles].concat([
  ...document.getElementsByClassName("write-comment-wrapper"),
]);

commentFieldToggles.forEach((item) =>
  item.addEventListener("click", () => {
    if (btnAndField) {
      btnAndField.forEach((item) => item.classList.toggle("hidden"));
    }
  })
);

function showMoreLess(lessMore) {
  const moreLessText = [...document.getElementsByClassName(lessMore)];
  if (moreLessText) {
    moreLessText.forEach((item) => {
      const moreLessTextHeight = item.offsetHeight;
      const moreLessTextLineHeight = parseInt(
        getComputedStyle(item).lineHeight
      );
      const lines = moreLessTextHeight / moreLessTextLineHeight;
      if (lines > 4 || item.classList.contains("less")) {
        if (!item.nextElementSibling) {
          item.classList.add("less");
          let moreLessToggle = document.createElement("span");
          moreLessToggle.className = "more-less-toggle";
          moreLessToggle.innerHTML = "Show more";
          item.insertAdjacentElement("afterend", moreLessToggle);
        }
        // const toggle = [
        //   // ...item.parentElement.getElementsByClassName("more-less-toggle")
        // ];
        const toggle = item.nextElementSibling;
        toggle.addEventListener("click", () => {
          item.classList.toggle("less");
          toggle.innerHTML === "Show more"
            ? (toggle.innerHTML = "Show less")
            : (toggle.innerHTML = "Show more");
        });
      }
    });
  }
}

showMoreLess("less-more");

// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== "") {
//     const cookies = document.cookie.split(";");
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//       // Does this cookie string begin with the name we want?
//       if (cookie.substring(0, name.length + 1) === name + "=") {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }

// const csrftoken = getCookie("csrftoken");

loadMoreBtn = document.getElementById("load-more");

loadMoreBtn.addEventListener("click", function () {
  let commentsShown = document.querySelectorAll(".comment-wrapper").length;
  const params = { movieId: movieId, commentsShown: commentsShown };
  ajaxSend(loadMoreUrl, params);
});

function ajaxSend(url, params) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(params),
  })
    .then((response) => response.json())
    .then((json) => {
      json.comments.length ? render(json) : loadMoreBtn.classList.add("hidden");
    })
    .catch((error) => console.log(error));
}

function render(data) {
  if (data.isAllShown) {
    loadMoreBtn.classList.add("hidden");
  }
  let template = Hogan.compile(html);
  let output = template.render(data);

  const section = document.querySelector(".comments-list");
  section.innerHTML += output;
  showMoreLess("less-more");
}

const writeCommentForm = document.getElementById("write-comment");

if (user !== "AnonymousUser") {
  writeCommentForm.addEventListener("submit", (e) => {
    e.preventDefault();
    // grecaptcha.reset();
    // grecaptcha.execute();
    fields = [...e.target.getElementsByTagName("input")];
    var inputObject = {};
    fields.forEach(
      (item) => (inputObject[item.getAttribute("name")] = item.value)
    );

    if (inputObject.text.length) {
      const params = { ...inputObject };
      console.log(params);
      sendAjax(writeCommentUrl, params, csrftoken);
    }
  });
}

function sendAjax(url, params, csrftoken) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(params),
  })
    .then((response) => response.json())
    .then((json) => renderData(json))
    .catch((error) => console.error(error));
}
function renderData(data) {
  const template = Hogan.compile(html);
  const output = template.render(data);
  const section = document.querySelector(".comments-list");
  const commentElement = document.createElement("div");
  section.prepend(commentElement);
  commentElement.outerHTML = output;
  writeCommentForm
    .querySelectorAll("input.input")
    .forEach((item) => (item.value = ""));
}

let html =
  '\
  {{#comments}}\
    <div class="comment-wrapper">\
          <div class="image-wrapper">\
            <img\
              src="{{ profile.image }}"\
              alt="{{ profile.username }}"\
              class="user-avatar"\
            />\
          </div>\
          <div class="text-part">\
            <span class="user-username">{{ profile.username }}</span>\
            <p class="less-more comment-content">{{ text }}</p>\
          </div>\
        </div>\
  {{/comments}}';
