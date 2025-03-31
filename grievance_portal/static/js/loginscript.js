document.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {
        let alert = document.querySelector(".alert");
        if (alert) alert.style.display = "none";
    }, 3000);
});


document.addEventListener("DOMContentLoaded", function () {

    // Check if we are on the login page by checking if the username field exists
    let usernameField = document.getElementById("username");
    let passwordField = document.getElementById("password");

    if (usernameField && passwordField) {
        usernameField.value = "";
        passwordField.value = "";
    }
});








