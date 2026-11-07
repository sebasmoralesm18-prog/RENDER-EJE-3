document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById("password");
    const toggle = document.getElementById("togglePassword");

    toggle.addEventListener("click", () => {
        password.type =
            password.type === "password" ? "text" : "password";
    });
});