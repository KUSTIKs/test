const buttons = document.querySelectorAll(".btn");

buttons.forEach((btn) => {
  btn.addEventListener("click", function (e) {
    var rect = e.target.closest(".btn").getBoundingClientRect();
    console.log("rect", rect);
    let x = e.clientX - rect.left;
    console.log("x", x);
    console.log("rect.left", rect.left);
    console.log("e.clientX", e.clientX);
    let y = e.clientY - rect.top;
    console.log("y", y);
    console.log("rect.top", rect.top);
    console.log("e.clientY", e.clientY);
    console.log("\n===========================\n\n");

    const circle = document.createElement("span");

    circle.className = "circle";
    circle.style.left = x + "px";
    circle.style.top = y + "px";

    this.appendChild(circle);

    animationDuration =
      parseInt(getComputedStyle(circle).animationDuration) * 1000;

    setTimeout(() => {
      circle.remove();
    }, animationDuration);
  });
});
