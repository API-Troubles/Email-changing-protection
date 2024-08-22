let submitBtn = null;
let warningInfo = {rushing: false, scam_info: false};

function handleChange(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email-field");

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

function warnWhyChange(btn) {
    let selectedValue = document.querySelector('input[name=why-change-email]:checked')
    let prompt = document.getElementById('warning-why');
    if (['own-choice', 'trusted-family'].includes(selectedValue.value)) {
        prompt.style.display = "none";
        warningInfo.scam_info = false;
    } else {
        prompt.style.display = "block";
        warningInfo.scam_info = true
    }
    changeBtnState();
}

function warnScams(btn) {
    let prompt = document.getElementById('warning-scams');
    if (btn.checked) { // This one is flipped from the rest, in this case yes = understand = gud
        prompt.style.display = "none";
        warningInfo.scam_info = false;
    } else {
        prompt.style.display = "block";
        warningInfo.scam_info = true
    }
    changeBtnState();
}

function warnRushing(btn) {
    let prompt = document.getElementById('warning-rush');
    if (btn.checked) { // Yes = rushing = bad
        prompt.style.display = "block";
        warningInfo.rushing = true;
    } else {
        prompt.style.display = "none";
        warningInfo.rushing = false;
    }
    changeBtnState();
}

function changeBtnState() {
    for (let w in warningInfo) {
        console.log(w)
        if (warningInfo[w] === true) {
            submitBtn.disabled = true;
            return
        }
    }
    submitBtn.disabled = false;
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    submitBtn = document.getElementById("submit-btn");

    const urgentElements = document.getElementsByName('urgent-matter');
    const understandElements = document.getElementsByName('understand-scams');
    const reasonElements = document.getElementsByName('why-change-email');

    urgentElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {warnRushing(urgentElements[0])});
    });

    understandElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {warnScams(understandElements[0])});
    });

        reasonElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {warnWhyChange(reasonElements)});
    });
});