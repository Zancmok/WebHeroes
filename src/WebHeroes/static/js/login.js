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


async function signupPress(event) {
    event.preventDefault();

    if (signupPassword.value === "" && confirmPassword.value === "") {
        return;
    } else if (signupPassword.value !== confirmPassword.value) {
        return;
    }

    const signup_data = {
        username: document.getElementById("signup-name").value,
        password: signupPassword.value
    };

    try {
        const response = await fetch("/user-management/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(signup_data)
        });

        const data = await response.json();

        if (response.status === 201) {
            // Success - account created
            console.log("Account created successfully!");
            // Redirect or clear form as needed
            form.reset();
            matchPass.textContent = "";
        } else if (response.status === 400) {
            // Bad request - invalid username
            console.error("Error:", data.reason);
            matchPass.textContent = `❌ ${data.reason}`;
            matchPass.style.color = "red";
        } else if (response.status === 409) {
            // Conflict - user already exists
            console.error("Error:", data.reason);
            matchPass.textContent = `❌ ${data.reason}`;
            matchPass.style.color = "red";
        }
    } catch (error) {
        console.error("Request failed:", error);
        matchPass.textContent = "❌ An error occurred. Please try again.";
        matchPass.style.color = "red";
    }
}

form.addEventListener("submit", signupPress);

async function loginPress(event) {
    event.preventDefault();

    const login_data = {
        username: document.getElementById("login-name").value,  // Changed from "login-username" to "login-name"
        password: document.getElementById("login-password").value
    };

    try {
        const response = await fetch("/user-management/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(login_data)
        });

        const data = await response.json();

        if (response.status === 200) {
            // Success - logged in
            console.log("Login successful!");
            loginShit.textContent = "✅ Login successful!";
            loginShit.style.color = "green";

            // Redirect to dashboard or home page
            window.location.assign("/online-lobbies/");
        } else if (response.status === 400) {
            // Bad request - user doesn't exist or auth failed
            console.error("Error:", data.reason);
            loginShit.textContent = `❌ ${data.reason}`;
            loginShit.style.color = "red";
        } else if (response.status === 403) {
            // Forbidden - already logged in
            console.error("Error:", data.reason);
            loginShit.textContent = `❌ ${data.reason}`;
            loginShit.style.color = "red";
        }
    } catch (error) {
        console.error("Request failed:", error);
        loginShit.textContent = "❌ An error occurred. Please try again.";
        loginShit.style.color = "red";
    }
}

login.addEventListener("submit", loginPress);