document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector(".sticky-header");
    if (header) {
        window.addEventListener("scroll", () => {
            header.style.backgroundColor = "#000";
        });
    }

    // Добавление бегущей строки
    const marqueeText = document.querySelector(".marquee");
    if (marqueeText) {
        marqueeText.innerHTML = "Внимание! Все запросы обрабатываются в порядке живой очереди в течении суток!";
    }
});
