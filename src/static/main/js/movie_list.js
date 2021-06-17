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

const searchButton = document.getElementById("search-btn");
const movieInfoTextPart = [
  ...document.querySelectorAll(".movie-card .text-part"),
];

if (searchButton) {
  searchButton.addEventListener("click", () =>
    searchButton.parentElement.submit()
  );
}

if (movieInfoTextPart) {
  movieInfoTextPart.forEach((element) => {
    const width = element.offsetWidth - 10;
    [...element.children].forEach((element) => {
      element.style.width = width + "px";
    });
  });
}

const form = document.querySelector('form[name="filter"]');
const genreCards = form.querySelectorAll(".genre-card");
const genreInput = document.getElementById("genre-input");

genreCards.forEach((item) =>
  item.addEventListener("click", (e) => {
    e.preventDefault();
    selectedGenreCard = e.target.closest(".genre-card");
    genreCards.forEach((element) => element.classList.remove("selected"));
    selectedGenreCard.classList.add("selected");
    let url = form.action;
    genreInput.setAttribute(
      "value",
      [...selectedGenreCard.querySelectorAll(".genre-name")][0].innerHTML
    );
    let params = new URLSearchParams(new FormData(form)).toString();
    ajaxSend(url, params);
  })
);

function ajaxSend(url, params) {
  fetch(`${url}?${params}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
    .then((response) => response.json())
    .then((json) => render(json))
    .catch((error) => console.error(error));
}

function render(data) {
  let template = Hogan.compile(html);
  let output = template.render(data);
  const section = document.querySelector(".movie-cards-section");
  output
    ? (section.innerHTML = output)
    : (section.innerHTML = "<p class='nothing-found'>Nothing found</p>");
}

let html =
  '\
{{#movies}}\
  <a href="{{ url }}" class="movie-card">\
      <div class="image-wrapper">\
      <img src="{{ poster }}" alt="movie-poster" />\
      </div>\
      <div class="movie-info">\
      <div class="text-part">\
          <span class="movie-title">{{ title }}</span>\
          <span class="movie-genres">\
          {{# genres }}\
            {{ name }}\
          {{/ genres }}\
          </span>\
      </div>\
      <i class="bx bx-bookmark-alt save-btn"></i>\
      </div>\
  </a>\
{{/movies}}';
