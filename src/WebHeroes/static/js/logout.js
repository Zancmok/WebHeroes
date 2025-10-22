const backButton = document.getElementById("back");

async function logoutPress(event) {
    event.preventDefault();

    try {
        const response = await fetch("/user-management/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (response.status === 200) {
            // Success - logged out
            console.log("Logout successful!");
            
            // Redirect to login/home page
            window.location.assign("/");
        } else if (response.status === 403) {
            // Not logged in
            console.error("Error:", data.reason);
            alert(`❌ ${data.reason}`);
        }
    } catch (error) {
        console.error("Request failed:", error);
        alert("❌ An error occurred. Please try again.");
    }
}

// Add event listener to the BACK button for logout
backButton.addEventListener("click", logoutPress);