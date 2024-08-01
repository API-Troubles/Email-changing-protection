function handleLogin(event) {
    event.preventDefault();

    const emailRe = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/;

    const email = document.getElementById('email-field').value;
    const password = document.getElementById('password-field').value;
    const rePassword = document.getElementById('re-password-field').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    if (password !== rePassword) {
        alert("The password fields do not match")
        return
    }

    if (!emailRe.test(email)) {
        alert("Woah thats not an email!")
        return
    }

    xhr.onload = function() {
        if (xhr.status === 201) { // HTTP 201 = resource created, aka new user!
            window.location.href = '/settings';
        } else if (xhr.status === 400) { // HTTP 400 = bad request
            const response = JSON.parse(xhr.responseText);
            alert(response.status);
        } else if (xhr.status === 409) { // HTTP 409 = Email taken ):
            alert("Email taken already!");
        }
    };

    xhr.send(JSON.stringify({ email: email, password: password }));
}