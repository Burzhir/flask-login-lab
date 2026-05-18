document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.getElementById('showPassword');
    var passwordField = document.getElementById('password');
    if (checkbox && passwordField) {
        checkbox.addEventListener('change', function () {
            passwordField.type = this.checked ? 'text' : 'password';
        });
    }
});
