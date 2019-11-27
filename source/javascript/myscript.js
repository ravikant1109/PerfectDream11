function saveuser() {
	email = document.getElementById("Semail").value
	pass = document.getElementById("Spass").value
	vpass = document.getElementById("Svpass").value
	if (pass==vpass){
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				alert(this.responseText);
			}
		};
		xhttp.open("GET", "cgi-bin/saveuser.py?email="+email+"&pass="+pass, true);
		xhttp.send();
	}
	else{
		alert("Password didn't match");
	}
}
function loginuser() {
	email = document.getElementById("lemail").value
	pass = document.getElementById("lpass").value
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
			if(this.responseText.length == 18){
				document.cookie = "set";
			}
			alert(this.responseText);
		}
	};
	xhttp.open("GET", "cgi-bin/loginuser.py?email="+email+"&pass="+pass, true);
	xhttp.send();
}





