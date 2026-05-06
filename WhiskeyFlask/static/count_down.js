let secondsRemaining = Number(document.body.dataset.delaySeconds);
const countdown_elements = document.getElementsByClassName("countdown_text");

const countdownTimer = setInterval(() => {
    secondsRemaining -= 1;
    for (let i = 0; i < countdown_elements.length; i++) {
        countdown_elements[i].textContent = secondsRemaining;
    }

    if (secondsRemaining <= 0) {
        clearInterval(countdownTimer);
        window.location.href = "/redirect";
    }
}, 1000);