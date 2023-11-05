var apiKey = 'hjdslfkadskfjsz';
var baseURL = 'https://open.er-api.com/v6/latest/';

document.addEventListener("DOMContentLoaded", function() {
    var currentValue = "SI";
    var selectElement = document.getElementById("input");
    var distances = document.getElementsByClassName("distance")
    var currency = document.getElementById("currency")
    const mmToInchRate = 25.4
    
    var distanceData = [];

    for (var i = 0; i < distances.length; i++) {
        var originalDistance = parseFloat(distances[i].innerText.split(" ")[0].replace(",", "."));
        // Convertir de milímetros a pulgadas usando el ratio mmToInchRate
        var convertedDistance = (parseFloat(originalDistance / mmToInchRate).toFixed(2));
        // Almacenar la distancia original y convertida en el array
        distanceData.push({ mm: originalDistance, inch: convertedDistance });
    }

    fetch(baseURL + 'EUR?apikey=' + apiKey)
        .then(response => response.json())
        .then(data => {
            // Obtener la tasa de cambio para convertir de euros a dólares
            var conversionRate = data.rates.USD;
        })

    selectElement.addEventListener("change", function() {
        var selectedValue = selectElement.value;
        if (selectedValue == "SI" && selectedValue != currentValue){
            for (var j = 0; j < distanceData.length; j++){
                distances[j].innerText = distanceData[j].mm + " mm"
            }
            price = parseFloat(currency.innerText.split(" ")[0].replace(",", "."));
            if (price > 0){
                currency.innerText = (price*(1-conversionRate)).toString() + " €";
            } else {
                currency.innerText = "0 €";
            }
            currentValue = "SI";
        } else if (selectedValue == "Imperial" && selectedValue != currentValue) {
            for (var j = 0; j < distanceData.length; j++){
                distances[j].innerText = distanceData[j].inch + " inch"
            }
            currentValue = "Imperial";
            price = parseFloat(currency.innerText.split(" ")[0].replace(",", "."));
            if (price > 0){
                currency.innerText = (price*conversionRate).toString() + " $";
            } else {
                currency.innerText = "0 $";
            }
        }
    });
});