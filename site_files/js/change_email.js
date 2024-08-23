let submitBtn = null;
let warningInfo = {rushing: null, scam_info: null, why_change: null, decision: null, remote_access: null, ownership: null};

function handleChange(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    let urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email-field");
    console.log(email);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/change_email', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) { // HTTP 200 = all good, go back to settings
            window.location.href = '/settings';

        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            alert(`Bad Request. This shouldn't happen, submit a Github issue with this error! ${response.status}`);
        }
    };

    xhr.send(JSON.stringify({ email: email }));
}

function changeBtnState() {
    for (let w in warningInfo) {
        if (warningInfo[w] === true || warningInfo[w] === null) {
            console.log(`Flagged at ${w}`)
            submitBtn.disabled = true;
            if (warningInfo[w] === true) {
                document.getElementById('warning-support').style.display = "block";
            }
            return
        }
    }
    document.getElementById('warning-support').style.display = "none";
    submitBtn.disabled = false;
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    submitBtn = document.getElementById("submit-btn");

    const ownershipElements = document.getElementsByName('own-email');
    const remoteAccessElements = document.getElementsByName('remote-access');
    const decisionElements = document.getElementsByName('decision-own');
    const reasonElements = document.getElementsByName('why-change-email');
    const understandElements = document.getElementsByName('understand-scams');
    const urgentElements = document.getElementsByName('urgent-matter');

    ownershipElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let prompt = document.getElementById('warning-ownership');
            if (ownershipElements[0].checked) {
                prompt.style.display = "none";
                warningInfo.ownership = false;
            } else {
                prompt.style.display = "block";
                warningInfo.ownership = true; // Bit counterintuitive, stands for flagging this as a warning, so true doesn't mean ownership
            }
            changeBtnState();
        });
    });

    remoteAccessElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let prompt = document.getElementById('warning-access');
            if (remoteAccessElements[0].checked) {
                prompt.style.display = "block";
                warningInfo.remote_access = true;
            } else {
                prompt.style.display = "none";
                warningInfo.remote_access = false;
            }
            changeBtnState();
        });
    });

    decisionElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let prompt = document.getElementById('warning-decision');
            if (decisionElements[0].checked) {
                prompt.style.display = "none";
                warningInfo.decision = false;
            } else {
                prompt.style.display = "block";
                warningInfo.decision = true;
            }
            changeBtnState();
        });
    });

    reasonElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let selectedValue = document.querySelector('input[name=why-change-email]:checked')
            let prompt = document.getElementById('warning-why');
            if (['own-choice', 'trusted-family'].includes(selectedValue.value)) {
                prompt.style.display = "none";
                warningInfo.why_change = false;
            } else {
                prompt.style.display = "block";
                warningInfo.why_change = true;
            }
            changeBtnState();
        });
    });

    understandElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let prompt = document.getElementById('warning-scams');
            if (understandElements[0].checked) { // yes = understand = gud
                prompt.style.display = "none";
                warningInfo.scam_info = false;
            } else {
                prompt.style.display = "block";
                warningInfo.scam_info = true;
            }
            changeBtnState();
        });
    });

    urgentElements.forEach(radioBtn => {
        radioBtn.addEventListener('change', () => {
            let prompt = document.getElementById('warning-rush');
            if (urgentElements[0].checked) { // Yes = rushing = bad
                prompt.style.display = "block";
                warningInfo.rushing = true;
            } else {
                prompt.style.display = "none";
                warningInfo.rushing = false;
            }
            changeBtnState();
        });
    });
});