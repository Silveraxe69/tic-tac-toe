document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        const s = document.querySelector("#startup-screen");
        if (s) {
            s.style.animation = "fadeOut 1s forwards";
            setTimeout(() => {
                window.parent.postMessage({screen: "names"}, "*");
            }, 900);
        }
    }
});

/* Fade-Out keyframe injected dynamically */
var style = document.createElement("style");
style.innerHTML = `
@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}
`;
document.head.appendChild(style);

/* Listen from JS → Streamlit */
window.addEventListener("message", (event) => {
    if (event.data.screen === "names") {
        window.location.reload();
    }
});
