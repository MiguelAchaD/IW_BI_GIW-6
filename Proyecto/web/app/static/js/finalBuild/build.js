const lastSelection = [null, null, null];
cart = [0, null];

setSelectionStyle();
setSentToCartAction(document.getElementById("anyadirCarrito"));

function changeSelection(type, products) {
  if (lastSelection[0] !== document.getElementById(type)) {
    clearLastSelection(0);
    clearModuleSelections();
    if (document.getElementById("device").children.length > 0) {
      clearCart();
    }
    lastSelection[0] = document.getElementById(type);
    lastSelection[0].style.backgroundColor = "gray";
    deviceSelection(lastSelection[0], products);
  } else {
    clearLastSelection(0);
    clearModuleSelections();
    if (document.getElementById("device").children.length > 0) {
      clearCart();
    }
  }
}

function clearCart() {
  var deviceOnCart = document.getElementById("device").children;
  deviceOnCart[0].remove();
  cart[1] = null;
}

function clearLastSelection(index) {
  if (lastSelection[index] !== null) {
    lastSelection[index].style.backgroundColor = "white";
    if (index === 0) {
      clearDeviceSelections();
    }
  }
}

function clearDeviceSelections() {
  for (let i = 1; i <= 2; i++) {
    if (lastSelection[i] !== null) {
      document.getElementById(lastSelection[i].getAttribute("id")).remove();
      lastSelection[i] = null;
    }
  }
  lastSelection[0] = null;
}

//TIPO DE DISPOSITIVO
function deviceSelection(type, products) {
  const parentDiv = document.getElementById("deviceSelections");
  const div = createSelectionDiv(type.getAttribute("id"));
  parentDiv.appendChild(div);

  products[type.getAttribute("id")].forEach(
    ([
      productID,
      productName,
      productPrice,
      productDimensionX,
      productDimensionY,
      productDimensionZ,
    ]) => {
      const divIntern = createDiv(
        productID,
        productName,
        productPrice,
        productDimensionX,
        productDimensionY,
        productDimensionZ
      );
      div.appendChild(divIntern);
    }
  );
  lastSelection[1] = div;
  setSelectionClickListener(div.children, moduleSelection);
  setCartClickListener(div.children, addToBuildList, products, 1);
}

//MODELO DE TIPO DE DISPOSITIVO
function moduleSelection(type) {
  $(document).ready(function () {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var dataToSend = "modulesFor_" + type;

    $.ajax({
      type: "POST",
      url: "builder",
      data: { datos: dataToSend },
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        //Primera vez que se selecciona
        if (lastSelection[2] === null) {
          const div = createSelectionDiv(type + "Modules");
          document.getElementById("moduleSelections").appendChild(div);
          lastSelection[2] = div;
          if (lastSelection[1] === document.getElementById(type)) {
            document.getElementById(type).style.backgroundColor = "gray";
          } else {
            document.getElementById(
              lastSelection[1].getAttribute("id")
            ).style.backgroundColor = "#ddd";
            document.getElementById(type).style.backgroundColor = "gray";
          }
          var compatibleModules = response;
          compatibleModules.forEach(
            ([
              moduleID,
              moduleName,
              modulePrice,
              moduleDimensionX,
              moduleDimensionY,
              moduleDimensionZ,
              modulePairs,
            ]) => {
              const divIntern = createDiv(
                moduleID,
                moduleName,
                modulePrice,
                moduleDimensionX,
                moduleDimensionY,
                moduleDimensionZ,
                modulePairs
              );
              div.appendChild(divIntern);
            }
          );
          setCartClickListener(
            div.children,
            addToBuildList,
            compatibleModules,
            2
          );
          //La selección es distinta de lo anterior
        } else if (
          type + "ModulesSelection" !==
          lastSelection[2].getAttribute("id")
        ) {
          let selectionChildren = document.getElementById(
            lastSelection[1].getAttribute("id")
          ).children;
          for (let index = 0; index < selectionChildren.length; index++) {
            document.getElementById(
              selectionChildren[index].getAttribute("id")
            ).style.backgroundColor = "#ddd";
          }
          document.getElementById(lastSelection[2].getAttribute("id")).remove();
          lastSelection[2] = null;
          moduleSelection(type);
          clearModuleSelections();
          //La selección es la misma que la anterior
        } else {
          document.getElementById(lastSelection[2].getAttribute("id")).remove();
          lastSelection[2] = null;
          document.getElementById(type).style.backgroundColor = "#ddd";
          clearModuleSelections();
        }
      },
      error: function (error) {
        console.log("Error en la solicitud AJAX:", error);
      },
    });
  });
}

function clearModuleSelections() {
  if (cart.length > 2) {
    for (let i = cart.length - 1; i > 1; i--) {
      document.getElementById(cart[i]).remove();
      cart.splice(i, 1);
    }
  }
}

function sendSelection(cart) {
  $(document).ready(function () {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var dataToSend = cart;
    console.log(dataToSend)

    $.ajax({
      type: "POST",
      url: "builder",
      data: { datos: dataToSend },
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        if (response === "success") {
          window.location.href = "/myCart";
        } else {
          console.log("Respuesta: " + response);
        }
      },
      error: function (error) {
        console.log("Error en la solicitud AJAX:", error);
      },
    });
  });
}

function addToBuildList(element, object, index) {
  //SUMAR EL COSTE
  var elementAttributes;
  //MODELO DE DISPOSITIVO
  if (index === 1) {
    object[element.split("-")[0]].forEach((e) => {
      if (e[0] == element.split("_")[0]) {
        elementAttributes = e;
      }
    });
    let device = document.getElementById("device");
    if (device.children.length === 0 && cart[1] !== elementAttributes[0]) {
      var div = document.createElement("div");
      div.setAttribute("id", element + "-toCart");
      setCartStyle(div);
      device.appendChild(div);
      cart[1] = elementAttributes[0];
      let divHeader = document.createElement("h2");
      divHeader.innerHTML = elementAttributes[1];
      div.appendChild(divHeader);
    } else if (
      device.children.length === 1 &&
      cart[1] !== elementAttributes[0]
    ) {
      removeFromBuildList(index, element);
      cart[1] = null;
      addToBuildList(element, object, index);
    } else {
      removeFromBuildList(index, element);
      cart[1] = null;
    }
    //MODULO DE DISPOSITIVO
  } else {
    object.forEach((e) => {
      if (e[0] == element.split("_")[0]) {
        elementAttributes = e;
      }
    });
    let cartDiv = document.getElementById("items");
    let itemsChildren = Array.from(cartDiv.children).splice(2);
    let itemsChildrenPairs = itemsChildren.map((e) => {
      return e.getAttribute("id").split("_")[1];
    });
    let itemsChildrenId = itemsChildren.map((e) => {
      return e.getAttribute("id").split("-")[0];
    });
    if (itemsChildrenPairs.includes(element.split("_")[1])) {
      if (itemsChildrenId.includes(element.split("_")[0])) {
        //mismo
        document.getElementById(element.replace("_", "-toCart_")).remove();
        cart.splice(cart.indexOf(element.split("_")[0] + "-toCart_" + element.split("_")[1]), 1);
      } else {
        //diferente
        itemsChildren.forEach((e) => {
          if (e.getAttribute("id").split("_")[1] == element.split("_")[1]) {
            document.getElementById(e.getAttribute("id")).remove();
            cart.splice(cart.indexOf(e.getAttribute("id")), 1);
            addToBuildList(element, object, index);
          }
        });
      }
    } else {
      let div = document.createElement("div");
      div.setAttribute(
        "id",
        element.split("_")[0] + "-toCart_" + element.split("_")[1]
      );
      setCartStyle(div);
      device.appendChild(div);
      cart.push((element.split("_")[0] + "-toCart_" + element.split("_")[1]));
      let divHeader = document.createElement("h2");
      divHeader.innerHTML = elementAttributes[1];
      div.appendChild(divHeader);
      document.getElementById("items").appendChild(div);
      //cart += element.split("_")[0] + "-toCart_" + element.split("_")[1];
    }
    //itemsChildren = itemsChildren.slice(2);
    //let itemsChildrenName = [];
    //itemsChildren.forEach((i) => {
    //  itemsChildrenName.push(i.textContent.split(" ")[0]);
    //});
    //itemsChildren = itemsChildren.map((e) => {
    //  return e.getAttribute("id").split("_")[0];
    //});
    //if (
    //  itemsChildren.length < 5 &&
    //  !itemsChildren.includes(element + "-toCart") &&
    //  !itemsChildrenName.includes(elementAttributes[1].split(" ")[0])
    //) {
    //  let div = document.createElement("div");
    //  div.setAttribute("id", element + "-toCart");
    //  setCartStyle(div);
    //  device.appendChild(div);
    //  cart.push(elementAttributes[0]);
    //  let divHeader = document.createElement("h2");
    //  divHeader.innerHTML = elementAttributes[1];
    //  div.appendChild(divHeader);
    //  document.getElementById("items").appendChild(div);
    //} else if (
    //  itemsChildren.includes(element) ||
    //  itemsChildrenName.includes(elementAttributes[1].split(" ")[0])
    //) {
    //  var toRemove = (Array.from(document.getElementById("items").children).splice(2))[itemsChildrenName.indexOf(elementAttributes[1].split(" ")[0])];
    //  removeFromBuildList(index, toRemove);
    //  itemsChildrenName.splice(
    //    itemsChildrenName.indexOf(elementAttributes[1].split(" ")[0]),
    //    1
    //  );
    //  cart.pop(cart.indexOf(elementAttributes[0]));
    //  addToBuildList(element, object, index);
    //}
  }
}

function removeFromBuildList(index, element) {
  //TODO: RESTAR EL COSTE
  if (index === 1) {
    let deviceChildren = document.getElementById("device").children;
    deviceChildren[0].remove();
    cart[1] = null;
  } else {
    //let cartDiv = document.getElementById("items");
    element.remove();
  }
}

function setSelectionStyle() {
  const buttons = document.getElementsByClassName("clickableOption");
  Array.from(buttons).forEach((button) => {
    button.style.border = "2px gray solid";
    button.style.borderRadius = "5px";
    button.addEventListener("mouseover", () => {
      button.style.border = "2px black solid";
    });
    button.addEventListener("mouseout", () => {
      button.style.border = "2px gray solid";
    });
  });
}

function createSelectionDiv(id) {
  const div = document.createElement("div");
  div.setAttribute("id", id + "Selection");
  setStyle(div);
  return div;
}

function createDiv(id, name, price) {
  const divIntern = document.createElement("div");
  setInternStyle(divIntern);
  divIntern.setAttribute("id", id);

  const divHeader = document.createElement("h2");
  divHeader.innerHTML = name;

  const divPrice = document.createElement("p");
  divPrice.innerHTML = price;

  divIntern.appendChild(divHeader);
  divIntern.appendChild(divPrice);

  return divIntern;
}

function createDiv(id, name, price, dimensionX, dimensionY, dimensionZ, pairs) {
  const divIntern = document.createElement("div");
  setInternStyle(divIntern);
  divIntern.setAttribute("id", id + "_" + pairs);

  const divHeader = document.createElement("h2");
  divHeader.innerHTML = name;

  const divDimensions = document.createElement("p");
  divDimensions.innerHTML =
    "x: " + dimensionX + ", y: " + dimensionY + ", z: " + dimensionZ;

  const divPrice = document.createElement("p");
  divPrice.innerHTML = price;

  divIntern.appendChild(divHeader);
  divIntern.appendChild(divDimensions);
  divIntern.appendChild(divPrice);

  return divIntern;
}

function setSelectionClickListener(elements, clickHandler) {
  Array.from(elements).forEach((element) => {
    element.addEventListener("click", () => {
      clickHandler(element.getAttribute("id"));
    });
  });
}

function setSentToCartAction(element){
  element.addEventListener("click", () => {
    sendSelection(cart);
  });
}

function setCartClickListener(
  elements,
  clickHandler,
  compatibleModules,
  index
) {
  Array.from(elements).forEach((element) => {
    element.addEventListener("click", () => {
      clickHandler(element.getAttribute("id"), compatibleModules, index);
    });
  });
}

function setStyle(element) {
  element.style.margin = "20px auto 20px auto";
  element.style.display = "flex";
  element.style.overflowY = "scroll";
  element.style.overflowX = "hidden";
  element.style.flexWrap = "wrap";
  element.style.backgroundColor = "#ddd";
  element.style.width = "70vw";
  element.style.height = "500px";
}

function setInternStyle(element) {
  element.addEventListener("mouseover", () => {
    element.style.border = "2px black solid";
  });

  element.addEventListener("mouseout", () => {
    element.style.border = "2px gray solid";
  });

  element.style.textAlign = "center";
  element.style.margin = "10px";
  element.style.height = "300px";
  element.style.minHeight = "300px";
  element.style.width = "275px";
  element.style.minWidth = "275px";
  element.style.border = "2px gray solid";
  element.style.borderRadius = "7px";
}

function setCartStyle(element) {
  //element.addEventListener("mouseover", () => {
  //  element.style.border = "2px black solid";
  //});

  //element.addEventListener("mouseout", () => {
  //  element.style.border = "2px gray solid";
  //});

  element.style.textAlign = "center";
  element.style.height = "100%";
  element.style.width = "100%";
  element.style.fontSize = "10px";
}

function noElementsShow(div, text) {
  const noElement = document.createElement("h1");
  noElement.innerHTML = text;
  noElement.style.textAlign = "center";
  noElement.style.lineHeight = "450px";
  document.getElementById(div.getAttribute("id")).appendChild(noElement);
}
