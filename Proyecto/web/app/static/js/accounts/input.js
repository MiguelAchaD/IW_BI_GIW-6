document.addEventListener('DOMContentLoaded', function () {

    const inputs = document.querySelectorAll('input');
    const inputLabels = document.querySelectorAll('.input-label');

    inputs.forEach((input, index) => {
        input.addEventListener('focus', () => {
            inputLabels[index].classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                inputLabels[index].classList.remove('focused');
            }
        });
    });
});

function handleInput(inputElement) {
    var inputValue = inputElement.value;

    if (inputValue.trim() !== '') {
        inputElement.classList.add('written');
        console.log("written");
    } else {
        inputElement.classList.remove('written');
        console.log("not written");
    }
}