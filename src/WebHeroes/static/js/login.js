const signupPassword = document.getElementById("signup-password")
const confirmPassword = document.getElementById("confirm-password")
const matchPass = document.getElementById("matchPass");
const loginShit = document.getElementById("loginWork")
const form = document.getElementById("kurwaForm");
const login = document.getElementById("login-stuff");

function comparePasswords() {
	if (signupPassword.value === "" && confirmPassword.value === "") {
		matchPass.textContent = "";
	} else if (signupPassword.value === confirmPassword.value) {
		matchPass.textContent = "✅ Passwords match!";
		matchPass.style.color = "green";
	} else {
		matchPass.textContent = "❌ Passwords do not match.";
		matchPass.style.color = "red";
	}
}

signupPassword.addEventListener("input", comparePasswords);
confirmPassword.addEventListener("input", comparePasswords);


function signupPress(event){
    event.preventDefualt();

    if (signupPassword.value === "" && confirmPassword.value === ""){
        return;
    } else if(signupPassword.value !== confirmPassword.value){
        return;
    }

    let signup_data = {
        username: document.getElementById("signup-name").value,
        password: signupPassword.value
    };
}