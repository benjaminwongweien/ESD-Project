<!DOCTYPE html>
	<html lang="zxx" class="no-js">
	<head>
		<!-- Mobile Specific Meta -->
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<!-- Favicon-->
		<link rel="shortcut icon" href="img/fav.png">
		<!-- Author Meta -->
		<meta name="author" content="codepixer">
		<!-- Meta Description -->
		<meta name="description" content="">
		<!-- Meta Keyword -->
		<meta name="keywords" content="">
		<!-- meta character set -->
		<meta charset="UTF-8">
		<!-- Site Title -->
		<title>EaSy Delivery</title>

		<link href="https://fonts.googleapis.com/css?family=Poppins:100,200,400,300,500,600,700" rel="stylesheet"> 
			<!--
			CSS
			============================================= -->
			<link rel="stylesheet" href="./homepage_util/css/linearicons.css">
			<link rel="stylesheet" href="./homepage_util/css/font-awesome.min.css">
			<link rel="stylesheet" href="./homepage_util/css/bootstrap.css">
			<link rel="stylesheet" href="./homepage_util/css/magnific-popup.css">
			<link rel="stylesheet" href="./homepage_util/css/nice-select.css">					
			<link rel="stylesheet" href="./homepage_util/css/animate.min.css">
			<link rel="stylesheet" href="./homepage_util/css/owl.carousel.css">
			<link rel="stylesheet" href="./homepage_util/css/main.css">

			<script>
				console.log(document.cookie);

				if (document.cookie == "") {
					// redirect users to login page
					window.location.replace("./logout.php");
				}
		
			</script>
		</head>
		<body>

			  <header id="header" id="home">
			    <div class="container">
			    	<div class="row align-items-center justify-content-between d-flex">
				      <div id="logo">
				        <a href="index.php"><img src="./homepage_util/img/logo.png" alt="" title="" /></a>
				      </div>
				      <nav id="nav-menu-container">
				        <ul class="nav-menu">
				          <li class="menu-active"><a href="#home">Home</a></li>
				          <li><a href="vendors.php">Vendors</a></li>
				          <!-- <li><a href="orders.php">Orders</a></li> -->
						  <li class="menu-has-children"><a href=""> <?php echo $_COOKIE['name'] ?></a>
				            <ul id="logout">
							  <li><a href="./orders.php">Orders</a></li>
							  <?php echo $_COOKIE['logout_button'] ?>
							  <!-- <li><a href="./logout.php">Logout</a></li> -->
							  <!-- <li><button onclick="logOut()">Logout</button></li> -->
				            </ul>
				          </li>
				        </ul>
				      </nav><!-- #nav-menu-container -->		    		
			    	</div>
			    </div>
			  </header><!-- #header -->

			<!-- start banner Area -->
			<section class="banner-area relative" id="home">
				<div class="container">
					<div class="row fullscreen d-flex align-items-center justify-content-start">
						<div class="banner-content col-lg-8 col-md-12">
						
							<h4 class="text-white text-uppercase">Wide Options of Choice</h4>
							<h1>
								Delicious Menu					
							</h1>
							<p class="text-white">
								Food delivery near you from a curated choice of local restaurants across Singapore.
							</p>
							<a href="vendors.php#main" class="primary-btn header-btn text-uppercase">Check Our Vendors</a>
						</div>												
					</div>
				</div>
			</section>
			<!-- End banner Area -->	

			<!-- Start top-dish Area -->
			<section class="top-dish-area section-gap" id="dish">
				<div class="container">
					<div class="row d-flex justify-content-center">
						<div class="menu-content pb-60 col-lg-8">
							<div class="title text-center">
								<h1 class="mb-10">Our Top Rated Vendor</h1>
								<p>Who are extremely loved by Singaporeans.</p>
							</div>
						</div>
					</div>						
					<div class="row">
						<div class="single-dish col-lg-4">
							<div class="thumb">
								<img class="img-fluid"  src="homepage_util/img/vendor-domino.png" alt="">
							</div>
							<h4 class="text-uppercase pt-20 pb-20">Domino's Pizza</h4>
							<p>
								Domino's Pizza Singapore is the best pizza company in Singapore with a relatively cheap price. Check out our latest pizza offers, promotions and special deals.
							</p>
						</div>
						<div class="single-dish col-lg-4">
							<div class="thumb">
								<img class="img-fluid"  src="homepage_util/img/vendor-purple.png" alt="">
							</div>
							<h4 class="text-uppercase pt-20 pb-20">Purple Sage</h4>
							<p>
								Purple Sage cooks a range of delicious dishes from fresh, local produce. Using a high level of technical skill, they are able to achieve fusion of flavours by taking a modern twist on traditional recipes. Their food contains only the finest, natural ingredients and contains less oil & less salt.
							</p>
						</div>
						<div class="single-dish col-lg-4">
							<div class="thumb">
								<img class="img-fluid"  src="homepage_util/img/vendor-broth.jpg" alt="">
							</div>
							<h4 class="text-uppercase pt-20 pb-20">Broth Asia</h4>
							<p>
								Broth Asia soup makes you feel warm inside. Happy, safe, comforted, and at home. Each one is unique, an expression of the culture that inspired it and the home cooking that created it.
							</p>
						</div>										
					</div>
				</div>	
			</section>
			<!-- End top-dish Area -->

			<!-- Start related Area -->
			<section class="related-area section-gap">
				<div class="container">
					<div class="row d-flex justify-content-center">
						<div class="menu-content pb-60 col-lg-8">
							<div class="title text-center">
								<h1 class="mb-10">Our Featured Food Menus</h1>
								<p>Who are in extremely love with eco friendly system.</p>
							</div>
						</div>
					</div>						
					<div class="row justify-content-center">
						<div class="active-realated-carusel">
							<?php
								$all_food = json_decode(file_get_contents("http://localhost:85/all_food"), TRUE);
								foreach ($all_food['food'] as $food) {
									if( $food['vendor_id'] == 1){
										echo "<form action='http://localhost:86/payment.php' method='POST'>";
										echo "<div class='row align-items-center'>";
											echo "<div class='col-lg-6 rel-left'>";
												echo "<h3>{$food['food_name']}</h3>";
												echo "<p class='pt-30 pb-30'>{$food['food_description']}</p>";
												echo "<p>Price: \$ {$food['food_price']}</p>";
												echo "<input value='1' min='1' style='width: 50px;' type='number' name='quantity'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
												echo "<input class='genric-btn info-border circle' type='submit' value='Buy Now'>";

												echo "<input type='hidden' value='{$food['vendor_id']}' name='customerid'>";
												echo "<input type='hidden' value='{$food['food_name']}' name='foodname'>";
												echo "<input type='hidden' value='{$food['food_description']}' name='food_description'>";
												echo "<input type='hidden' value='{$food['food_price']}' name='amount'>";
											echo "</div>";
											echo "<div class='thumb'>";
												echo "<img class='img-fluid' src='http://localhost:85/static/{$food['food_image']}' alt=''>";
											echo "</div>";
										echo "</div>";
										echo "</form>";
									}
								}
							?>					
												
						</div>
					</div>
				</div>	
			</section>
			<!-- End related Area -->				

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
								<!-- <p>
									Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore dolore magna aliqua.
								</p> -->
								<p class="number">
									012-6532-568-9746
								</p>
							</div>
						</div>	
						
						<div class="col-lg-5  col-md-6 col-sm-6">
							<div class="single-footer-widget">
								<h4 class="text-white">Newsletter</h4>
								<p>You can trust us. we only send  offers, not a single spam.</p>
								<div class="d-flex flex-row" id="mc_embed_signup">


									  <form class="navbar-form" novalidate="true" action="https://spondonit.us12.list-manage.com/subscribe/post?u=1462626880ade1ac87bd9c93a&amp;id=92a4423d01" method="get">
									    <div class="input-group add-on">
									      	<input class="form-control" name="EMAIL" placeholder="Email address" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Email address'" required="" type="email">
											<div style="position: absolute; left: -5000px;">
												<input name="b_36c4fd991d266f23781ded980_aefe40901a" tabindex="-1" value="" type="text">
											</div>
									      <!--- <div class="input-group-btn">
									        <button class="genric-btn"><span class="lnr lnr-arrow-right"></span></button>
									      </div> -->
									    </div>
									      <div class="info mt-20"></div>									    
									  </form>

								</div>
							</div>
						</div>				
					</div>
					<div class="footer-bottom d-flex justify-content-between align-items-center flex-wrap">
						<!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
            <p class="footer-text m-0">EaSy Delivery &copy; <script>document.write(new Date().getFullYear());</script>. All rights reserved | Powered by <a href="https://colorlib.com" target="_blank">Colorlib</a> <i class="fa fa-heart-o" aria-hidden="true"></i></p>
            <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
						<div class="footer-social d-flex align-items-center">
							<a href="#"><i class="fa fa-facebook"></i></a>
							<a href="#"><i class="fa fa-twitter"></i></a>
							<a href="#"><i class="fa fa-dribbble"></i></a>
							<a href="#"><i class="fa fa-behance"></i></a>
						</div>
					</div>
				</div>
			</footer>	
			<!-- End footer Area -->

			<script src="homepage_util/js/vendor/jquery-2.2.4.min.js"></script>
			<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
			<script src="homepage_util/js/vendor/bootstrap.min.js"></script>			
			<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBhOdIF3Y9382fqJYt5I_sswSrEw5eihAA"></script>
  			<script src="homepage_util/js/easing.min.js"></script>			
			<script src="homepage_util/js/hoverIntent.js"></script>
			<script src="homepage_util/js/superfish.min.js"></script>	
			<script src="homepage_util/js/jquery.ajaxchimp.min.js"></script>
			<script src="homepage_util/js/jquery.magnific-popup.min.js"></script>	
			<script src="homepage_util/js/owl.carousel.min.js"></script>			
			<script src="homepage_util/js/jquery.sticky.js"></script>
			<script src="homepage_util/js/jquery.nice-select.min.js"></script>			
			<script src="homepage_util/js/parallax.min.js"></script>	
			<script src="homepage_util/js/mail-script.js"></script>	
			<script src="homepage_util/js/main.js"></script>	
			<script src="homepage_util/js/logout_script.js"></script>	

			<!-- FACEBOOK -->
			<script>
				function statusChangeCallback(response) {  // Called with the results from FB.getLoginStatus().
				console.log('statusChangeCallback');
				console.log(response);                   // The current login status of the person.	
				
				if (response.status === 'connected') {   // Logged into your webpage and Facebook.
						console.log("Logged in as facebook");
						console.log(document.cookie);
					} else {                                 // Not logged into your webpage or we are unable to tell.
						console.log("Not logged in as facebook")
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

				
				function logOut(){
					FB.logout(function(response) {
						statusChangeCallback(response);
						document.getElementById('logout').style.display = "none";
						window.location.replace("./logout.php");
					});
				}
			</script>
		</body>
	</html>



