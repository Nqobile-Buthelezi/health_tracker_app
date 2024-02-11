function validateForm() {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Passwords don't match!");
        return false; // Prevent form submission
    }
    // Add more checks if you like (empty fields, password length...)
}