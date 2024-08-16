function handleChange(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    const email = document.getElementById('email-field').value;
    const password = document.getElementById('password-field').value;

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
            const error = document.createTextNode(`Bad Request. This shouldn't happen, submit a Github issue with this error! ${response.status}`);
            errorBox.appendChild(error);

        }
    };

    xhr.send(JSON.stringify({ email: email }));
}