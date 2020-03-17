<!DOCTYPE html>
<html lang="en">
<head>
	<title>Login to EaSy Delivery</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
	<!--Login API  -->
	<meta name="google-signin-client_id" content="520394046268-u3jk5i6a7bt3ghkdmgu8g6hc3oanhh31.apps.googleusercontent.com">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="login_util/images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="login_util/vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/vendor/select2/select2.min.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="login_util/vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="login_util/css/util.css">
	<link rel="stylesheet" type="text/css" href="login_util/css/main.css">
<!--===============================================================================================-->

</head>
<body>
	
	<div class="limiter">
		<div class="container-login100" style="background-image: url('login_util/images/bg-01.jpg');">
			<div class="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">
				<form class="login100-form validate-form flex-sb flex-w">
					<span class="login100-form-title p-b-53">
						Sign In With
					</span>
						
						<!-- default FB button -->
						<a href="c_homepage.php" class="btn-face m-b-20" id="facebook_button">
							<div>
								<i class="fa fa-facebook-official" style="position:relative;"></i>
							</div>	
							Facebook
							<div style="opacity:0;position:absolute;">
								<fb:login-button size='large' scope="public_profile,email" onlogin="checkLoginState();">Login with Facebook Today</fb:login-button>
								<fb:login-button size='large' scope="public_profile,email" onlogin="checkLoginState();">Login with Facebook Today</fb:login-button>
								<fb:login-button size='large' scope="public_profile,email" onlogin="checkLoginState();">Login with Facebook Today</fb:login-button>
							</div>
						</a>
						
						<!-- working FB button -->
						<!-- <div style="opacity:0.5">
							<div class="facebook">
								<fb:login-button scope="public_profile,email" onlogin="checkLoginState();">
								</fb:login-button>

								<div id="status">
								</div>

								<div id="logout">
								<button onclick="facebook_logOut()">Logout</button> 
								</div>
							</div>
						</div> -->
					
					<!-- default google button -->
					<a href="c_homepage.php" class="btn-google m-b-20" id="google_button">
						<div>
							<img src="login_util/images/icons/icon-google.png" alt="GOOGLE" style="position:relative;">
						</div>	
							Google
						<div style="opacity:0;position:absolute;">
							<div href="#" class="g-signin2" data-onsuccess="onSignIn" data-width="205" data-height="75"></div>  
						</div>
					</a>
					
					<!-- working google button -->
					<!-- <div style="opacity:0.5">
						<div href="#" class="g-signin2" data-onsuccess="onSignIn"></div>  
					</div> -->
				
				</form>
			</div>
		</div>
	</div>

	<!-- <div class="data">
        <p>Profile Details</p>
        <img id="pic" class="img-circle" width="100" height="100"/>
        <p>Email Address</p>
        <p id="email" class="alert alert-danger"></p>
        <p>Name</p>
        <p id="name" class="alert alert-danger"></p>
        <button onclick="signOut()" class="btn btn-danger">Sign Out</button>
    </div> -->
	
	
<!--===============================================================================================-->
	<script src="login_util/vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="login_util/vendor/animsition/js/animsition.min.js"></script>
<!--===============================================================================================-->
	<script src="login_util/vendor/bootstrap/js/popper.js"></script>
	<script src="login_util/vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="login_util/vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="login_util/vendor/daterangepicker/moment.min.js"></script>
	<script src="login_util/vendor/daterangepicker/daterangepicker.js"></script>
<!--===============================================================================================-->
	<script src="login_util/vendor/countdowntime/countdowntime.js"></script>
<!--===============================================================================================-->
	<script src="login_util/js/main.js"></script>
	<script src="login_util/js/google_script.js"></script>
<!--===============================================================================================-->
<!-- Login API -->
	<script src="https://apis.google.com/js/platform.js" async defer></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	
<!-- Facebook JS -->
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
		sessionStorage.setItem("name", response.name);
		window.location.replace("./c_homepage.php");
		}

// /// ///  Google JS /// /// //
		function onSignIn(googleUser) {
			var profile = googleUser.getBasicProfile();
			$(".g-signin2").css("display", "none");
			$(".data").css("display", "block");
			var pic = $("#pic").attr('src',  profile.getImageUrl());
			var email = $("#email").text(profile.getEmail());
			var name = $("#name").text(profile.getName());
			
			sessionStorage.setItem("name", profile.getName());
			window.location.replace("./c_homepage.php");
		}
		

	</script>

</body>
</html>