let selectedPairs = [];
let selectedColor = 'black'; // Color predeterminado

function selectModule(elementId, pair) {
  const element = document.querySelector(`.selectable[data-id="${elementId}"]`);
  if (!element) return;

  // Si el módulo ya está seleccionado, lo deseleccionamos y lo eliminamos de selectedPairs
  if (element.classList.contains('moduleSelected')) {
    element.classList.remove('moduleSelected');
    selectedPairs = selectedPairs.filter(item => item.element !== element);
    return;
  }

  // Verificar si hay otro módulo seleccionado del mismo par
  const existingIndex = selectedPairs.findIndex(item => item.pair === pair);
  if (existingIndex !== -1) {
    // Deseleccionar el módulo previamente seleccionado del mismo par
    selectedPairs[existingIndex].element.classList.remove('moduleSelected');
    selectedPairs.splice(existingIndex, 1);
  }

  // Seleccionar el nuevo módulo
  element.classList.add('moduleSelected');
  selectedPairs.push({ element, pair });
}

function selectColor(color) {
  selectedColor = color;

  // Actualizar la selección visual
  document.querySelectorAll('.circle').forEach(circle => {
    circle.classList.remove('selected');
  });
  document.querySelector(`.circle.${color}`).classList.add('selected');

  // Actualizar la imagen del dispositivo según el color seleccionado
  const deviceImage = document.getElementById('deviceImage');
  let currentSrc = deviceImage.getAttribute('src');

  // Remover cualquier extensión de color existente
  currentSrc = currentSrc.replace(/\.(red|blue|black)\.png$/, '.png');
  currentSrc = currentSrc.replace(/\.png$/, '');

  // Agregar el nuevo color
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
