document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-id');
            const productContainer = this.closest('.cart-item');

            fetch(`remove/${productId}/`, {
                method: 'GET'
            }).then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        removeProductContainer(productContainer);
                        document.getElementById('totalPrice').innerText = `Total: ${data.newTotalPrice} €`;
                    } else if (data.status === 'empty') {
                        removeProductContainer(productContainer);
                        setTimeout(() => window.location.reload(), 500);
                    } else {
                        alert(data.message);
                    }
                });
        });
    });
    document.querySelectorAll('.increase-quantity').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-id');
            const productContainer = this.closest('.cart-item');
            updateQuantity(productId, 1, productContainer);
        });
    });

    document.querySelectorAll('.decrease-quantity').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-id');
            const productContainer = this.closest('.cart-item');
            updateQuantity(productId, -1, productContainer);
        });
    });

    document.querySelectorAll('.cart-item').forEach(item => {
        item.addEventListener('click', function (event) {
            if (event.target.tagName !== 'BUTTON' && !event.target.closest('button')) {
                const moduleDetails = this.querySelector('.module-details');
                if (moduleDetails) {
                    if (moduleDetails.classList.contains('open')) {
                        moduleDetails.style.height = '0px';
                    } else {
                        moduleDetails.style.height = moduleDetails.scrollHeight -1  + 'px';
                    }
                    moduleDetails.classList.toggle('open');
                }
            }
        });
    });
    

    function removeProductContainer(productContainer) {
        productContainer.classList.add('collapse');
        setTimeout(() => productContainer.remove(), 500);
    }

    function updateQuantity(productId, change, productContainer) {
        fetch(`updateQuantity/${productId}/${change}/`, {
            method: 'GET',
        }).then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (data.newQuantity > 0) {
                        document.getElementById(`quantity-${productId}`).innerText = data.newQuantity;
                    } else {
                        removeProductContainer(productContainer);
                    }
                    document.getElementById('totalPrice').innerText = `Total: ${data.newTotalPrice} €`;
                } else if (data.status === 'empty') {
                    window.location.reload();
                } else {
                    alert(data.message);
                }
            });
    }
});