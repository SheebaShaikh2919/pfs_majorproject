// prompt("check if im not at all connected");

// var x = document.getElementsByClassName("card");
// var i;
// for (i = 0; i < x.length; i++) {
//   // x[i].style.backgroundColor = "red";
//   x[i].addEventListener("click", myFunction);
// }

function myFunction() {
  prompt("Somebody is clicking");
}


// document.getElementById("tttt").onclick = () => {
//   myFunction()
// };   
// sampleFunction toggles between adding and removing the show class, which is used to hide and show the dropdown content
function sampleFunction() {
  document.getElementById("sampleDropdown").classList.toggle("show");
}

function highlightImage(e) {
	e.getElementsByTagName("input")[0].checked = true;
	// console.log(e.getElementsByTagName("input")[0].value)
	// console.log(e.getElementsByTagName("input")[0].checked)
	var inputTags = document.getElementsByName("style");
	// console.log("lol")
	for(i = 0;i < inputTags.length;i++) {
		// console.log(inputTags[i].checked)
		inputTags[i].parentElement.style.backgroundColor="rgb(255, 255, 255, 1)";
		inputTags[i].parentElement.getElementsByTagName("img")[0].style.opacity=1;
	}
	e.style.backgroundColor="rgb(153, 204, 255, 0.5)";
	e.getElementsByTagName("img")[0].style.opacity=0.5;
	// e.style.border='10px solid #000000';
}

