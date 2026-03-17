const signupPassword = document.getElementById("signup-password");
const confirmPassword = document.getElementById("confirm-password");
const matchPass       = document.getElementById("matchPass");
const loginWork       = document.getElementById("loginWork");
const form            = document.getElementById("signupForm");
const loginForm       = document.getElementById("loginForm");

function comparePasswords() {
    if (signupPassword.value === "" && confirmPassword.value === "") {
        matchPass.textContent = "";
        matchPass.className = "";
    } else if (signupPassword.value === confirmPassword.value) {
        matchPass.textContent = "✅ Passwords match!";
        matchPass.className = "msg-ok";
    } else {
        matchPass.textContent = "❌ Passwords do not match.";
        matchPass.className = "msg-err";
    }
}

signupPassword.addEventListener("input", comparePasswords);
confirmPassword.addEventListener("input", comparePasswords);


async function signupPress(event) {
    event.preventDefault();

    if (signupPassword.value === "" && confirmPassword.value === "") return;
    if (signupPassword.value !== confirmPassword.value) return;

    const signup_data = {
        username: document.getElementById("signup-name").value,
        password: signupPassword.value
    };

    // rollDice is defined in sharedAnims.js (loaded before this file)
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
                matchPass.className = "msg-ok";
            } else if (response.status === 400 || response.status === 409) {
                matchPass.textContent = `❌ ${data.reason}`;
                matchPass.className = "msg-err";
            }
        } catch (error) {
            console.error("Signup request failed:", error);
            matchPass.textContent = "❌ An error occurred. Please try again.";
            matchPass.className = "msg-err";
        }
    });
}

form.addEventListener("submit", signupPress);

async function loginPress(event) {
    event.preventDefault();

    const login_data = {
        username: document.getElementById("login-name").value,
        password: document.getElementById("login-password").value
    };

    // rollDice is defined in sharedAnims.js (loaded before this file)
    rollDice(async () => {
        try {
            const response = await fetch("/user-management/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(login_data)
            });

            const data = await response.json();

            if (response.status === 200) {
                loginWork.textContent = "✅ Login successful!";
                loginWork.className = "msg-ok";
                window.location.assign("/online-lobbies/");
            } else if (response.status === 400 || response.status === 403) {
                console.error("Login error:", data.reason);
                loginWork.textContent = `❌ ${data.reason}`;
                loginWork.className = "msg-err";
            }
        } catch (error) {
            console.error("Login request failed:", error);
            loginWork.textContent = "❌ An error occurred. Please try again.";
            loginWork.className = "msg-err";
        }
    });
}

loginForm.addEventListener("submit", loginPress);

//tab animation
function revealFormItems(paneId) {
    const pane = document.getElementById(paneId);
    if (!pane) return;
    const items = pane.querySelectorAll('.form-item');
    items.forEach(item => {
        item.classList.remove('visible');
        item.style.transitionDelay = '0s';
    });
    requestAnimationFrame(() => {
        items.forEach((item, i) => {
            item.style.transitionDelay = (i * 0.1 + 0.1) + 's';
            setTimeout(() => item.classList.add('visible'), 20);
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    revealFormItems('signup');

    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            const target = e.target.getAttribute('href').replace('#', '');
            revealFormItems(target);
        });
    });
});