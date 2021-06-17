const imagePreview = document.querySelectorAll(".image-preview");

imagePreview.forEach((item) => {
  const inputElement = item
    .closest(".input-item")
    .querySelector("input[type=file]");
  inputElement.addEventListener("change", function (event) {
    const imageLink = URL.createObjectURL(event.target.files[0]);
    item.setAttribute("src", imageLink);
  });
});

const inputs = [
  ...document.querySelectorAll(
    "input[type=text], input[type=password], input[type=email]"
  ),
];

inputs.forEach((item) => item.classList.add("input"));

// const fileTypes = [
//   "image/apng",
//   "image/bmp",
//   "image/gif",
//   "image/jpeg",
//   "image/pjpeg",
//   "image/png",
//   "image/svg+xml",
//   "image/tiff",
//   "image/webp",
//   "image/x-icon",
// ];

// function updatePreview() {
//   const file = inputPicture.files[0];
//   if (fileTypes.includes(file.type)) {
//     preview.setAttribute("src", URL.createObjectURL(file));
//   }
// }

// inputPicture.addEventListener("change", updatePreview);
