function handleLogin(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    const emailRe = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/;

    const email = document.getElementById('email-field').value;
    const password = document.getElementById('password-field').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    if (!emailRe.test(email)) {
        errorBox.textContent = `That is not a valid email.`;
        return
    }

    xhr.onload = function() {
        if (xhr.status === 200) { // HTTP 200 = login :yay:
            window.location.href = '/settings';

        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            errorBox.textContent = `Bad Request. This shouldn't happen, submit a Github issue with this error: ${response.status}`;

        } else if (xhr.status === 401) { // HTTP 401 = Unauthorized
            errorBox.textContent = `Wrong password/username, pls try again.`;
        }
    };

    xhr.send(JSON.stringify({ email: email, password: password }));
}

function showPassword() {
    if (document.getElementById('show-pw').checked) {
        document.getElementById('password-field').type="text";
    } else {
        document.getElementById('password-field').type="password";
    }
}