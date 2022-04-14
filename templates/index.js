let wordlesPlayed = 0;
let wordlesSolved = 0;

const headers = {
        "Content-Type": "application/json"
    };

const statusClasses = {
    0: "correct-char",
    1: "wrong-char",
    2: "correct-char-wrong-position",
};

const charBoxes = document.querySelectorAll(".tile-box");
const logBox = document.querySelector("#log-content");
const statistics = document.querySelectorAll(".log > div > span");


function clearGuesses() {
    charBoxes.forEach((box) => {
        box.innerHTML = "";
        box.classList.remove(...Object.values(statusClasses));
    });
}

function clearStatistics() {
    wordlesPlayed = 0;
    wordlesSolved = 0;
    statistics[0].innerHTML = `${wordlesSolved}/${wordlesPlayed}`;
    statistics[1].innerHTML = `0%`;
}

/**
 * 
 * @param {Record<string, any>[]} guesses 
 */
function setGuesses(guesses) {
    try {
        let index = 0;
        guesses.forEach(({ word, status }) => {
            [...word].forEach((char, charIndex) => {
                const box = charBoxes[index];
                box.innerHTML = char;
                box.classList.add(statusClasses[status[charIndex]]);
                index += 1;
            })
        });
    } catch(err) {
        // console.error(err);
    }
}

/**
 * 
 * @param {boolean} hasWon 
 */
function setStatistics(hasWon) {
    try {
        wordlesPlayed += 1;
        if (hasWon) {
            wordlesSolved += 1;
        }

        const fullPercentage = (wordlesSolved / wordlesPlayed) * 100;
        const percentage = fullPercentage < 100 ? fullPercentage.toFixed(2) : fullPercentage;
        statistics[0].innerHTML = `${wordlesSolved}/${wordlesPlayed}`;
        statistics[1].innerHTML = `${percentage}%`;
    } catch (err) {
        // console.error(err);
    }
}

function reset() {
    clearGuesses();
    clearStatistics();
    logBox.textContent = "";
}

async function triggerSolve() {
    try {

        const result = await fetch("/api/solve", {
            headers,
        });
        if (result.ok) {
            const results = await result.json();
            if (results) {
                clearGuesses();
                setGuesses(results.guesses);
                setStatistics(results.word_solved);
                logBox.textContent = JSON.stringify(results, undefined, 2)
            }
        }
    } catch(err) {
        // console.error(err);
    }
}
