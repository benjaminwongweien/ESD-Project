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
		<div class="container-login100" style="background-image: url('login_util/images/bg-04.jpg');">
			<div class="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">
				<form class="login100-form validate-form flex-sb flex-w">
					<span class="login100-form-title p-b-53">
						Register
					</span>

					<div class="p-t-31 p-b-9">
						<span class="txt1">
							Email
						</span>
					</div>
					<div class="wrap-input100 validate-input">
						<input class="input100" type="text" name="username" id="username" value= <?php echo $_COOKIE['email'] ?> readonly>
						<span class="focus-input100"></span>
					</div>
					
					<div class="p-t-13 p-b-9">
						<span class="txt1">
							User type
						</span>
					</div>
					<div class="wrap-inputRadio validate-input" id="user_type">
						<input class="inputRadio" type="radio" id="user" name="user_type" value="user" ><label for="user">User</label> <br>
						<input class="inputRadio" type="radio" id="vendor" name="user_type" value="vendor"><label for="vendor">Vendor</label> <br>
						<input class="inputRadio" type="radio" id="driver" name="user_type" value="driver"><label for="driver">Driver</label> <br>
					</div>


					<div class="container-login100-form-btn m-t-17" >
						<button class="login100-form-btn" id="addUser">
							Sign Up
						</button>
					</div>

					<br>
					<!-- <div>
							All rights reserved | Image taken from : https://qz.com/1038229/to-lose-weight-you-need-to-understand-the-psychology-of-why-you-crave-the-wrong-things/
					</div> -->
				</form>	
			</div>	
		</div>
	</div>
	
	
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
	
<!--  -->
	<script>
		// console.log(document.cookie);
		function accessCookie(cookieName){
          var name = cookieName + "=";
		  var allCookieArray = document.cookie.split(';');
		//   console.log(allCookieArray);
          for(var i=0; i<allCookieArray.length; i++)
          {
			var temp = allCookieArray[i].trim();
            if (temp.includes("email"))
            	return temp;
       	  }
        	return "";
		}

		// Post user data to the database
		async function postData(serviceURL, requestBody, user_type) {   
			const response =
                 await fetch(
                   serviceURL, {   
                       method: 'POST', // or 'PUT'
                       headers: {
                           'Content-Type': 'application/json',
                       },
                       body: JSON.stringify(requestBody),
					});
			// after adding, redirect user to the various homepage according to their inputted user type
			if(user_type == "user"){
				window.location.replace("./c_homepage.php");
			}
			else if(user_type == "vendor"){
				window.location.replace("./v_homepage.php");
			}
			
			else if(user_type == "driver"){
				window.location.replace("./d_homepage.php");
			}
        }

		$("#addUser").click(async() => {
			event.preventDefault()
		    var email_cookie = accessCookie(document.cookie);
			var email = email_cookie.slice(6);
			var id = null;

            var user_type = $("input:radio[name=user_type]:checked").val();
			var serviceURL = "http://localhost:88/register";
            var requestBody = {
        		uid : email, 
                type: user_type, 
                tid: id
            };

        	postData(serviceURL, requestBody, user_type);
        });
	</script>

</body>
</html>