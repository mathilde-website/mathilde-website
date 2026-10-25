document.addEventListener("DOMContentLoaded", function () {
  var burger = document.getElementById("burger");
  var menu = document.querySelector(".menu");
  function toggleMobileMenu(open) {
    let lines = burger.querySelectorAll(".burger-line");
    if (open) {
      burger.dataset["open"] = "true";
      lines[0].classList.add("rotate-45");
      lines[0].classList.remove("-translate-y-1.5");
      lines[1].classList.add("opacity-0");
      lines[2].classList.add("-rotate-45");
      lines[2].classList.remove("translate-y-1.5");
      menu.classList.remove("hidden");
    } else {
      burger.dataset["open"] = "false";
      lines[0].classList.remove("rotate-45");
      lines[0].classList.add("-translate-y-1.5");
      lines[1].classList.remove("opacity-0");
      lines[2].classList.remove("-rotate-45");
      lines[2].classList.add("translate-y-1.5");
      menu.classList.add("hidden");
    }
  }
  toggleMobileMenu(false)
  burger.getElementsByTagName("button")[0].addEventListener(
    "click", () => {
      toggleMobileMenu(burger.dataset["open"] === "false");
    }
  );
  menu.querySelectorAll("a").forEach(element => {
    element.addEventListener("click", () => { toggleMobileMenu(false) });
  });

  window.addEventListener("hashchange", function () {
    window.scrollTo(window.scrollX, window.scrollY - 100);
  });

  document.querySelectorAll('a[href="mailto:"]').forEach((element) => {
    var sourceElement = document.getElementById("email");
    var email = sourceElement.dataset.email + "@" + sourceElement.dataset.domain;
    element.href = "mailto:" + email;
    element.innerHTML = email;
  })

});
