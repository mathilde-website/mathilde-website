document.addEventListener("DOMContentLoaded", function() {
  var mapData = JSON.parse(document.getElementById("map-data").innerText);

  var map = L.map(
    'map',
    {scrollWheelZoom: false}
  ).setView(mapData.init, mapData.initZoom);

  map.on('focus', function() { console.log("focus"); map.scrollWheelZoom.enable(); });
  map.on('blur', function() { console.log("blur"); map.scrollWheelZoom.disable(); });

  L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 15,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: mapData.token
  }).addTo(map);
  L.circle(mapData.center, mapData.radius).addTo(map);

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
    "click", ()=>{
      toggleMobileMenu(burger.dataset["open"] === "false");
      }
  );
  menu.querySelectorAll("a").forEach(element => {
    element.addEventListener("click", ()=>{toggleMobileMenu(false)});
  });

  window.addEventListener("hashchange", function () {
    window.scrollTo(window.scrollX, window.scrollY - 100);
  });
  
  document.querySelectorAll('a[href="mailto:"]').forEach((element) => {
    // what's displayed
    var email = element.innerHTML + "@" + document.querySelector("body").dataset.emailDomain
    element.href = "mailto:" + email;
    element.innerHTML = email;
  })

});
