var apiKey = 'hjdslfkadskfjsz';
var baseURL = 'https://open.er-api.com/v6/latest/';

document.addEventListener("DOMContentLoaded", function() {
    var currentValue = "SI";
    var selectElement = document.getElementById("input");
    var distances = document.getElementsByClassName("distance")
    var currencies = document.getElementsByClassName("currency")
    const mmToInchRate = 25.4
    
    var distanceData = [];

    for (var i = 0; i < distances.length; i++) {
        var originalDistance = parseFloat(distances[i].innerText.split(" ")[0].replace(",", "."));
        var convertedDistance = (parseFloat(originalDistance / mmToInchRate).toFixed(2));
        distanceData.push({ mm: originalDistance, inch: convertedDistance });
    }

    fetch(baseURL + 'EUR?apikey=' + apiKey)
        .then(response => response.json())
        .then(data => {
            var conversionRate = data.rates.USD;
        })

    selectElement.addEventListener("change", function() {
        var selectedValue = selectElement.value;
        if (selectedValue == "SI" && selectedValue != currentValue){
            for (var j = 0; j < distanceData.length; j++){
                distances[j].innerText = distanceData[j].mm + " mm"
            }
            for (var i = 0; i < currencies.length; i++){
                price = parseFloat(currencies[i].innerText.split(" ")[0].replace(",", "."));
                if (price > 0){
                    currencies[i].innerText = (price*(1-conversionRate)).toString() + " €";
                } else {
                    currencies[i].innerText = "0 €";
                }
            }
            currentValue = "SI";
        } else if (selectedValue == "Imperial" && selectedValue != currentValue) {
            for (var j = 0; j < distanceData.length; j++){
                distances[j].innerText = distanceData[j].inch + " inch"
            }
            for (var i = 0; i < currencies.length; i++){
                price = parseFloat(currencies[i].innerText.split(" ")[0].replace(",", "."));
                if (price > 0){
                    currencies[i].innerText = (price*conversionRate).toString() + " $";
                } else {
                    currencies[i].innerText = "0 $";
                }
            }
            currentValue = "Imperial";
        }
    });
});