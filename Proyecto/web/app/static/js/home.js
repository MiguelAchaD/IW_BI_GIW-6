document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.image-stack img').forEach(function(image) {
        image.addEventListener('click', function() {
            const url = image.getAttribute('data-url');
            window.location.href = url;
        });
    });
});