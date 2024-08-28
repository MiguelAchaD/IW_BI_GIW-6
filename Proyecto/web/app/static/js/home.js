document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function(event) {
        const closestElement = event.target.closest('[data-url]');
        if (closestElement) {
            const url = closestElement.getAttribute('data-url');
            window.location.href = url;
        }
    });
});
