document.addEventListener("DOMContentLoaded", function () {
  const maxFrames = 100;
  let frame = 0;
  const imageElements = document.querySelectorAll(".animation-section img");

  function updateImages(frame) {
    if (frame <= 0) {
      return;
    }
    const paddedFrame = frame.toString().padStart(4, "0");
    imageElements.forEach((img) => {
      const basePath = img.src.split("/").slice(0, -1).join("/");
      img.src = `${basePath}/${paddedFrame}.png`;
    });
  }

  function preventDefault(e) {
    e.preventDefault();
  }

  var keys = { 37: 1, 38: 1, 39: 1, 40: 1 };

  function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
      preventDefault(e);
      return false;
    }
  }

  var supportsPassive = false;
  try {
    window.addEventListener(
      "test",
      null,
      Object.defineProperty({}, "passive", {
        get: function () {
          supportsPassive = true;
        },
      })
    );
  } catch (e) {}

  var wheelOpt = supportsPassive ? { passive: false } : false;
  var wheelEvent =
    "onwheel" in document.createElement("div") ? "wheel" : "mousewheel";

  function disableScroll() {
    window.addEventListener("DOMMouseScroll", preventDefault, false);
    window.addEventListener(wheelEvent, preventDefault, wheelOpt);
    window.addEventListener("touchmove", preventDefault, wheelOpt);
    window.addEventListener("keydown", preventDefaultForScrollKeys, false);
  }

  function enableScroll() {
    window.removeEventListener("DOMMouseScroll", preventDefault, false);
    window.removeEventListener(wheelEvent, preventDefault, wheelOpt);
    window.removeEventListener("touchmove", preventDefault, wheelOpt);
    window.removeEventListener("keydown", preventDefaultForScrollKeys, false);
  }

  function handleWheel(event) {
    let delta = event.deltaY || event.detail || event.wheelDelta;

    if (delta > 0) {
      console.log("Desplazamiento hacia abajo");
      if (frame < maxFrames) {
        frame++;
        updateImages(frame);
      }
    } else if (delta < 0) {
      console.log("Desplazamiento hacia arriba");
      if (frame > 0) {
        frame--;
        updateImages(frame);
      }
    }
  }

  window.addEventListener(wheelEvent, (e) => {
    if (frame < maxFrames) {
      disableScroll();
      handleWheel(e);
    } else {
      enableScroll();
    }
  });

  window.addEventListener("touchmove", (e) => {
    if (frame < maxFrames) {
      disableScroll();
      handleWheel(e);
    } else {
      enableScroll();
    }
  });
});
