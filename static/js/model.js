document.getElementById('cacc').addEventListener('click', function() {
    document.getElementById('loginform').style.display = "none";
    document.getElementById('signupform').style.display = "block";
})

document.getElementById('logacc').addEventListener('click', function() {
    document.getElementById('loginform').style.display = "block";
    document.getElementById('signupform').style.display = "none";
})

function usercheck() {
    var mail = document.getElementById("email").value;
    axios.post('auth/generateotp', {
            "email": mail,
        })
        .then(res => {
            if (res['data']['message'] == 'Success')
                alert("otp send to " + mail)
            else
                alert(res['data']['message']);
        });
}

document.getElementById("otpgen").addEventListener("click", usercheck);