<?php 
	// var_dump($_POST);
	// var_dump($_POST['username']);
	// $username = $_COOKIE['email'];

	// var_dump($username);
	?>

<!DOCTYPE html>
<html lang="en">
<head>
	<title>Vendor Registration</title>
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
						Your Details
					</span>

					<div class="p-t-31 p-b-9">
						<span class="txt1">
							Name of Shop
						</span>
					</div>
					<div class="wrap-input100 validate-input">
						<input class="input100" type="text" name="vendor_name" id="vendor_name" placeholder="Name of Shop">
						<span class="focus-input100"></span>
                    </div>
                    
                    <div class="p-t-31 p-b-9">
						<span class="txt1">
							Shop Description
						</span>
					</div>
					<div class="wrap-input100 validate-input">
						<textarea rows="10" class="input100" name="vendor_description" id="vendor_description" placeholder="Store description (What do you cook?)"></textarea>
                        <span class="focus-input100"></span>
                    </div>
                    
                    <div class="p-t-31 p-b-9">
						<span class="txt1">
							Address
						</span>
					</div>
					<div class="wrap-input100 validate-input">
						<input rows="10" class="input100" name="vendor_location" id="vendor_location" placeholder="Where is your shop?">
						<span class="focus-input100"></span>
					</div>
                    
                    <div class="container-login100-form-btn m-t-17" >
						<button class="login100-form-btn" id="next">
							Next
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
        function accessCookie(cookieName, finder){
          var name = cookieName + "=";
		  var allCookieArray = document.cookie.split(';');
		//   console.log(allCookieArray);
          for(var i=0; i<allCookieArray.length; i++)
          {
			var temp = allCookieArray[i].trim();
            if (temp.includes(finder))
            	return temp;
       	  }
        	return "";
        }
        
		async function postData(serviceURL, requestBody) {   
			const response =
                 await fetch(
                   serviceURL, {   
                       method: 'POST', // or 'PUT'
                       headers: {
                           'Content-Type': 'application/json',
                       },
                       body: JSON.stringify(requestBody),
                    });
            data = await response.json();
            if (response.ok){
                document.cookie = "vendor_id = " + data['data']['vendor_id'];
                window.location.replace("./v_register2.php");
            }
            else {
                console.log("die");
            }
        }

		$("#next").click(async() => {
            let isNext = confirm("You cannot return to the previous pages after submitting. Are you sure your details are correct?"); //true if OK is pressed
            event.preventDefault()

            var vendor_name = document.getElementById("vendor_name").value;  
            var vendor_description = document.getElementById("vendor_description").value;
            var vendor_location = document.getElementById("vendor_location").value;

		    var email_cookie = accessCookie(document.cookie, "email");
            var email = email_cookie.slice(6);
            
            if (isNext == true) {
                var serviceURL = "http://localhost:85/register_info";
                var requestBody = {
                    vendor_name : vendor_name, 
                    vendor_email: email, 
                    vendor_description:vendor_description, 
                    vendor_location: vendor_location
                };
            }
            
        	postData(serviceURL, requestBody);
        });
	</script>

</body>
</html>