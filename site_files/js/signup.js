function handleSignup(event) {
    event.preventDefault();
    const errorBox = document.getElementById("error-msg");

    const emailRe = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/;

    const email = document.getElementById('email-field').value;
    const password = document.getElementById('password-field').value;
    const rePassword = document.getElementById('re-password-field').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    if (password !== rePassword) {
        errorBox.textContent = `The password fields do not match.`;
        errorBox.appendChild(error);
        return
    }

    if (!emailRe.test(email)) {
        errorBox.textContent = `That is not a valid email.`;
        return
    }

    xhr.onload = function() {
        if (xhr.status === 201) { // HTTP 201 = resource created, aka new user!
            window.location.href = '/settings';

        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            errorBox.textContent = `Bad Request. This shouldn't happen, submit a Github issue with this error: ${response.status}`;

        } else if (xhr.status === 409) { // HTTP 409 = Email taken ):
            errorBox.textContent = `This email has already been registered. ): Use another one.`;
        }
    };

    xhr.send(JSON.stringify({ email: email, password: password }));
}

function showPassword() {
    if (document.getElementById('show-pw').checked) {
        document.getElementById('re-password-field').type="text";
        document.getElementById('password-field').type="text";
    } else {
        document.getElementById('re-password-field').type="password";
        document.getElementById('password-field').type="password";
    }
}