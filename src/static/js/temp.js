document.addEventListener("DOMContentLoaded", function () {
    // API endpoint
    const apiUrl = "/get-basic-user-data/";

    // Fetch user data
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Handle the data received from the server

            // Get DOM elements to update
            const nameDisplay = document.getElementById("nameDisplay");
            const ratingDisplay = document.getElementById("ratingDisplay");
            const pfpDisplay = document.getElementById("pfp-display");

            // Check if data is empty (e.g., user is not logged in)
            if (Object.keys(data).length === 0) {
                // If no user data, set default text for name, rating, and avatar
                nameDisplay.textContent = "Guest";
                ratingDisplay.textContent = "No rating available";
                pfpDisplay.src = "";  // You could set a default avatar if desired
                pfpDisplay.alt = "Default Avatar";
            } else {
                // Populate the user data into the HTML elements
                nameDisplay.textContent = data.username || "Unknown";  // Username
                ratingDisplay.textContent = data.rating || "No rating available";  // Rating (If available)
                pfpDisplay.src = data.avatar_url || "";  // Avatar image
                pfpDisplay.alt = data.username ? `${data.username}'s Avatar` : "User Avatar";  // Alt text for image
            }
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
            document.getElementById("user-data").innerHTML = "<p>Error loading user data. Please try again later.</p>";
        });
});
