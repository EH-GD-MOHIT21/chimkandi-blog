document.getElementById('cacc').addEventListener('click', function() {
    document.getElementById('loginform').style.display = "none";
    document.getElementById('signupform').style.display = "block";
})

document.getElementById('logacc').addEventListener('click', function() {
    document.getElementById('loginform').style.display = "block";
    document.getElementById('signupform').style.display = "none";
})

document.getElementById('fp2log').addEventListener('click', function() {
    document.getElementById('loginform').style.display = "block";
    document.getElementById('fpform').style.display = "none";
})

document.getElementById('facc').addEventListener('click', function() {
    document.getElementById('loginform').style.display = 'none';
    document.getElementById('fpform').style.display = 'block';
})

function usercheck() {
    document.getElementById("otpgen").disabled = true;
    var mail = document.getElementById("email").value;
    axios.post('/auth/generateotp', {
            "email": mail,
        })
        .then(res => {
            document.getElementById("otpgen").disabled = false;
            if (res['data']['message'] == 'Success') {
                alert("otp send to " + mail)
            } else
                alert(res['data']['message']);
        });
}

function setfpjs() {
    var mail = document.getElementById("fpemail").value;
    axios.post('/auth/generatefp', {
            "email": mail,
        })
        .then(res => {
            if (res['data']['message'] == 'success') {
                document.getElementById('aria-fp-invisible').style.display = 'block';
                document.getElementById('emailfpico').style.top = "8.5%";
            } else
                alert(res['data']['message']);
        });
}

function finalfpjs() {
    var mail = document.getElementById("fpemail").value;
    var otp = document.getElementById("fpotp").value;
    var fpp1 = document.getElementById("fpp1").value;
    var fpp2 = document.getElementById("fpp2").value;
    if (fpp1 != fpp2 || fpp1.length < 8) {
        alert("please use strong password, use caps letter, numbers and special chars and both should match")
    }
    axios.post('/auth/matchfp', {
            "email": mail,
            "otp": otp,
            "password": fpp1,
            "cpassword": fpp2
        })
        .then(res => {
            if (res['data']['message'] == 'success') {
                window.location.reload();
            } else
                alert(res['data']['message']);
        });
}

document.getElementById("otpgen").addEventListener("click", usercheck);
document.getElementById("fpotpgen").addEventListener("click", setfpjs);
document.getElementById("res-btn").addEventListener("click", finalfpjs);