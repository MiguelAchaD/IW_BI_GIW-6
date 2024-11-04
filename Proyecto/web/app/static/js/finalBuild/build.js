let selectedPairs = [];

function selectModule(elementId, pair) {
  const element = document.querySelector(`.selectable[data-id="${elementId}"]`);
  if (!element) return;

  const existingIndex = selectedPairs.findIndex(item => item.pair === pair);

  if (existingIndex !== -1) {
    if (selectedPairs[existingIndex].element === element) {
      element.classList.remove('moduleSelected');
      selectedPairs.splice(existingIndex, 1);
      return;
    } else {
      selectedPairs[existingIndex].element.classList.remove('moduleSelected');
      selectedPairs.splice(existingIndex, 1);
    }
  }

  element.classList.add('moduleSelected');
  selectedPairs.push({ element, pair });
}

function addToCart(product_id) {
  const cartItems = selectedPairs.map(item => ({
    id: item.element.getAttribute('data-id'),
    pair: item.pair,
  }));

  const moduleIds = cartItems.map(item => item.id);

  const cart = [];
  cart[0] = product_id;
  cart[1] = [];
  cart[1] = cartItems.map(item => item.id);

  $(document).ready(function () {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var dataToSend = cart;
    console.log(dataToSend)

    $.ajax({
      type: "POST",
      url: "/addToCart/",
      data: JSON.stringify({ product_id: product_id, modules: moduleIds }),
      contentType: "application/json",
      dataType: "json",  
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        console.log(response);  
      },
      error: function (xhr, status, error) {
        console.error("Error en la solicitud:", error)
      } 
    });
  });
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


document.querySelectorAll('.selectable').forEach(el => {
  el.addEventListener('click', function () {
    const elementId = el.classList[1];
    const pair = el.getAttribute('data-pair');
    selectModule(elementId, pair);
  });
});
