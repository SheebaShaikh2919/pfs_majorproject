function selectSize(e) {
	var otherSizeOptions = e.parentElement.getElementsByTagName("input");
	for(var i = 1;i < otherSizeOptions.length;i++) {
		if(otherSizeOptions[i].classList.contains("btn-dark")) {
			otherSizeOptions[i].classList.remove("btn-dark");
		}
		if(!otherSizeOptions[i].classList.contains("btn-primary")) {
			otherSizeOptions[i].classList.add("btn-primary");
		}
	}
	var selectedSize = e.parentElement.getElementsByTagName("input")[0];
	selectedSize.value = e.value;
	e.classList.remove("btn-primary");
	e.classList.add("btn-dark");
}

function changeStatusInCart(e) {
	var prevInnerHTML = e.innerHTML;
	e.innerHTML = "<span class='spinner-grow spinner-grow-md' role='status' aria-hidden='true'></span>Loading...";

	var minTimeoutValue = 100;
	var maxTimeoutValue = 1000;
	var timeoutValue = Math.random() * (maxTimeoutValue - minTimeoutValue) + minTimeoutValue;
	// Math.random() is [0, 1)
	// Lol class 11th maths
	setTimeout(() => {
		var selectedSize = e.parentElement.parentElement.getElementsByTagName("input")[0];
		if(selectedSize.value == "") {
			alert("Please select a size");
			e.innerHTML = prevInnerHTML;
			return true;
		}
		var cartStatus = e.parentElement.getElementsByTagName("input")[0];
		if(cartStatus.value == "n") {
			cartStatus.value = "y";
			e.innerHTML = "Remove From Cart";
		}
		else if(cartStatus.value == "y") {
			cartStatus.value = "n";
			e.innerHTML = "Add To Cart";
		}
	}, timeoutValue);
}

