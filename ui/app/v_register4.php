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
						Upload your food image
					</span>

					<div class="p-t-31 p-b-9">
						<span class="txt1">
							<input type="file" name="fileToUpload" id="fileToUpload">
							<br><img id="myImg" src="#" alt="your image" height=50% width=50%>
						</span>
					</div>
                    
                    
                    <div class="p-t-31 p-b-9">
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

		// Image upload function listens to any change to the upload button
		// If there is a change,
		// 		user has uploaded an image
		// 		grab that image using querySelector
		window.addEventListener('load', function() {
			document.querySelector('input[type="file"]').addEventListener('change', function() {
				if (this.files && this.files[0]) {
					var img = document.querySelector('img');  // $('img')[0]
					img.src = URL.createObjectURL(this.files[0]); // set src to blob url
				}
			});
		});

		// Function to extract cookie
		// Pass in: the whole cookie, the name of the cookie you want to find
		// Return: the whole cookie that you want to find
		// 		   e.g. "username=xxx@gmail.com"
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
		
		// Post Json data
		// Redirect user back to to part vendor homepage
		async function postData(serviceURL, file) { 
			
			// console.log(file);

			const response =
                 await fetch(
                   serviceURL, {   
					   method: 'POST', // or 'PUT'
					   headers: {},
                       body: file,
                    });
            data = await response.json();
			// console.log(data);
            if (response.ok){
                window.location.replace("https://localhost/v_homepage.php");
            }
            // else {
            //     console.log("die");
            // }
        }

		$("#next").click(async() => {
            let isNext = confirm("You cannot return to the previous pages after submitting. Are you sure your details are correct?"); //true if OK is pressed
            event.preventDefault()

			var fd = new FormData();

			myFile = document.getElementById("fileToUpload").files[0];
			fd.append('image', myFile);

			var vendor_id_cookie = accessCookie(document.cookie, "vendor_id");
			var vendor_id = vendor_id_cookie.slice(10);
			
			var food_id_cookie = accessCookie(document.cookie, "food_id");
			var food_id = food_id_cookie.slice(8);

			// post data to menu to store the food image
			var serviceURL = "http://localhost:85/upload/" + vendor_id +"/" + food_id;
			postData(serviceURL, fd);
        });
	</script>

</body>
</html>