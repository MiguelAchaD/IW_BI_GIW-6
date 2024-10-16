document.addEventListener("DOMContentLoaded", function() {
    var selectCustom = document.querySelector('.select-custom');
    var optionsContainer = document.querySelector('.custom-options');
    var selectTrigger = selectCustom.querySelector('.select-custom-trigger');

    // Configurar el valor inicial como "SI" y realizar el cálculo inicial
    selectTrigger.textContent = "SI (Europa)";
    selectTrigger.dataset.value = "SI";
    initializeValuesAndFetchConversionRate();
    handleMetricChange("SI");

    selectCustom.addEventListener('click', function(e) {
        var isOpen = optionsContainer.style.maxHeight === '150px';
        optionsContainer.style.maxHeight = isOpen ? '0px' : '150px';
        selectCustom.classList.toggle('open', !isOpen);
        
        // Añadir funcionalidad para centrar la pantalla en el selector de métricas si está en el 25% inferior de la pantalla
        scrollToSelectCustom();
        
        e.stopPropagation();
    });

    var allOptions = document.querySelectorAll('.custom-option');
    allOptions.forEach(function(option) {
        option.addEventListener('click', function(e) {
            selectTrigger.textContent = this.textContent;
            selectTrigger.dataset.value = this.dataset.value;
            optionsContainer.style.maxHeight = '0px';
            handleMetricChange(this.dataset.value);
            e.stopPropagation();
        });
    });

    document.addEventListener('click', function(event) {
        if (!selectCustom.contains(event.target) && optionsContainer.style.maxHeight === '150px') {
            optionsContainer.style.maxHeight = '0px';
            selectCustom.classList.remove('open');
        }
    });

    // Redirigir al hacer clic en el precio
    document.querySelectorAll('.currency').forEach(function(priceElement) {
        priceElement.addEventListener('click', function() {
            var url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});

function scrollToSelectCustom() {
    // Seleccionar el elemento selectCustom y desplazar la vista hacia él solo si está en el 25% inferior de la pantalla
    var selectCustom = document.querySelector('.select-custom');
    if (selectCustom) {
        var rect = selectCustom.getBoundingClientRect();
        var windowHeight = window.innerHeight;
        
        // Verificar si el elemento está en el 25% inferior de la pantalla visible
        if (rect.bottom > windowHeight * 0.65) {
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            var offsetTop = rect.top + scrollTop - 20; // Ajuste para colocar el elemento justo debajo de la parte superior
            window.scrollTo({ top: offsetTop, behavior: 'smooth' });
        }
    }
}

var conversionRate = 1; // Por defecto, tasa de conversión inicial
var originalPrices = [];
var originalMetrics = []; // Usamos "metrics" en lugar de "distances" para mayor claridad

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