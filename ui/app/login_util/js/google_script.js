function google_signOut(){
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function(){

        alert("You have been successfully signed out");

        $(".g-signin2").css("display", "block");
        $(".data").css("display", "none");
    });
}

function facebook_logOut(){
    FB.logout(function(response) {
        statusChangeCallback(response);
        document.getElementById('logout').style.display = "none";
        location.reload();
    });
    }

