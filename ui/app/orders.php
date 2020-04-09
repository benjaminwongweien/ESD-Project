<!DOCTYPE html>
	<html lang="en">
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
			<?php

				// Using Post, get vendor information from order_processing
				// Pass in: customerID
				// Return: username, user_type, chat_id
				$postdata = json_encode(array(
						'customerID' => $_COOKIE["email"]
					)
				);

				$opts = array('http' =>
					array(
						'method'  => 'POST',
						'header'  => 'Content-Type: application/json',
						'content' => $postdata
					)
				);
				
				$context  = stream_context_create($opts);
				$customer_list= json_decode(file_get_contents("http://host.docker.internal:8080/order/history/customer", false, $context), TRUE);
			?>
		</head>
		<body>
		  <header id="header" id="home">
		    <div class="container">
		    	<div class="row align-items-center justify-content-between d-flex">
			      <div id="logo">
			        <a href="c_homepage.php"><img src="homepage_util/img/logo.png" alt="" title="" /></a>
			      </div>
			      <nav id="nav-menu-container">
				        <ul class="nav-menu">
				          <li><a href="vendors.php">View All Vendors</a></li>
						  <li class="menu-has-children"><a href=""> <?php echo $_COOKIE['name'] ?></a>
				            <ul id="logout">
							  <li><a href="https://localhost/orders.php">Order History</a></li>
							  <?php echo $_COOKIE['logout_button'] ?>
				            </ul>
				          </li>
				        </ul>
				      </nav><!-- #nav-menu-container -->		    		
		    	</div>
		    </div>
		  </header><!-- #header -->			
			<section class="banner-area relative relative">	
				<div class="container">
				<div class="row fullscreen d-flex align-items-center justify-content-start">
						<div class="banner-content col-lg-8 col-md-12">
							<h4 class="text-white text-uppercase">View History</h4>
							<h1>
								Orders
							</h1>
							<p class="text-white">
								View your orders that you bought with us.
							</p>
						</div>
					</div>
				</div>
			</section>		
			<!-- End banner Area -->
		
			<!-- About Generic Start -->
			<div class="main-wrapper">
				<!-- Start team Area -->
				<section class="team-area pt-100">
					<div class="container">					
						<div class="row justify-content-left d-flex align-items-left">
							<h4 class="text-white text-uppercase">Your orders</h4>
							<?php
							foreach($customer_list as $customer){
								$vendorID = $customer['vendorID'];
								$delivererID = $customer['delivererID'];
								$vendorID = $customer['vendorID'];
								$foodID = $customer['foodID'];
								$status = $customer['order_status'];
								$quantity = $customer['quantity'];
								$price = $customer['price'];
								$deliveryAddress = $customer['delivery_address'];

								
								// Using Post, get vendor and food information from menu
								// Pass in: vendor_email , food_id
								// Return: food_description, food_id, food_image, food_label, food_name, food_price
								$postdata = json_encode(array(
									'vendor_email' => $vendorID,
									'food_id' => $foodID
									)
								);
				
								$opts = array('http' =>
									array(
										'method'  => 'POST',
										'header'  => 'Content-Type: application/json',
										'content' => $postdata
									)
								);
								
								$context  = stream_context_create($opts);
								$food_info = json_decode(file_get_contents("http://host.docker.internal:85/search/food/email", false, $context), TRUE);
								
								if ($customer['customerID'] == $_COOKIE['email']){
									?>
									<table border="1">
										<tr>
											<td colspan="2"><h4 class='meta-text mt-30 text-center'>Status of Delivery: <?=$status?></h4></td>
										</tr>
										<tr>
											<td colspan="2"><h4 class='meta-text mt-30 text-center'>Food Name: <?=$food_info['food']['food_name']?></h4></td>
										</tr>
										<tr>
											<td><h4 class='meta-text mt-30 text-center'>Quantity: <?=$quantity?></h4></td>
											<td><h4 class='meta-text mt-30 text-center'>Price: <?=$price?></h4></td>
										</tr>
										<tr>
											<td colspan="2"><h4 class='meta-text mt-30 text-center'>Total: <?=number_format(($price * $quantity), 2)?></h4></td>
										</tr>
										<tr>
											<td colspan="2"><h4 class='meta-text mt-30 text-center'>Deliverer: <?=($delivererID == "0")?"None":$delivererID?></h4></td>
										</tr>
										<tr>
											<td colspan="2"><h4 class='meta-text mt-30 text-center'>Delivery Address: <?=$deliveryAddress?></h4></td>
										</tr>
										
									</table>

									<?php
									}								
							}
							?>
							
						</div>
					</div>	
				</section>
			</div>
				<!-- End team Area -->	

			<div class="main-wrapper">
			<!-- Start team Area -->
			<section class="team-area pt-100">
				<div class="container">	
				</div>
			</section>
			</div>

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
			<script src="homepage_util/js/mail-script.js"></script>				
			<script src="homepage_util/js/main.js"></script>	
		</body>
	</html>
