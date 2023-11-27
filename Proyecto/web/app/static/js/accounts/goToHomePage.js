document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("goToHomePage").addEventListener("click", function () {
        var url = this.getAttribute("data-url");
        window.location.href = url;
    });
});
