var lastSelection = [null];

function changeSelection(type) {
  if (lastSelection[0] != type) {
    if (lastSelection[0] != null) {
      lastSelection[0].style.backgroundColor = "white";
      if (lastSelection[1] != null) {
        document.getElementById(lastSelection[1].getAttribute("id")).remove();
      }
    }
    lastSelection[0] = type;
    lastSelection[0].style.backgroundColor = "gray";
    deviceSelection(lastSelection[0].getAttribute("id"));
  } else {
    lastSelection[0].style.backgroundColor = "white";
    document.getElementById(lastSelection[1].getAttribute("id")).remove();
    lastSelection[0] = null;
    lastSelection.splice(lastSelection[1], 1);
  }
}

// TODO: Refactorizar estas funciones
function deviceSelection(type) {
  let div = document.createElement("div");
  div.setAttribute("id", type.toString() + "Selection");
  setStyle(div);
  //TODO: Agregar los tipos de productos (bd)
  document.getElementById("deviceSelections").appendChild(div);
  lastSelection[1] = div;
  let divChildren = div.children;
  if (divChildren.length != 0) {
    for (let index = 0; index < divChildren.length; index++) {
      divChildren[index].addEventListener("click", moduleSelection(this));
    }
  } else {
    let noDevices = document.createElement("h1");
    noDevices.innerHTML = "No hay dispositivos disponibles.";
    noDevices.style.textAlign = "center";
    noDevices.style.lineHeight = "450px";
    document
      .getElementById(type.toString() + "Selection")
      .appendChild(noDevices);
  }
}

function moduleSelection(device) {
  let div = document.createElement("div");
  div.setAttribute("id", type.toString() + "Modules");
  setStyle(div);
  //TODO: Agregar los tipos de productos (bd)
  document.getElementById("moduleSelections").appendChild(div);
  let divChildren = div.children;
  if (divChildren.length != 0) {
    for (let index = 0; index < divChildren.length; index++) {
      divChildren[index].addEventListener("click", addToBuildList(this));
    }
  } else {
    let noModules = document.createElement("h1");
    noModules.innerHTML = "No hay módulos disponibles.";
    noModules.style.textAlign = "center";
    noModules.style.lineHeight = "450px";
    document
      .getElementById(type.toString() + "Selection")
      .appendChild(noModules);
  }
}

function addToBuildList(module) {
  //TODO: Añadir a una lista de módulos de construcción
}

function setStyle(element) {
  element.style.margin = "20px auto 20px auto";
  //TODO: Poner el wrap adecuado para los elementos dentro del div
  element.style.justifyContent = "space-around";
  element.style.backgroundColor = "gray";
  element.style.overflowY = "scroll";
  element.style.overflowX = "hidden";
  element.style.width = "70vw";
  element.style.height = "450px";
}
