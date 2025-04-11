function changeStatusInCart(e) {
	var prevInnerHTML = e.innerHTML;
	e.innerHTML = "<span class='spinner-grow spinner-grow-md' role='status' aria-hidden='true'></span>Loading...";

	var minTimeoutValue = 100;
	var maxTimeoutValue = 1000;
	var timeoutValue = Math.random() * (maxTimeoutValue - minTimeoutValue) + minTimeoutValue;
	console.log(timeoutValue);
	// Math.random() is [0, 1)
	// Lol class 11th maths
	setTimeout(() => {
		var selectedSize = e.parentElement.getElementsByClassName("productsizesclass")[0];
		if(selectedSize.value == "") {
			alert("Please select a size");
			e.innerHTML = prevInnerHTML;
			return false;
		}
		var cartStatus = e.parentElement.getElementsByClassName("productstatusclass")[0];
		if(cartStatus.value == "n") {
            var templateimage = e.parentElement.parentElement.getElementsByClassName("templateimage")[0];
            var templateid = e.parentElement.parentElement.getElementsByClassName("templateid")[0];
            var cartid = e.parentElement.parentElement.getElementsByClassName("cartid")[0];
			var csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0];
			var productQty = parseInt(e.parentElement.getElementsByClassName("cartQty")[0].innerHTML);
			if(productQty == 0) {
				cartStatus.value = "n";
				e.innerHTML = "Add To Cart";
				return false;
			}
            post_data = {
                "add-to-cart": true,
                "styled_template_url": templateimage.src,
                "template_id": templateid.value,
				'csrfmiddlewaretoken': csrftoken.value,
				"quantity": productQty
            }
            console.log(post_data);
            $.post("/api/add-remove-cart", post_data,
                function(data) {
                    // Added to cart
                    cartid.value = data;
					console.log(cartid.value);
					cartStatus.value = "y";
					e.innerHTML = "Remove From Cart";
				}
			);
        }
		else if(cartStatus.value == "y") {
            var cartid = e.parentElement.parentElement.getElementsByClassName("cartid")[0];
            var csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0];
            post_data = {
                "remove-from-cart": true,
                "cart_object_id": cartid.value,
                'csrfmiddlewaretoken': csrftoken.value
            }
            console.log(post_data);
            $.post("/api/add-remove-cart", post_data,
                function(data) {
                    if(data == "success") {
                        cartid.value = ""
						// Removed from cart
						cartStatus.value = "n";
						e.innerHTML = "Add To Cart";
					}
					else {
						alert("Sorry error occured while removing item");
						cartStatus.value = "y";
						e.innerHTML = "Remove From Cart";
					}
                }
            );
		}
	}, timeoutValue);
}

function shareProduct(e) {
	console.log("Product is shared");
}

function selectSize(e) {
	var productSizeTags = e.parentElement.getElementsByClassName("productsizesclass");
	var currProductSize = productSizeTags[0];
	for(var i = 1;i < productSizeTags.length;i++) {
		if(productSizeTags[i].classList.contains("btn-dark")) {
			productSizeTags[i].classList.remove("btn-dark");
		}
		if(!productSizeTags[i].classList.contains("btn-primary")) {
			productSizeTags[i].classList.add("btn-primary");
		}
	}
	currProductSize.value = e.value;
	console.log(currProductSize.value);
	e.classList.remove("btn-primary");
	e.classList.add("btn-dark");
}

