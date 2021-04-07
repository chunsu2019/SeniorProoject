function login() {
    var userEmail = document.getElementById("inputEmail").value;
    var userPassword = document.getElementById("inputPassword").value;

    firebase.auth().signInWithEmailAndPassword(userEmail, userPassword)
        .then((userCredential) => {
            // Signed in
            var user = userCredential.user;
            //print('localId');
            //window.alert(user.uid);
            window.location = 'http://127.0.0.1:5000/login/' + user.uid;
            // ...  
        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            window.alert(errorCode + " " + errorMessage);
        });
}