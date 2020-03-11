function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    $(".g-signin2").css("display", "none");
    $(".data").css("display", "block");
    $("#pic").attr('src',  profile.getImageUrl());
    $("#email").text(profile.getEmail());
    $("#name").text(profile.getName());
    window.location.href = "c_homepage.html";
}

function google_signOut(){
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function(){

        alert("You have been successfully signed out");

        $(".g-signin2").css("display", "block");
        $(".data").css("display", "none");
    });
}


function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

function facebook_logOut(){
FB.logout(function(response) {
    statusChangeCallback(response);
    document.getElementById('logout').style.display = "none";
    location.reload();
});
}