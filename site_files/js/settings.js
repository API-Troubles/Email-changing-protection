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

    event.currentTarget.submit()
}