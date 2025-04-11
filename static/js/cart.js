const navbarCart = document.getElementById("navbarCart");
const cartButton = document.getElementById("cartButton");
const minCartQty = 0, maxCartQty = 5;

$(document).ready(function(){
    navbarCart.style.marginTop = (cartButton.offsetTop).toString() + "px";
    navbarCart.style.right = (cartButton.offsetWidth / 2).toString() + "px";
    // console.log(navbarCart.style.right);
});

function fadeToggleCart() {
    if(navbarCart.style.display == "block") {
        navbarCart.style.display = "none";
    }
    else if(navbarCart.style.display == "none") {
        navbarCart.style.display = "block";
    }
}

function showProductImg(e) {
    var product_image = e.getElementsByClassName("product_image")[0];
    product_image.style.display = "block";
}
function hideProductImg(e) {
    var product_image = e.getElementsByClassName("product_image")[0];
    product_image.style.display = "none";
}

// Handle cart quantity
function disableQty(e) {
    e.style.color = "#a6a6a6";
}
function enableQty(e) {
    e.style.color = "black";
}
var decQtyClass = document.getElementsByClassName("decQty");
var cartQtyClass = document.getElementsByClassName("cartQty");
var incQtyClass = document.getElementsByClassName("incQty");
for(var i = 0;i < cartQtyClass.length;i++) {
    var n = parseInt(cartQtyClass[i].innerHTML);
    if(n <= minCartQty) {
        disableQty(decQtyClass[i]);
    }
    if(n >= maxCartQty) {
        disableQty(incQtyClass[i]);
    }
}
function  changeCartQuantity(e, changeValue) {
    try {
        e.parentElement.getElementsByClassName("isUpdated")[0].value = "y";
    }
    catch(err) {
        console.log(err);
    }

    var decQtyTag = e.parentElement.getElementsByClassName("decQty")[0];
    var incQtyTag = e.parentElement.getElementsByClassName("incQty")[0];
    var quantityTag = e.parentElement.getElementsByTagName("span")[0];
    var quantityTagNewValue = parseInt(quantityTag.innerHTML) + changeValue;

    enableQty(decQtyTag);
    enableQty(incQtyTag);
    if(quantityTagNewValue == minCartQty) {
        disableQty(decQtyTag);
    }
    if(quantityTagNewValue == maxCartQty) {
        disableQty(incQtyTag);
    }
    if(quantityTagNewValue < minCartQty) {
        disableQty(decQtyTag);
        return false;
    }
    if(quantityTagNewValue > maxCartQty) {
        disableQty(incQtyTag);
        return false;
    }
    quantityTag.innerHTML = quantityTagNewValue;
    try {
        var total_price = e.parentElement.parentElement.getElementsByClassName("total_price")[0];
        var unit_price = e.parentElement.parentElement.getElementsByClassName("unit_price")[0];
        var prev_total_price = parseFloat(total_price.innerHTML);
        total_price.innerHTML = " " + quantityTagNewValue * parseFloat(unit_price.innerHTML);
        var new_total_price = parseFloat(total_price.innerHTML);
        updateTotalPayable(new_total_price - prev_total_price);
    }
    catch(err) {
        console.log(err);
    }
}

function updateTotalPayable(changeValue) {
    var total_payable = document.getElementById("total_payable");
    total_payable.innerHTML = " " + (parseFloat(total_payable.innerHTML) + changeValue);
}

var deletedProductsArr = new Array();
function deleteProduct(e) {
    var cartId = e.parentElement.parentElement.getElementsByClassName("cartId")[0].value;
    var total_price = parseFloat(e.parentElement.parentElement.getElementsByClassName("total_price")[0].innerHTML);
    updateTotalPayable(0 - total_price);
    deletedProductsArr.push(cartId);
    e.parentElement.parentElement.remove();
}

function saveCart() {
    var tableRows = document.getElementsByTagName("tr");
    var csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0];
    var cartId = document.getElementsByClassName("cartId");
    var cartQty = document.getElementsByClassName("cartQty");
    var isUpdated = document.getElementsByClassName("isUpdated");
    var productArr = new Array();
    var numProducts = 0;
    var rowsToBeRemoved = new Array();
    for(var i = 0;i < cartId.length;i++) {
        if(isUpdated[i].value == 'y') {
            curr = {
                "0": cartId[i].value,
                "1": cartQty[i].innerHTML
            }
            if(cartQty[i].innerHTML == '0') {
                // Since heading of table also present
                // in the list so we store i + 1 as index of row
                rowsToBeRemoved.push(i + 1);
            }
            productArr.push(curr);
            numProducts++;
        }
    }
    while(deletedProductsArr.length > 0) {
        curr = {
            "0": deletedProductsArr[deletedProductsArr.length - 1],
            "1": 0
        }
        productArr.push(curr);
        deletedProductsArr.pop();
        numProducts++;
    }
    if(numProducts == 0) {
        return false;
    }
    while(rowsToBeRemoved.length > 0) {
        tableRows[rowsToBeRemoved[rowsToBeRemoved.length - 1]].remove();
        rowsToBeRemoved.pop();
    }
    post_data = {
        "product_list_len": numProducts,
        "product_list": productArr,
        'csrfmiddlewaretoken': csrftoken.value
    }
    $.post("/api/update-product-quantity", post_data,
        function(data) {
            if(data == "success") {
                return true;
            }
            return false;
        }
    );
}
