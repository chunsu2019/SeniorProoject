var today = new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().split("T")[0];

document.getElementById("date").value = today;
document.getElementById("date").max = today;

//Firebase login
function login() {
    var userEmail = document.getElementById("inputEmail").value;
    var userPassword = document.getElementById("inputPassword").value;

    firebase.auth().signInWithEmailAndPassword(userEmail, userPassword)
        .then((userCredential) => {
            var user = userCredential.user;

            uid = user.uid;

            window.location.href = 'http://127.0.0.1:5000/home'
        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            window.alert(errorCode + " " + errorMessage);
        });
}

//
$('select').on('change', function (e) {

    switch (this.value) {
        //show 0
        case "0":
            //hide and clear other
            clearForm(1);

            //display
            document.getElementById("form0").style.display = "block";

            document.getElementById("form_submit_btn").style.display = "block";
            
            break;

        //show 1
        case "1":
            //hide and clear other
            clearForm(0);

            //display
            document.getElementById("form1").style.display = "block";

            document.getElementById("form_submit_btn").style.display = "block";
            break;

        default:
            //clear all
            clearForm(3);

            document.getElementById("form_submit_btn").style.display = "none";

    }
});

function clearForm(form) {
    if (form == 0) {
        document.getElementById("form0").style.display = "none";
        document.getElementById("feet").value = "";
        document.getElementById("inches").value = "";
        document.getElementById("weight").value = "";
        document.getElementById("age").value = "";

        //
        document.getElementById("feet").removeAttribute("required");
        document.getElementById("inches").removeAttribute("required");
        document.getElementById("weight").removeAttribute("required");
        document.getElementById("age").removeAttribute("required");
    }
    else if (form == 1) {
        document.getElementById("form1").style.display = "none";
        document.getElementById("reading").value = "";
        document.getElementById("dynamicInput").innerHTML = "";

        //
        document.getElementById("reading").removeAttribute("required");
        document.getElementById("date").removeAttribute("required");
    }
    else {
        //Form0
        document.getElementById("form0").style.display = "none";
        document.getElementById("feet").value = "";
        document.getElementById("inches").value = "";
        document.getElementById("weight").value = "";
        document.getElementById("age").value = "";

        //Form1
        document.getElementById("form1").style.display = "none";
        document.getElementById("reading").value = "";
        document.getElementById("dynamicInput").innerHTML = "";
    }
}


$("#add").click(function () {
    var html = '';
    html += '<div class="row" id="dynamicRow">';

    html += '<div class="col-5">';
    html += '<input type="date" id="start" name="trip-start" value="' + today + '" min="" max="' + today + '" required="true">';
    html += '</div>';

    html += '<div class="col-4">';
    html += '<input type="email" class="form-control" name="reading" id="reading" placeholder="Reading.." required="true">';
    html += '</div>';
    html += '<div class="col-1">';
    html += '<button id="removeRow" type="button" class="btn btn-danger">Remove</button>';
    html += '</div>';

    html += '<hr class="mt-3">';

    html += '</div>';


    $('#dynamicInput').append(html);
});

$(document).on('click', '#removeRow', function () {
    $(this).closest('#dynamicRow').remove();
});
