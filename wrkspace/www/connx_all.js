
var action = "";
var caisse = "";

function voirLog() {
	alert("voir log");
}

function fairecible(action, caisse) {
	//alert("faire " + action + " sur cible " + caisse);
	document.getElementById("valFaire").value = action;
	document.getElementById("valCible").value = caisse;
	// pour browser modernes .textContent
	document.getElementById("display").innerHTML = "faire " + action + " sur cible " + caisse;
	document.getElementById("frm1").submit();
}


function faire(btn) {
	//alert(btn.name);
	action = btn.id;
	//alert(action);
	if (caisse != "") {
		//alert("action=" + action);
		fairecible(action, caisse);
		caisse = "";
		action = "";
	}
	
}


function cible(btn) {
	caisse = btn.id;
	//alert(caisse);
	if (action != "") {
		//alert("Caisse");
		fairecible(action, caisse);
		caisse = "";
		action = "";
	}
}