const lastSelection = [null, null, null];
cart = [0, null];

setSelectionStyle();

function changeSelection(type, modules, index) {
  if (lastSelection[index] !== type) {
    clearLastSelection(index);

    lastSelection[index] = type;
    lastSelection[index].style.backgroundColor = "gray";
    if (index === 0) {
      deviceSelection(lastSelection[index].getAttribute("id"), modules);
    }
  } else {
    clearLastSelection(index);
  }
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

function deviceSelection(type, compatibleModules) {
  const parentDiv = document.getElementById("deviceSelections");
  const div = createSelectionDiv(type);
  parentDiv.appendChild(div);

  compatibleModules.forEach(([moduleId, moduleType, modulePrice]) => {
    if (moduleType.split(" ")[0] === type) {
      const divIntern = createDiv(moduleId, moduleType, modulePrice);
      div.appendChild(divIntern);
    }
  });

  lastSelection[1] = div;
  setSelectionClickListener(div.children, moduleSelection, compatibleModules);
  setCartClickListener(div.children, addToBuildList, compatibleModules, 1);
}

function moduleSelection(type, compatibleModules) {
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
    compatibleModules.forEach(
      ([moduleId, moduleType, modulePrice, modules]) => {
        if (moduleId === type) {
          modules.forEach(([moduleID, moduleName, modulePrice]) => {
            const divIntern = createDiv(moduleID, moduleName, modulePrice);
            div.appendChild(divIntern);
          });
        }
      }
    );
    setCartClickListener(div.children, addToBuildList, compatibleModules, 2);
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
    moduleSelection(type, compatibleModules);
  } else {
    document.getElementById(lastSelection[2].getAttribute("id")).remove();
    lastSelection[2] = null;
    document.getElementById(type).style.backgroundColor = "#ddd";
  }
}

function sendSelection(cart) {
  $(document).ready(function () {
    var csrftoken = getCookie("csrftoken");

    $.ajax({
      url: builderUrl,
      type: "POST",
      data: { datos_nuevos: cart },
      dataType: "json",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      success: function (response) {
        //TODO: Crear alerta en div emergente
        console.log(response.mensaje);
      },
    });

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
}

function addToBuildList(element, compatibleModules, index) {
  TODO: //SUMAR EL COSTE
  var elementAttributes;
  compatibleModules.forEach((e) => {
    if (e[0] == element) {
      elementAttributes = e;
      elementAttributes += e[3];
    }
  });
  console.log(element);
  console.log("elementAttributes:", elementAttributes);
  if (index === 1) {
    let device = document.getElementById("device");
    if (device.children.length === 0 && cart[1] !== elementAttributes[0]) {
      var div = document.createElement("div");
      div.setAttribute("id", element + "-toCart");
      setCartStyle(div);
      device.appendChild(div);
      cart[1] = elementAttributes[0];
      let divHeader = document.createElement("h2");
      divHeader.innerHTML = elementAttributes[1];
      divHeader.innerHTML = "prueba";
      div.appendChild(divHeader);
    } else if (
      device.children.length === 1 && cart[1] !== elementAttributes[0]) {
      removeFromBuildList(index, element);
      addToBuildList(element, compatibleModules, index);
    } else {
      removeFromBuildList(index, element);
    }
  } else {
    let cartDiv = document.getElementById("items");
    itemsChildren = Array.from(cartDiv.children); 
    itemsChildren = itemsChildren.map((e) => {
      return e.getAttribute("id");
    });
    itemsChildren = itemsChildren.slice(2);
    if (itemsChildren.length < 5 && !itemsChildren.includes(element + "-toCart")) {
      let div = document.createElement("div");
      div.setAttribute("id", element + "-toCart");
      setCartStyle(div);
      device.appendChild(div);
      //HERE
      cart.append(elementAttributes[0]);
      let divHeader = document.createElement("h2");
      //divHeader.innerHTML = elementAttributes[1];
      divHeader.innerHTML = "prueba";
      div.appendChild(divHeader);
      document.getElementById("items").appendChild(div);

    } else if (itemsChildren.includes(element)) {
      removeFromBuildList(index, element);
    } else {
      console.log("lleno");
    }
  }
}

function removeFromBuildList(index, element) {
  //TODO: RESTAR EL COSTE
  if (index === 1) {
    let deviceChildren = document.getElementById("device").children;
    deviceChildren[0].remove();
    cart[1] = null;
  } else {
    let cartDiv = document.getElementById("items");
    console.log(element);
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

function setSelectionClickListener(elements, clickHandler, compatibleModules) {
  Array.from(elements).forEach((element) => {
    element.addEventListener("click", () => {
      clickHandler(element.getAttribute("id"), compatibleModules);
    });
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
