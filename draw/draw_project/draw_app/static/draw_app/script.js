document.addEventListener("DOMContentLoaded", () => {
    fetch('http://localhost:8000/get_count/')
        .then(response => response.json())
        .then(data => {
            const users = data.users;
            const participantCount = users.length;
            document.getElementById("participant-count").textContent = participantCount + " " + getCorrectWordForm(participantCount);

            const drawButton = document.getElementById("draw-winner");
            drawButton.addEventListener("click", () => drawWinner(users));
        });
});

// Function to draw winner with animation
function drawWinner(users) {
    fetch('http://localhost:8000/get_winner')
        .then(response => response.json())
        .then(data => {
            const users = data.users;
            const participantCount = users.length;
            document.getElementById("participant-count").textContent = participantCount + " " + getCorrectWordForm(participantCount);
            const animationContainer = document.getElementById("animation-container");
            const winnerAnnouncement = document.getElementById("winner-announcement");
            const winner = users.find(user => user.winner);

            let currentIndex = 0;
            let iteration = 0;
            const totalIterations = 250; // Total number of iterations for the animation
            let delay = 10; // Initial speed of the animation in milliseconds

            winnerAnnouncement.textContent = ""; // Clear any previous winner announcement

            function animate() {
                if (iteration < totalIterations) {
                    animationContainer.textContent = `Номер: ${users[currentIndex].id}`;
                    currentIndex = (currentIndex + 1) % users.length;
                    iteration += 10;

                    // Increase the delay to slow down the animation
                    delay += 10;

                    setTimeout(animate, delay);
                } else {
                    animationContainer.textContent = `Номер: ${winner.id}`;
                    winnerAnnouncement.textContent = `Участник с номером ${winner.id} - ${winner.tg_name} является победителем!`;
                    showConfetti();
                    fetch('http://localhost:8000/mailing/', {
                        method: 'POST',
                        body: JSON.stringify({
                            'tg_name': winner.tg_name
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
            }

            animate();
        });
}

// Function to get the correct word form for "человек"
function getCorrectWordForm(number) {
    const lastDigit = number % 10;
    const lastTwoDigits = number % 100;

    if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
        return 'человек';
    }

    if (lastDigit === 1) {
        return 'человек';
    }

    if (lastDigit >= 2 && lastDigit <= 4) {
        return 'человека';
    }

    return 'человек';
}

// Function to show confetti
function showConfetti() {
    const duration = 2 * 1000; // Duration of confetti in milliseconds
    const end = Date.now() + duration;

    (function frame() {
        // Launch a few confetti from the left edge
        confetti({
            particleCount: 3,
            angle: 60,
            spread: 55,
            origin: { x: 0 }
        });
        // And launch a few confetti from the right edge
        confetti({
            particleCount: 3,
            angle: 120,
            spread: 55,
            origin: { x: 1 }
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
}
