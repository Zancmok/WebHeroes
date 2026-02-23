/* ============================================================
   PASSWORD MATCH CHECK
   ============================================================ */
const signupPassword = document.getElementById("signup-password");
const confirmPassword = document.getElementById("confirm-password");
const matchPass       = document.getElementById("matchPass");
const loginShit       = document.getElementById("loginWork");
const form  = document.getElementById("signupForm");
const login = document.getElementById("loginForm");

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

// SIGN UP
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

    // rollDice is defined in animations.js (loaded before this file)
    rollDice(async () => {
        try {
            const response = await fetch("/user-management/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(signup_data)
            });

            const data = await response.json();

            if (response.status === 201) {
                form.reset();
                matchPass.textContent = "✅ Account created successfully!";
                matchPass.style.color = "green";
            } else if (response.status === 400) {
                matchPass.textContent = `❌ ${data.reason}`;
                matchPass.style.color = "red";
            } else if (response.status === 409) {
                matchPass.textContent = `❌ ${data.reason}`;
                matchPass.style.color = "red";
            }
        } catch (error) {
            console.error("Request failed:", error);
            matchPass.textContent = "❌ An error occurred. Please try again.";
            matchPass.style.color = "red";
        }
    });
}

form.addEventListener("submit", signupPress);

// LOGIN
async function loginPress(event) {
    event.preventDefault();

    const login_data = {
        username: document.getElementById("login-name").value,
        password: document.getElementById("login-password").value
    };

    // rollDice is defined in animations.js (loaded before this file)
    rollDice(async () => {
        try {
            const response = await fetch("/user-management/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(login_data)
            });

            const data = await response.json();

            if (response.status === 200) {
                console.log("Login successful!");
                loginShit.textContent = "✅ Login successful!";
                loginShit.style.color = "green";
                window.location.assign("/online-lobbies/");
            } else if (response.status === 400) {
                console.error("Error:", data.reason);
                loginShit.textContent = `❌ ${data.reason}`;
                loginShit.style.color = "red";
            } else if (response.status === 403) {
                console.error("Error:", data.reason);
                loginShit.textContent = `❌ ${data.reason}`;
                loginShit.style.color = "red";
            }
        } catch (error) {
            console.error("Request failed:", error);
            loginShit.textContent = "❌ An error occurred. Please try again.";
            loginShit.style.color = "red";
        }
    });
}

login.addEventListener("submit", loginPress);