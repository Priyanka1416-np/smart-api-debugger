const form = document.getElementById("apiForm");
const loader = document.getElementById("loader");

form.addEventListener("submit", () => {
    loader.style.display = "block";
});

/* Smooth scroll to result */
window.onload = () => {
    const result = document.querySelector(".result");
    if (result) {
        result.scrollIntoView({ behavior: "smooth" });
    }
};