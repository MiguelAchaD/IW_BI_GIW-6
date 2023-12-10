document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-id');
            const productContainer = this.closest('.cart-item');

            fetch(`remove/${productId}/`, {
                method: 'GET',
            }).then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        if(data.newQuantity >= 0){
                            productContainer.remove();
                            document.getElementById('totalPrice').innerText = `Total: ${data.newTotalPrice} €`;
                        } else {
                            window.location.reload();
                        }
                    } else if (data.status === 'empty') {
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                });
        });
    });
});
