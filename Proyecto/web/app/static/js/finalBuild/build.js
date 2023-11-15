var lastSelection = [null, null, null];

function changeSelection(type, compatibleModules) {
  if (lastSelection[0] != type) {
    if (lastSelection[0] != null) {
      lastSelection[0].style.backgroundColor = "white";
      if (lastSelection[1] != null) {
        document.getElementById(lastSelection[1].getAttribute("id")).remove();
        lastSelection[1] = null;
      } 
      if (lastSelection[2] != null){
        document.getElementById(lastSelection[2].getAttribute("id")).remove();
        lastSelection[2] = null;
      }
    }
    lastSelection[0] = type;
    lastSelection[0].style.backgroundColor = "gray";
    deviceSelection(lastSelection[0].getAttribute("id"), compatibleModules);
  } else {
    lastSelection[0].style.backgroundColor = "white";
    document.getElementById(lastSelection[1].getAttribute("id")).remove();
    lastSelection[0] = null;
    lastSelection.splice(lastSelection[1], 1);
  }
}

// TODO: Refactorizar estas funciones
function deviceSelection(type, compatibleModules) {
  let parentDiv = document.getElementById("deviceSelections");
  let div = document.createElement("div");
  div.setAttribute("id", type + "Selection");
  setStyle(div);
  parentDiv.appendChild(div);
  compatibleModules.forEach(element => {
    if (element[1].split(" ")[0] == type){
      //TODO: Agregar los tipos de productos (bd)
      let divIntern = document.createElement("div");
      setInternStyle(divIntern);
      divIntern.setAttribute("id", element[0]);
      let divHeader = document.createElement("h2");
      divHeader.innerHTML = element[1];
      let divPrice = document.createElement("p");
      divPrice.innerHTML = element[2];
      divIntern.appendChild(divHeader);
      divIntern.appendChild(divPrice);
      div.appendChild(divIntern);
    }
  });
  lastSelection[1] = div;
  let divChildren = div.children;
  if (divChildren.length != 0) {
    for (let index = 0; index < divChildren.length; index++) {
      divChildren[index].addEventListener("click", function() {moduleSelection(divChildren[index].getAttribute("id"), compatibleModules)}, false);
    }
  } else {
    let noDevices = document.createElement("h1");
    noDevices.innerHTML = "No hay dispositivos disponibles.";
    noDevices.style.textAlign = "center";
    noDevices.style.lineHeight = "450px";
    document
      .getElementById(div.getAttribute("id"))
      .appendChild(noDevices);
  }
}

function moduleSelection(type, compatibleModules) {
  if (lastSelection[2] == null){
    let div = document.createElement("div");
    div.setAttribute("id", type + "Modules");
    setStyle(div);
    compatibleModules.forEach(element => {
      if (element[0] == type){
        element[3].forEach(module => {
          let divIntern = document.createElement("div");
          setInternStyle(divIntern);
          divIntern.setAttribute("id", module);
          let divHeader = document.createElement("h2");
          divHeader.innerHTML = module[0];
          let divPrice = document.createElement("p");
          divPrice.innerHTML = module[1];
          divIntern.appendChild(divHeader);
          divIntern.appendChild(divPrice);
          div.appendChild(divIntern);});
      }
    });
    document.getElementById("moduleSelections").appendChild(div);
    lastSelection[2] = div;
    let divChildren = div.children;
    if (divChildren.length != 0) {
      for (let index = 0; index < divChildren.length; index++) {
        divChildren[index].addEventListener("click", function(){ addToBuildList(this)});
      }
    } else {
      let noModules = document.createElement("h1");
      noModules.innerHTML = "No hay módulos disponibles.";
      noModules.style.textAlign = "center";
      noModules.style.lineHeight = "450px";
      document
        .getElementById(div.getAttribute("id"))
        .appendChild(noModules);
    }
  } else {
    if (type+"Modules" != lastSelection[2].getAttribute("id")){
      document.getElementById(lastSelection[2].getAttribute("id")).remove();
      lastSelection[2] = null;
      moduleSelection(type, compatibleModules); 
    }
  }
}

function addToBuildList(module) {
  //TODO: Añadir a una lista de módulos de construcción
}

function setStyle(element) {
  element.style.margin = "20px auto 20px auto";
  element.style.display = "flex";
  element.style.overflowY = "scroll";
  element.style.overflowX = "hidden";
  element.flexWrap = "wrap";
  element.style.backgroundColor = "gray";
  element.style.width = "70vw";
}

function setInternStyle(element) {
  element.style.textAlign = "center";
  element.style.margin = "10px auto 10px auto";
  element.style.height = "300px";
  element.style.minHeight = "300px";
  element.style.width = "250px";
  element.style.minWidth = "250px";
  element.style.backgroundColor = "white";
  element.style.borderRadius = "10px";
}