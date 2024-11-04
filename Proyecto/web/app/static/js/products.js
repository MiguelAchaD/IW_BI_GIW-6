document.addEventListener("DOMContentLoaded", function() {
    var selectCustom = document.querySelector('.select-custom');
    var optionsContainer = document.querySelector('.custom-options');
    var selectTrigger = selectCustom.querySelector('.select-custom-trigger');

    selectTrigger.textContent = "SI (Europa)";
    selectTrigger.dataset.value = "SI";
    initializeValuesAndFetchConversionRate();
    handleMetricChange("SI");

    selectCustom.addEventListener('click', function(e) {
        var isOpen = selectCustom.classList.contains('open');
        
        if (!isOpen) {
            fadeText(selectTrigger, "Seleccionar medida");
        } else {
            restoreSelectedText(selectTrigger); // Pasa selectTrigger como parámetro
        }

        selectCustom.classList.toggle('open', !isOpen);

        if (!isOpen && window.innerWidth <= 768) {
            scrollToSelectCustom();
        }

        e.stopPropagation();
    });

    var allOptions = document.querySelectorAll('.custom-option');
    allOptions.forEach(function(option) {
        option.addEventListener('click', function(e) {
            var selectedText = this.textContent;
            selectTrigger.dataset.value = this.dataset.value;

            fadeText(selectTrigger, selectedText);

            selectCustom.classList.remove('open');
            handleMetricChange(this.dataset.value);
            e.stopPropagation();
        });
    });

    document.addEventListener('click', function(event) {
        if (!selectCustom.contains(event.target) && selectCustom.classList.contains('open')) {
            selectCustom.classList.remove('open');
            restoreSelectedText(selectTrigger);
        }
    });

    document.querySelectorAll('.product-item').forEach(function(priceElement) {
        priceElement.addEventListener('click', function() {
            var url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});

function restoreSelectedText(selectTrigger) {
    var selectedValue = selectTrigger.dataset.value;
    var restoredText = selectedValue === "SI" ? "SI (Europa)" : "Imperial (América del Norte)";
    fadeText(selectTrigger, restoredText);
}

function fadeText(element, newText) {
    element.classList.add('hidden');
    setTimeout(function() {
        element.textContent = newText;
        element.classList.remove('hidden');
    }, 250); 
}

function scrollToSelectCustom() {
    var selectCustom = document.querySelector('.select-custom');
    if (selectCustom) {
        var rect = selectCustom.getBoundingClientRect();
        var windowHeight = window.innerHeight;
        
        if (rect.bottom > windowHeight * 0.65) {
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            var offsetTop = rect.top + scrollTop - 20;  
            window.scrollTo({ top: offsetTop, behavior: 'smooth' });
        }
    }
}

var conversionRate = 1; 
var originalPrices = [];
var originalMetrics = [];

function initializeValuesAndFetchConversionRate() {
    var currencies = document.getElementsByClassName("currency");
    var metrics = document.getElementsByClassName("metric");
    
    for (var i = 0; i < currencies.length; i++) {
        originalPrices.push(parseFloat(currencies[i].innerText.split(" ")[0].replace(",", ".")));
    }
    for (var i = 0; i < metrics.length; i++) {
        originalMetrics.push(parseFloat(metrics[i].innerText.split(" ")[0].replace(",", ".")));
    }
    getConversionRate();
}

function getConversionRate() {
    var url = `https://api.exchangerate-api.com/v4/latest/EUR`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            conversionRate = data.rates.USD;
        })
        .catch(error => console.error('Error al obtener la tasa de conversión:', error));
}

function handleMetricChange(selectedValue) {
    var metrics = document.getElementsByClassName("metric");
    var currencies = document.getElementsByClassName("currency");

    for (var i = 0; i < metrics.length; i++) {
        if (selectedValue === "SI") {
            metrics[i].innerText = originalMetrics[i].toFixed(2) + " mm";
        } else if (selectedValue === "Imperial") {
            var convertedMetric = (originalMetrics[i] / 25.4).toFixed(2);
            metrics[i].innerText = convertedMetric + " inch";
        }
    }

    for (var i = 0; i < currencies.length; i++) {
        if (selectedValue === "SI") {
            currencies[i].innerText = originalPrices[i].toFixed(2) + " €";
        } else if (selectedValue === "Imperial") {
            var convertedPrice = (originalPrices[i] * conversionRate).toFixed(2);
            currencies[i].innerText = convertedPrice + " $";
        }
    }
}
