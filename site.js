document.querySelectorAll("[data-current-year]").forEach((element) => {
    element.textContent = new Date().getFullYear();
});

document.querySelectorAll("a.app-feature-image").forEach((link) => {
    const image = link.querySelector("img");
    const updateSource = () => {
        link.href = image.currentSrc || image.src;
    };

    image.addEventListener("load", updateSource);
    link.addEventListener("click", updateSource);
    link.addEventListener("contextmenu", updateSource);
    link.addEventListener("auxclick", updateSource);
    updateSource();
});
