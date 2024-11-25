document.addEventListener("DOMContentLoaded", function () {
  let descriptionVisibility = {
    phone: true,
    tablet: false,
    laptop: false,
  };
  let phoneDescription = document.getElementById("phoneDescription");
  let tabletDescription = document.getElementById("tabletDescription");
  let laptopDescription = document.getElementById("laptopDescription");

  renderDescriptions(descriptionVisibility);

  document.addEventListener("click", function (event) {
    const closestElement = event.target.closest("[data-url]");
    if (closestElement) {
      const url = closestElement.getAttribute("data-url");
      window.location.href = url;
    }
  });

  function getPagePercentage() {
    let totalHeight = document.body.scrollHeight - window.innerHeight;
    let currentPosition = window.scrollY;

    if (totalHeight <= 0 || currentPosition <= 0) {
      return 0;
    }

    let percentage = (currentPosition / totalHeight) * 100;
    return percentage;
  }

  function renderDescriptions(descriptionVisibility) {
    if (descriptionVisibility.phone) {
      phoneDescription.classList.remove("invisible");
    } else {
      phoneDescription.classList.add("invisible");
    }

    if (descriptionVisibility.tablet) {
      tabletDescription.classList.remove("invisible");
    } else {
      tabletDescription.classList.add("invisible");
    }

    if (descriptionVisibility.laptop) {
      laptopDescription.classList.remove("invisible");
    } else {
      laptopDescription.classList.add("invisible");
    }
  }

  window.onscroll = function () {
    let currentScrollPercentage = getPagePercentage();
    if (currentScrollPercentage < 20) {
      descriptionVisibility.phone = true;
      descriptionVisibility.tablet = false;
      descriptionVisibility.laptop = false;
      renderDescriptions(descriptionVisibility);
    }

    if (currentScrollPercentage > 20 && currentScrollPercentage < 50) {
      descriptionVisibility.phone = false;
      descriptionVisibility.tablet = true;
      descriptionVisibility.laptop = false;
      renderDescriptions(descriptionVisibility);
    }

    if (currentScrollPercentage > 50) {
      descriptionVisibility.phone = false;
      descriptionVisibility.tablet = false;
      descriptionVisibility.laptop = true;
      renderDescriptions(descriptionVisibility);
    }
  };
});
