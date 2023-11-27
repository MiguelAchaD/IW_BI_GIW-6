document.addEventListener('DOMContentLoaded', function () {

    const inputs = document.querySelectorAll('input');
    const inputLabels = document.querySelectorAll('.input-label');

    inputs.forEach((input, index) => {
        input.addEventListener('focus', () => {
            inputLabels[index - 1].classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                inputLabels[index - 1].classList.remove('focused');
            }
        });
    });
});

function handleInput(inputElement) {
    var inputValue = inputElement.value;

    if (inputValue.trim() !== '') {
        inputElement.classList.add('written');
    } else {
        inputElement.classList.remove('written');
    }
}