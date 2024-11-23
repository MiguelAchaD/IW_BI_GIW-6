let selectedPairs = [];
let selectedColor = 'black';

function selectModule(elementId, pair) {
  const element = document.querySelector(`.selectable[data-id="${elementId}"]`);
  if (!element) return;

  if (element.classList.contains('moduleSelected')) {
    element.classList.remove('moduleSelected');
    selectedPairs = selectedPairs.filter(item => item.element !== element);
    return;
  }

  const existingIndex = selectedPairs.findIndex(item => item.pair === pair);
  if (existingIndex !== -1) {
    selectedPairs[existingIndex].element.classList.remove('moduleSelected');
    selectedPairs.splice(existingIndex, 1);
  }

  element.classList.add('moduleSelected');
  selectedPairs.push({ element, pair });
}

function selectColor(color) {
  selectedColor = color;

  document.querySelectorAll('.circle').forEach(circle => {
    circle.classList.remove('selected');
  });
  document.querySelector(`.circle.${color}`).classList.add('selected');

  const deviceImage = document.getElementById('deviceImage');
  let currentSrc = deviceImage.getAttribute('src');

  currentSrc = currentSrc.replace(/\.(red|blue|black)\.png$/, '.png');
  currentSrc = currentSrc.replace(/\.png$/, '');

  const newSrc = `${currentSrc}.${color}.png`;

  deviceImage.src = newSrc;
}

function addToCart(product_name, product_type_id) {
  const moduleIds = selectedPairs.map(item => item.element.getAttribute('data-id'));

  const csrfToken = getCookie('csrftoken');

  $.ajax({
    type: "POST",
    url: "/addToCart/",
    data: JSON.stringify({ name: product_name, type_id: product_type_id, modules: moduleIds, color: selectedColor }),
    contentType: "application/json",
    dataType: "json",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    success: function (response) {
      console.log(response);
      showPopup('Producto añadido al carrito con éxito.', true);
    },
    error: function (xhr, status, error) {
      console.error("Error en la solicitud:", error);
      showPopup('Hubo un error al añadir el producto al carrito.', false);
    }
  });
}

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

function showPopup(message, isSuccess) {
  const popup = document.getElementById('popup');
  const popupContent = document.querySelector('.popup-content');
  const popupMessage = document.getElementById('popupMessage');
  popupMessage.textContent = message;

  const popupButtons = document.getElementById('popupButtons');
  if (isSuccess) {
    popupButtons.style.display = 'flex';
  } else {
    popupButtons.style.display = 'none';
  }

  popup.style.display = 'block';
}

function closePopup() {
  const popup = document.getElementById('popup');
  const popupContent = document.querySelector('.popup-content');

  popup.classList.add('hide');
  popupContent.classList.add('hide');

  popupContent.addEventListener('animationend', function handler() {
    popupContent.removeEventListener('animationend', handler);

    popup.style.display = 'none';

    popup.classList.remove('hide');
    popupContent.classList.remove('hide');
  });
}

function goToCart() {
  window.location.href = '/myCart/';
}

document.addEventListener('DOMContentLoaded', function () {
  selectColor(selectedColor);

  document.querySelectorAll('.selectable').forEach(el => {
    el.addEventListener('click', function () {
      const elementId = el.getAttribute('data-id');
      const pair = el.getAttribute('data-pair');
      selectModule(elementId, pair);
    });
  });

  const popup = document.getElementById('popup');
  window.addEventListener('click', function(event) {
    if (event.target == popup) {
      closePopup();
    }
  });
});
