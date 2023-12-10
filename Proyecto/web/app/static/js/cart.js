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
                        productContainer.remove()
                        document.getElementById('totalPrice').innerText = `Total: ${data.newTotalPrice} €`;
                    } else if (data.status === 'empty'){
                        window.location.reload();
                    }else {
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

    function updateQuantity(productId, change, productContainer) {
        fetch(`updateQuantity/${productId}/${change}/`, { 
            method: 'GET',
         }).then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if(data.newQuantity >= 0){
                        document.getElementById(`quantity-${productId}`).innerText = data.newQuantity;
                    }else{
                        productContainer.remove()                        
                    }
                    document.getElementById('totalPrice').innerText = `Total: ${data.newTotalPrice} €`;
                } else if (data.status === 'empty'){
                    window.location.reload();
                }else {
                    alert(data.message);
                }
            });
    }
});