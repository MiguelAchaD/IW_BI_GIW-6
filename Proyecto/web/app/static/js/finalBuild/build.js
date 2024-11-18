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

function addToCart(product_id) {
  const moduleIds = selectedPairs.map(item => item.element.getAttribute('data-id'));

  const csrfToken = getCookie('csrftoken');

  $.ajax({
    type: "POST",
    url: "/addToCart/",
    data: JSON.stringify({ product_id: product_id, modules: moduleIds, color: selectedColor }),
    contentType: "application/json",
    dataType: "json",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    success: function (response) {
      console.log(response);
      alert('Producto añadido al carrito con éxito.');
    },
    error: function (xhr, status, error) {
      console.error("Error en la solicitud:", error);
      alert('Hubo un error al añadir el producto al carrito.');
    }
  });
}

function getCookie(name) {
  // ... (sin cambios)
}

// Establecer el color predeterminado al cargar la página y asignar eventos
document.addEventListener('DOMContentLoaded', function () {
  selectColor(selectedColor);

  // Añadir event listeners a los elementos seleccionables
  document.querySelectorAll('.selectable').forEach(el => {
    el.addEventListener('click', function () {
      const elementId = el.getAttribute('data-id');
      const pair = el.getAttribute('data-pair');
      selectModule(elementId, pair);
    });
  });
});
