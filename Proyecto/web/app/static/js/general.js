document.addEventListener("DOMContentLoaded", function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated', 'slideInLeft');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    // Seleccionar elementos para animar, excluyendo el select y sus opciones
    document.querySelectorAll('main *:not(.select-custom, .select-custom *)').forEach(el => {
        observer.observe(el);
    });
});
