window.onload = function () {
    if (window.history && window.history.pushState) {
        window.history.pushState(null, null, document.URL);
        window.addEventListener("popstate", function () {
            window.history.pushState(null, null, document.URL);
        });
    }
};

// Clear session storage & local storage after logout
sessionStorage.clear();
localStorage.clear();


window.addEventListener("beforeunload", function () {
    fetch("/logout/", { method: "GET", credentials: "same-origin" });
});