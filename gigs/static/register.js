const errMessage = function(message) {
    document.getElementById("error").innerHTML = message;
}

const validated = function() {
    document.getElementById("error").style.display = "none"
}

const validEmail = function(value) {
    return value !== "" && /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/.test(value)
}
const validatePassword = function(password = document.getElementById("password").value, confirmation = document.getElementById("password-confirmation").value) {
    return password === confirmation && /^.{0,128}$/.test(confirmation);
}

const isValid = function(key, value) {
    return key === "email" ? validEmail(value) :
        key === "password-confirmation" ? validatePassword() :
        value !== ""
}

const submit = document.getElementById('submit')
submit.onclick = function(event) {
    let forms = {}
    let i = 0
    for (input of document.querySelectorAll(".required")) {
        forms[input.id] = document.getElementById(input.id).value;
        if (isValid(input.id, forms[input.id])) {
            i++
        } else if (!validatePassword()) {
            event.preventDefault()
            return errMessage(`Password confirmation does not match`);
        } else {
            event.preventDefault()
            return errMessage(`${input.id} is missing`);
        }
    }
    validated()
}