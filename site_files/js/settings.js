function handleSettingsEmail(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");
    const emailRe = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/;
    const email = document.getElementById('email-field').value;

    if (!emailRe.test(email)) {
        const error = document.createTextNode(`That is not a valid email.`);
        errorBox.appendChild(error);
        return
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/change_email', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    if (!emailRe.test(email)) {
        const error = document.createTextNode(`That is not a valid email.`);
        errorBox.appendChild(error);
        return
    }

    xhr.onload = function() {
        if (xhr.status === 200) { // HTTP 200 = all good, logout of account
            window.location.href = '/change_email';

        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            const error = document.createTextNode(`Bad Request. This shouldn't happen, submit a Github issue with this error! ${response.status}`);
            errorBox.appendChild(error);

        }
    };

    xhr.send(JSON.stringify({ email: email }));
}