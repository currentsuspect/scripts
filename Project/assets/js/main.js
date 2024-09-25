document.addEventListener("DOMContentLoaded", function () {
    // Toggle between login and signup forms
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const showSignup = document.getElementById("showSignup");
    const showLogin = document.getElementById("showLogin");

    showSignup.addEventListener("click", () => {
        loginForm.classList.add("hidden");
        signupForm.classList.remove("hidden");
    });

    showLogin.addEventListener("click", () => {
        signupForm.classList.add("hidden");
        loginForm.classList.remove("hidden");
    });

    // Signup logic with role selection
    signupForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = document.getElementById("signupName").value;
        const email = document.getElementById("signupEmail").value;
        const password = document.getElementById("signupPassword").value;
        const role = document.getElementById("signupRole").value;

        let users = JSON.parse(localStorage.getItem("users")) || [];
        users.push({ name, email, password, role, available: role === 'vendor' ? false : null });
        localStorage.setItem("users", JSON.stringify(users));
        alert("Signup Successful! You can now log in.");
        signupForm.reset();
        showLogin.click();
    });

    // Login logic
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;

        let users = JSON.parse(localStorage.getItem("users")) || [];
        const user = users.find(u => u.email === email && u.password === password);
        if (user) {
            localStorage.setItem("currentUser", JSON.stringify(user));
            alert(`Welcome back, ${user.name}!`);
            redirectUser(user);
        } else {
            alert("Invalid credentials. Please try again.");
        }
    });

    // Redirect user based on role
    function redirectUser(user) {
        if (user.role === "customer") {
            window.location.href = "customer-dashboard.html";
        } else if (user.role === "vendor") {
            window.location.href = "vendor-dashboard.html";
        } else if (user.role === "admin") {
            window.location.href = "admin-dashboard.html";
        }
    }

    // Customer Dashboard: Display Available Vendors
    const vendorList = document.getElementById("vendorList");
    if (vendorList) {
        const users = JSON.parse(localStorage.getItem("users")) || [];
        const availableVendors = users.filter(user => user.role === 'vendor' && user.available);
        vendorList.innerHTML = availableVendors.length
            ? availableVendors.map(vendor => `<li>${vendor.name} is available</li>`).join('')
            : `<li>No vendors available</li>`;
    }

    // Customer Dashboard: Handle Order Submission
    const orderForm = document.getElementById("orderForm");
    if (orderForm) {
        orderForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const quantity = document.getElementById("quantity").value;

            // Get available vendors
            let users = JSON.parse(localStorage.getItem("users")) || [];
            const availableVendors = users.filter(user => user.role === 'vendor' && user.available);

            if (availableVendors.length === 0) {
                alert("No vendors are currently available to fulfill your order.");
                return;
            }

            // Assuming the first available vendor for simplicity
            const selectedVendor = availableVendors[0];

            // Confirm the order with the user
            const confirmOrder = confirm(`You are about to order ${quantity} litres of water from ${selectedVendor.name}. Do you want to proceed?`);

            if (confirmOrder) {
                alert(`You have successfully ordered ${quantity} litres of water from ${selectedVendor.name}!`);
            }

            orderForm.reset();
        });
    }

    // Vendor Dashboard: Toggle Availability
    const toggleAvailabilityBtn = document.getElementById("toggleAvailability");
    const availabilityStatus = document.getElementById("availabilityStatus");

    if (toggleAvailabilityBtn && availabilityStatus) {
        let currentUser = JSON.parse(localStorage.getItem("currentUser"));
        updateAvailabilityStatus(currentUser);

        toggleAvailabilityBtn.addEventListener("click", () => {
            // Toggle the availability status
            currentUser.available = !currentUser.available;

            // Update the user in local storage
            localStorage.setItem("currentUser", JSON.stringify(currentUser));

            // Update the displayed status
            updateAvailabilityStatus(currentUser);
        });
    }

    // Logout Functionality
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("currentUser"); // Clear current user from local storage
            window.location.href = "/index.html"; // Redirect to index page
        });
    }

    // Function to update the displayed availability status
    function updateAvailabilityStatus(user) {
        availabilityStatus.textContent = user.available ? "Currently Available" : "Currently Unavailable";
    }

    // Helper Functions
    function updateUser(user) {
        let users = JSON.parse(localStorage.getItem("users")) || [];
        const userIndex = users.findIndex(u => u.email === user.email);
        if (userIndex > -1) {
            users[userIndex] = user;
            localStorage.setItem("users", JSON.stringify(users));
            localStorage.setItem("currentUser", JSON.stringify(user));
        }
    }
});
