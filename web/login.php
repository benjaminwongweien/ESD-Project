<!DOCTYPE html>
<html>
<head>
  <title>Facebook Login JavaScript Example</title>
  <meta charset="UTF-8">
  <meta name="google-signin-client_id" content="520394046268-urbu2ec5h4hadfqf6ach7487qgg3tfsp.apps.googleusercontent.com">
  <script src="https://apis.google.com/js/platform.js" async defer></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
  <script src="script.js"></script>
  <script>
    function statusChangeCallback(response) {  // Called with the results from FB.getLoginStatus().
      console.log('statusChangeCallback');
      console.log(response);                   // The current login status of the person.
      if (response.status === 'connected') {   // Logged into your webpage and Facebook.
        testAPI();
      } else {                                 // Not logged into your webpage or we are unable to tell.
        document.getElementById('status').innerHTML = 'Please log ' +
          'into this webpage.';
      }
    }


    function checkLoginState() {               // Called when a person is finished with the Login Button.
      FB.getLoginStatus(function(response) {   // See the onlogin handler
        statusChangeCallback(response);
      });
    }


    window.fbAsyncInit = function() {
      FB.init({
        appId      : '201004657801578',
        xfbml      : true,                     // Parse social plugins on this webpage.
        version    : 'v6.0'           // Use this Graph API version for this call.
      });


      FB.getLoginStatus(function(response) {   // Called after the JS SDK has been initialized.
        statusChangeCallback(response);        // Returns the login status.
      });
    };


    (function(d, s, id) {                      // Load the SDK asynchronously
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));


    function testAPI() {                      // Testing Graph API after login.  See statusChangeCallback() for when this call is made.
      console.log('Welcome!  Fetching your information.... ');
      FB.api('/me', function(response) {
        console.log('Successful login for: ' + response.name);
        document.getElementById('status').innerHTML =
          'Thanks for logging in, ' + response.name + '!';
        document.getElementById('logout').style.display = "block";
        document.getElementById('g-signin2').style.display = "none";
        document.getElementById('data').style.display = "none";
      });
    }

    function logOut(){
      FB.logout(function(response) {
        statusChangeCallback(response);
        document.getElementById('logout').style.display = "none";
        location.reload();
      });
    }

  </script>
  <style>
    .data{
      display: none;
    }
    #logout{
      display: none;
    }
  </style>
</head>
<body>


<!--  The JS SDK Login Button -->
  <div class="g-signin2" data-onsuccess="onSignIn"></div>
  <div class="data">
      <p>Profile Details</p>
      <img id="pic" class="img-circle" width="100" height="100"/>
      <p>Email Address</p>
      <p id="email" class="alert alert-danger"></p>
      <button onclick="signOut()" class="bth btn-danger">Sign Out</button>
  </div>
  
  
  <div class="facebook">
    <fb:login-button scope="public_profile,email" onlogin="checkLoginState();">
    </fb:login-button>

    <div id="status">
    </div>

    <div id="logout">
      <button onclick="logOut()">Logout</button> 
    </div>
  </div>


</body>
</html>