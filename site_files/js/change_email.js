let submitBtn = null;
let warningInfo = {};

function handleChange(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email-field"); // TODO CHANGE THIS

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/change_email', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    if (!emailRe.test(email)) {
        const error = document.createTextNode(`That is not a valid email.`);
        errorBox.appendChild(error);
        return
    }

    xhr.onload = function() {
        if (xhr.status === 200) { // HTTP 200 = all good, logout of account
            window.location.href = '/logout';

        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            alert(`Bad Request. This shouldn't happen, submit a Github issue with this error! ${response.status}`);
        }
    };

    xhr.send(JSON.stringify({ email: email }));
}

function warnScams(btn) {
    let prompt = document.getElementById('warning-scams');
    if (btn.checked) { // This one is flipped from the rest, in this case yes = understand = gud
        prompt.style.display = "none";
        if (warningInfo.scam_info) {
            warningInfo.Remove("scam_info");
        }
    } else {
        prompt.style.display = "block";
        if (!warningInfo.scam_info) {
            warningInfo.scam_info = ""
        }
    }
    changeBtnState();
}

function warnRushing(btn) {
    let prompt = document.getElementById('warning-rush');
    if (btn.checked) { // Yes = rushing = bad
        prompt.style.display = "block";
        warningScore++;
    } else {
        prompt.style.display = "none";
        warningScore--;
    }
    changeBtnState();
}

function changeBtnState() {
    for (let w in warningInfo) {
        if (w === true) {
            submitBtn.disabled = false;
            return
        }
    }
    submitBtn.disabled = true;
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    submitBtn = document.getElementById("submit-btn");

    const urgentElements = document.getElementsByName('urgent-matter');
    const understandElements = document.getElementsByName('understand-scams');

    urgentElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {warnRushing(urgentElements[0])});
    });

    understandElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {warnScams(understandElements[0])});
    });
});