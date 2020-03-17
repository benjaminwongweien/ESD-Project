<? session_start(); ?>
	
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
				var username = sessionStorage.getItem("name");
				console.log(username);
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
						  <li class="menu-has-children"><a href=""><p id="user"></p></a>
				            <ul>
				              <li id="logout"><a href="./orders.php">Orders</a></li>
				              <li><a href="./logout.php">Logout</a></li>
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
			
			<!-- Start video Area -->
			<!-- <section class="video-area">
				<div class="container">
					<div class="row justify-content-center align-items-center flex-column">
						<a class="play-btn" href="http://www.youtube.com/watch?v=0O2aH4XLbto">
							<img src="img/play-btn.png" alt="">
						</a>
						<h3 class="pt-20 pb-20 text-white">We Always serve the vaping hot and delicious foods</h3>
						<p class="text-white">Youtube video will appear in popover</p>
					</div>
				</div>	
			</section> -->
			<!-- End video Area -->
			

			<!-- Start features Area -->
			<!-- <section class="features-area pt-100" id="feature">
				<div class="container">
					<div class="feature-section">
						<div class="row">
							<div class="single-feature col-lg-3 col-md-6">
								<img src="img/f1.png" alt="">
								<h4 class="pt-20 pb-20">Refreshing Breakfast</h4>
								<p>
									Lorem ipsum dolor sit ametcons ecteturadipis icing elit.
								</p>
							</div>
							<div class="single-feature col-lg-3 col-md-6">
								<img src="img/f2.png" alt="">
								<h4 class="pt-20 pb-20">Awesome Lunch</h4>
								<p>
									Lorem ipsum dolor sit ametcons ecteturadipis icing elit.
								</p>
							</div>
							<div class="single-feature col-lg-3 col-md-6">
								<img src="img/f3.png" alt="">
								<h4 class="pt-20 pb-20">Soothing Dinner</h4>
								<p>
									Lorem ipsum dolor sit ametcons ecteturadipis icing elit.
								</p>
							</div>
							<div class="single-feature col-lg-3 col-md-6">
								<img src="img/f4.png" alt="">
								<h4 class="pt-20 pb-20">Rich Quality Buffet</h4>
								<p>
									Lorem ipsum dolor sit ametcons ecteturadipis icing elit.
								</p>
							</div>														
						</div>											
					</div>
				</div>	
			</section> -->
			<!-- End features Area -->


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


			<!-- Start team Area -->
			<!-- <section class="team-area section-gap" id="chefs">
				<div class="container">
					<div class="row d-flex justify-content-center">
						<div class="menu-content pb-70 col-lg-8">
							<div class="title text-center">
								<h1 class="mb-10">Meet Our Qualified Chefs</h1>
								<p>Who are in extremely love with eco friendly system.</p>
							</div>
						</div>
					</div>						
					<div class="row justify-content-center d-flex align-items-center">
						<div class="col-md-3 single-team">
						    <div class="thumb">
						        <img class="img-fluid" src="img/t1.jpg" alt="">
						        <div class="align-items-center justify-content-center d-flex">
									<a href="#"><i class="fa fa-facebook"></i></a>
									<a href="#"><i class="fa fa-twitter"></i></a>
									<a href="#"><i class="fa fa-linkedin"></i></a>
						        </div>
						    </div>
						    <div class="meta-text mt-30 text-center">
							    <h4>Ethel Davis</h4>
							    <p>Managing Director (Sales)</p>									    	
						    </div>
						</div>
						<div class="col-md-3 single-team">
						    <div class="thumb">
						        <img class="img-fluid" src="img/t2.jpg" alt="">
						        <div class="align-items-center justify-content-center d-flex">
									<a href="#"><i class="fa fa-facebook"></i></a>
									<a href="#"><i class="fa fa-twitter"></i></a>
									<a href="#"><i class="fa fa-linkedin"></i></a>
						        </div>
						    </div>
						    <div class="meta-text mt-30 text-center">
							    <h4>Rodney Cooper</h4>
							    <p>Creative Art Director (Project)</p>			    	
						    </div>
						</div>	
						<div class="col-md-3 single-team">
						    <div class="thumb">
						        <img class="img-fluid" src="img/t3.jpg" alt="">
						        <div class="align-items-center justify-content-center d-flex">
									<a href="#"><i class="fa fa-facebook"></i></a>
									<a href="#"><i class="fa fa-twitter"></i></a>
									<a href="#"><i class="fa fa-linkedin"></i></a>
						        </div>
						    </div>
						    <div class="meta-text mt-30 text-center">
							    <h4>Dora Walker</h4>
							    <p>Senior Core Developer</p>			    	
						    </div>
						</div>	
						<div class="col-md-3 single-team">
						    <div class="thumb">
						        <img class="img-fluid" src="img/t4.jpg" alt="">
						        <div class="align-items-center justify-content-center d-flex">
									<a href="#"><i class="fa fa-facebook"></i></a>
									<a href="#"><i class="fa fa-twitter"></i></a>
									<a href="#"><i class="fa fa-linkedin"></i></a>
						        </div>
						    </div>
						    <div class="meta-text mt-30 text-center">
							    <h4>Lena Keller</h4>
							    <p>Creative Content Developer</p>			    	
						    </div>
						</div>																		
					</div>
				</div>	
			</section> -->
			<!-- End team Area -->			

			<!-- start blog Area -->		
			<!-- <section class="blog-area section-gap" id="blog">
				<div class="container">
					<div class="row d-flex justify-content-center">
						<div class="menu-content pb-70 col-lg-8">
							<div class="title text-center">
								<h1 class="mb-10">Latest From Our Blog</h1>
								<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore  et dolore magna aliqua.</p>
							</div>
						</div>
					</div>					
					<div class="row">
						<div class="col-lg-3 col-md-6 single-blog">
							<div class="thumb">
								<img class="img-fluid" src="img/b1.jpg" alt="">
							</div>
							<p class="date">10 Jan 2018</p>
							<a href="#"><h4>Cooking Perfect Fried Rice
							in minutes</h4></a>
							<p>
								inappropriate behavior ipsum dolor sit amet, consectetur.
							</p>
							<div class="meta-bottom d-flex justify-content-between">
								<p><span class="lnr lnr-heart"></span> 15 Likes</p>
								<p><span class="lnr lnr-bubble"></span> 02 Comments</p>
							</div>									
						</div>
						<div class="col-lg-3 col-md-6 single-blog">
							<div class="thumb">
								<img class="img-fluid" src="img/b2.jpg" alt="">
							</div>
							<p class="date">10 Jan 2018</p>
							<a href="#"><h4>Secret of making Heart 
							Shaped eggs</h4></a>
							<p>
								inappropriate behavior ipsum dolor sit amet, consectetur.
							</p>
							<div class="meta-bottom d-flex justify-content-between">
								<p><span class="lnr lnr-heart"></span> 15 Likes</p>
								<p><span class="lnr lnr-bubble"></span> 02 Comments</p>
							</div>									
						</div>
						<div class="col-lg-3 col-md-6 single-blog">
							<div class="thumb">
								<img class="img-fluid" src="img/b3.jpg" alt="">
							</div>
							<p class="date">10 Jan 2018</p>
							<a href="#"><h4>How to check steak if 
							it is tender or not</h4></a>
							<p>
								inappropriate behavior ipsum dolor sit amet, consectetur.
							</p>
							<div class="meta-bottom d-flex justify-content-between">
								<p><span class="lnr lnr-heart"></span> 15 Likes</p>
								<p><span class="lnr lnr-bubble"></span> 02 Comments</p>
							</div>									
						</div>
						<div class="col-lg-3 col-md-6 single-blog">
							<div class="thumb">
								<img class="img-fluid" src="img/b4.jpg" alt="">
							</div>
							<p class="date">10 Jan 2018</p>
							<a href="#"><h4>Addiction When Gambling
							Becomes A Problem</h4></a>
							<p>
								inappropriate behavior ipsum dolor sit amet, consectetur.
							</p>
							<div class="meta-bottom d-flex justify-content-between">
								<p><span class="lnr lnr-heart"></span> 15 Likes</p>
								<p><span class="lnr lnr-bubble"></span> 02 Comments</p>
							</div>									
						</div>						
					</div>
				</div>	
			</section> -->
			<!-- end blog Area -->	

			<!-- Start Contact Area -->
			<!--<section class="contact-area" id="contact">
				<div class="container-fluid">
					<div class="row align-items-center d-flex justify-content-center">
						<div class="mapouter"><div class="gmap_canvas"><iframe width="582" height="545" id="gmap_canvas" src="https://maps.google.com/maps?q=singapore%20management%20university&t=&z=13&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://www.embedgooglemap.net/blog/divi-discount-code-elegant-themes-coupon/"></a></div><style>.mapouter{position:relative;text-align:right;height:545px;width:582px;}.gmap_canvas {overflow:hidden;background:none!important;height:545px;width:582px;}</style></div>
						<div class="col-lg-4 col-md-12 pt-100 pb-100">
							<form class="form-area" id="myForm" action="mail.php" method="post" class="contact-form text-right">
								<input name="fname" placeholder="Enter your name" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Enter your name'" class="common-input mt-10" required="" type="text">
								<input name="email" placeholder="Enter email address" pattern="[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,63}$" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Enter email address'" class="common-input mt-10" required="" type="email">
								<textarea class="common-textarea mt-10" name="message" placeholder="Messege" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Messege'" required=""></textarea>
								<button class="primary-btn mt-20">Send Message<span class="lnr lnr-arrow-right"></span></button>
								<div class="mt-10 alert-msg">
								</div>
							</form>
						</div>
					</div>
				</div>
			</section> -->
			<!-- End Contact Area -->				

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


			<!-- Display user name upon logging in -->
			<script>
				document.getElementById("user").innerHTML = username;
			</script>
		</body>
	</html>


