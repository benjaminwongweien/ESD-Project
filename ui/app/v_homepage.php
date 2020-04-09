<!DOCTYPE html>
	<html lang="zxx" class="no-js">
	<head>
		<!-- Mobile Specific Meta -->
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<!-- Favicon-->
		<link rel="shortcut icon" href="homepage_util/img/elements/fav.png">
		<!-- Author Meta -->
		<meta name="author" content="colorlib">
		<!-- Meta Description -->
		<meta name="description" content="">
		<!-- Meta Keyword -->
		<meta name="keywords" content="">
		<!-- meta character set -->
		<meta charset="UTF-8">
		<!-- Site Title -->
		<title>Restaurant</title>

		<link href="https://fonts.googleapis.com/css?family=Poppins:100,200,400,300,500,600,700" rel="stylesheet"> 
			<!--
			CSS
			============================================= -->
			<link rel="stylesheet" href="homepage_util/css/linearicons.css">
			<link rel="stylesheet" href="homepage_util/css/owl.carousel.css">
			<link rel="stylesheet" href="homepage_util/css/font-awesome.min.css">
			<link rel="stylesheet" href="homepage_util/css/nice-select.css">			
			<link rel="stylesheet" href="homepage_util/css/magnific-popup.css">
			<link rel="stylesheet" href="homepage_util/css/bootstrap.css">
			<link rel="stylesheet" href="homepage_util/css/main.css">

			<script>
				// console.log(document.cookie);

				// If user does not have cookie, it means they are not logged in
				// redirect them back to the logout page to clear cookies again, JUST IN CASE
				// then logout will bring them back to the index page
				if (document.cookie == "") {
					window.location.replace("./logout.php");
				}

			</script>
		
		</head>
		<body>
		  <header id="header" id="home">
		    <div class="container">
		    	<div class="row align-items-center justify-content-between d-flex">
			      <div id="logo">
			        <a href="v_homepage.php"><img src="homepage_util/img/logo.png" alt="" title="" /></a>
			      </div>
			      <nav id="nav-menu-container">
			        <ul class="nav-menu">
						<li class="menu-has-children"><a href="">Welcome, <?= $_COOKIE['name'] ?> !</a></li>
						<li><?= $_COOKIE['logout_button'] ?></li>
			        </ul>
			      </nav><!-- #nav-menu-container -->		    		
		    	</div>
		    </div>
		  </header><!-- #header -->			
			<section class="banner-area relative relative">	
				<div class="container">
					<div class="row fullscreen d-flex align-items-center justify-content-start">
						<div class="banner-content col-lg-8 col-md-12">
							
							<h4 class="text-white text-uppercase">An Exciting Journey Awaits You</h4>
							<h1>
								Welcome! <p>We can't wait to try your food!				
							</h1>
							<p class="text-white">
								We bring you closer to your customers
							</p>
							<a href="v_register.php" class="primary-btn header-btn text-uppercase">Let's get started</a>
						</div>			
						
						<?php
							// get list of food from menu
							// return: [food_description, food_id, food_image, food_label, food_name, food_price]
							// 		   status, vendor_description, vendor_email, vendor_id, vendor_image, vendor_location, vendor_name
							$vendors= json_decode(file_get_contents("http://host.docker.internal:85/all_vendor"), TRUE);
							
							// get all food from menu
							// return: [food_description, food_id, food_image, food_label, food_name, food_price]
							$all_food = json_decode(file_get_contents("http://host.docker.internal:85/all_food"), TRUE);

							
							$exist = 0;
							foreach ($vendors['vendors'] as $vendor) {
								if( $_GET["vendor_id"] == $vendor['vendor_id']) {
									$exist = 1; ?>
									<h4 class='text-white text-uppercase'>Wide Network of Choice</h4>
									<h1><?=$vendor['vendor_name']?></h1>
									<p class='text-white'>Food delivery near you from a curated choice of local restaurants across Singapore.</p>
						
						?>
						</div>
					</div>
				</div>
			</section>		
			<!-- End banner Area -->
		
			<!-- About Generic Start -->
			<div class="main-wrapper">

				<!-- Start team Area -->
				<section class="team-area pt-100" id="main">
					<div class="container">					
						<div class="row justify-content-center d-flex align-items-left">

						<?php
							// get list of food from menu
							// return: food_description, food_id, food_image, food_label, food_name, food_price
							$food_list = json_decode(file_get_contents("http://host.docker.internal:85/all_food"), TRUE);
							
							foreach ($food_list['food'] as $food) {?>
								<div class='col single-team'>
									<div class='thumb'>
										<a href='food.php?vendor_id=<?=$food['vendor_id']?>'><img class='img-fluid' src='http://host.docker.internal:85/static/{$vendor['vendor_image']}'></a>
									</div>
									<div class='meta-text mt-30 text-justify'>
										<h4><?=$food['food_id']?></h4>
										<p><?=$food['food_name']?></p>
										<p><?=$food['food_description']?></p>
										<p><?=$vendor['food_price']?></p>
									</div>
								</div>
								<?php
								}
							}?>
							<br/><br/><br/><br/><br/>
						<?php
						}?>
					
						</div>
					</div>	
				</section>
			</div>
				<!-- End team Area -->

			<!-- start footer Area -->		
			<footer class="footer-area section-gap">
				<div class="container">
					<div class="row">
						<div class="col-lg-3  col-md-6 col-sm-6">
							<div class="single-footer-widget">
								<h4 class="text-white">About Us</h4>
								<p>
									For us, it's not just about bringing you good food from your favourite restaurants. It's about making a connection, which is why we sit down with the vendors, ensuring that you get the best delivered to your doorstep.
								</p>
							</div>
						</div>
						<div class="col-lg-4  col-md-6 col-sm-6">
							<div class="single-footer-widget">
								<h4 class="text-white">Contact Us</h4>
								<p class="number">
									63-74-350
								</p>
							</div>
						</div>	
										
					</div>
					<div class="footer-bottom d-flex justify-content-between align-items-center flex-wrap">
					<!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
            <p class="footer-text m-0">EaSy Delivery &copy; <script>document.write(new Date().getFullYear());</script>. All rights reserved | Powered by <a href="https://colorlib.com" target="_blank">Colorlib</a> <i class="fa fa-heart-o" aria-hidden="true"></i></p>
            <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
					</div>
				</div>
			</footer>	
			<!-- End footer Area -->
			<script src="homepage_util/js/vendor/jquery-2.2.4.min.js"></script>
			<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
			<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBhOdIF3Y9382fqJYt5I_sswSrEw5eihAA"></script>
			<script src="homepage_util/js/vendor/bootstrap.min.js"></script>			
			<script src="homepage_util/js/hoverIntent.js"></script>
			<script src="homepage_util/js/easing.min.js"></script>			
			<script src="homepage_util/js/superfish.min.js"></script>	
			<script src="homepage_util/js/jquery.ajaxchimp.min.js"></script>
			<script src="homepage_util/js/jquery.magnific-popup.min.js"></script>	
			<script src="homepage_util/js/owl.carousel.min.js"></script>			
			<script src="homepage_util/js/jquery.sticky.js"></script>
			<script src="homepage_util/js/jquery.nice-select.min.js"></script>			
			<script src="homepage_util/js/parallax.min.js"></script>	
			<script src="homepage_util/js/waypoints.min.js"></script>
			<script src="homepage_util/js/jquery.counterup.min.js"></script>
			<script src="homepage_util/js/mail-script.js"></script>				
			<script src="homepage_util/js/main.js"></script>	
										

			<!-- FACEBOOK -->
			<script>
				function statusChangeCallback(response) {  // Called with the results from FB.getLoginStatus().
				// console.log('statusChangeCallback');
				// console.log(response);                   // The current login status of the person.	
				
				// if (response.status === 'connected') {   // Logged into the webpage using Facebook.
				// 		console.log("Logged in as facebook");
				// 		console.log(document.cookie);
				// 	} else {                                 // Logged in using Google
				// 		console.log("Not logged in as facebook")
				// 	}
				}

				function checkLoginState() {               // Called when a person is finished with the Login Button.
					FB.getLoginStatus(function(response) {   // See the onlogin handler
						statusChangeCallback(response);
					});
				}
				window.fbAsyncInit = function() {
				FB.init({
					appId      : '201004657801578',
					cookie     : true,
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

				
				function logOut(){		// Facebook logout works differently, as such, you need to use the function
					FB.logout(function(response) {
						statusChangeCallback(response);
						document.getElementById('logout').style.display = "none";
						// redirect users to logout to remove the cookies stored in the console
						window.location.replace("./logout.php");
					});s
				}
			</script>
		
		</body>
	</html>
