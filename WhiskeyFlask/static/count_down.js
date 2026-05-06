let secondsRemaining = Number(document.body.dataset.secondsRemaining);
const countdown_element = document.getElementById("countdown");

function formatTime(seconds) {
    const days = Math.floor(seconds / (24 * 3600));
    seconds %= (24 * 3600);
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);

    let parts = [];
    if (days > 0) parts.push(`${days} Days`);
    if (hours > 0 || days > 0) parts.push(`${hours} Hours`);
    parts.push(`${minutes} Minutes`);
    parts.push(`${secs} Seconds`);

    return parts.join(", ");
}

const countdownTimer = setInterval(() => {
    secondsRemaining -= 1;
    if (countdown_element) {
        countdown_element.textContent = formatTime(secondsRemaining);
    }

    if (secondsRemaining <= 0) {
        clearInterval(countdownTimer);
        if (countdown_element) {
            countdown_element.textContent = "Arrived!";
        }
    }
}, 1000);