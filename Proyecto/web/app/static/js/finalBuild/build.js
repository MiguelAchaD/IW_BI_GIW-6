var lastSelection;
var productType = document.getElementsByClassName("clickableOption");

document.addEventListener("DOMContentLoaded", function() {
    for (var i = 0; i<productType.length;i++){
        productType[i].addEventListener("change"+[i].toString(), function() {
            changeSelection(productType[i].attributes());
        });
    }
});

function changeSelection(type){
    console.log(type["id"]);
}