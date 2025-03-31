document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        let alert = document.querySelector(".alert");
        if (alert) alert.style.display = "none";
    }, 3000);
});
