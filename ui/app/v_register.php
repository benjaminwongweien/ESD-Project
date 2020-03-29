<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Vendor Registration</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta name="author" content="colorlib.com">

		<!-- MATERIAL DESIGN ICONIC FONT -->
		<link rel="stylesheet" href="v_register_util/fonts/material-design-iconic-font/css/material-design-iconic-font.css">

		<!-- DATE-PICKER -->
		<link rel="stylesheet" href="v_register_util/vendor/date-picker/css/datepicker.min.css">

		<!-- STYLE CSS -->
		<link rel="stylesheet" href="v_register_util/css/style.css">
	</head>
	<body>
		<div class="wrapper">
            <form action="" id="wizard" action="" method="post" enctype="multipart/form-data">
        		<!-- SECTION 1 -->
                <h4></h4>
                <section>
                    <h3>Your details</h3>
                	<div class="form-row">
                        <div class="form-holder">
                            <i class="zmdi zmdi-account"></i>
                            <input type="text" class="form-control" name="vendor_name" id="vendor_name" placeholder="Name of Shop">
                        </div>
                	</div>
                    <div class="form-row">
                        <div class="form-holder">
                            <i class="zmdi zmdi-account-box-o"></i>
                            <input type="text" class="form-control" name="vendor_description" id="vendor_description" placeholder="Store description (What do you cook?)">
                        </div>
                    </div>
                    <div class="form-row">
                            <div class="form-holder">
                                <i class="zmdi zmdi-pin"></i>
                                <input type="text" class="form-control" name="vendor_location" id="vendor_location" placeholder="Address">
                        </div>
                    </div>
                </section>
            <!-- </form>
            <form action="" id="wizard" action="" method="post" enctype="multipart/form-data"> -->
				<!-- SECTION 2 -->
                <h4></h4>
                <section>
                	<h3>Upload Your Store Image</h3>
                    <div class="form-row">
                        <div class="form-holder w-100">
                            <input type="file" name="fileToUpload" id="fileToUpload">
                            <input type="submit" value="Upload Image" name="submit">
                        </div>
                    </div>
                </section>

                <!-- SECTION 3 -->
                <h4></h4>
                <section>
                    <h3 style="margin-bottom: 16px;">Add a food</h3>
                    <div class="form-row">
                        <div class="form-holder">
                            <i class="zmdi zmdi-account"></i>
                            <input type="text" class="form-control" name="food_name" id="vendor_name" placeholder="Name of Food">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-holder">
                            <i class="zmdi zmdi-account"></i>
                            <input type="text" class="form-control" name="food_description" id="food_description" placeholder="Description">
                        </div>
                	</div>
                    <div class="form-row">
                        <div class="form-holder">
                            <i class="zmdi zmdi-shopping-cart"></i>
                            <input type="text" class="form-control" name="food_price" id="food_price" placeholder="Price">
                        </div>
                    </div>


                    <!-- <table cellspacing="0" class="table-cart shop_table shop_table_responsive cart woocommerce-cart-form__contents table" id="shop_table">
                        <thead>
                            <th >&nbsp;</th>
                            <th style="text-align: left;">Product Detail</th>
                            <th >Quantity</th>
                            <th >Total Price</th>
                            <th >&nbsp;</th>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="product-thumb">
                                    <a href="#" class="item-thumb">
                                        <img src="images/item-1.jpg" alt="">
                                    </a>
                                </td>
                                <td class="product-detail" data-title="Product Detail">
                                    <div>
                                        <a href="#">Cherry</a>
                                        <span>$</span>
                                        <span>35</span>
                                    </div>
                                </td>
                                <td class="product-quantity" data-title="Quantity">
                                    <div class="quantity">
                                        <span class="plus">+</span>
                                        <input type="number" id="quantity_5b4f198d958e1" class="input-text qty text" step="1" min="0" max="" name="cart[5934c1ec0cd31e12bd9084d106bc2e32][qty]" value="1" title="Qty" size="4" pattern="[0-9]*" inputmode="numeric" />
                                        <span class="minus">-</span>
                                    </div>
                                </td>
                                <td class="total-price" data-title="Total Price">
                                    <span class="woocommerce-Price-amount amount">
                                        <span class="woocommerce-Price-currencySymbol">$</span>
                                        70
                                    </span>
                                </td>
                                <td class="product-remove">
                                    <a href="#">
                                        <i class="zmdi zmdi-close-circle-o"></i>
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td class="product-thumb">
                                    <a href="#" class="item-thumb">
                                        <img src="images/item-2.jpg" alt="">
                                    </a>
                                </td>
                                <td class="product-detail" data-title="Product Detail">
                                    <div>
                                         <a href="#">Mango</a>
                                        <span>$</span>
                                        <span>2035</span>
                                    </div>
                                </td>
                                <td class="product-quantity" data-title="Quantity">
                                    <div class="quantity">
                                        <span class="plus">+</span>
                                        <input type="number" id="quantity_5b4f198d958e1" class="input-text qty text" step="1" min="0" max="" name="cart[5934c1ec0cd31e12bd9084d106bc2e32][qty]" value="1" title="Qty" size="4" pattern="[0-9]*" inputmode="numeric" />
                                        <span class="minus">-</span>
                                    </div>
                                </td>
                                <td class="total-price" data-title="Total Price">
                                    <span class="woocommerce-Price-amount amount">
                                        <span class="woocommerce-Price-currencySymbol">$</span>
                                        20
                                    </span>
                                </td>
                                <td class="product-remove">
                                    <a href="#">
                                        <i class="zmdi zmdi-close-circle-o"></i>
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table> -->
                </section>

                <!-- SECTION 4 -->
                <h4></h4>
                <section>
                    <h3>Add Your Food Image</h3>
                    <div class="form-row">
                        <div class="form-holder w-100">
                            <input type="file" name="fileToUpload" id="fileToUpload">
                            <input type="submit" value="Upload Image" name="submit">
                        </div>
                    </div>
                    
                </section>
            </form>
		</div>

		<script src="v_register_util/js/jquery-3.3.1.min.js"></script>
		
		<!-- JQUERY STEP -->
		<script src="v_register_util/js/jquery.steps.js"></script>

		<script src="v_register_util/js/main.js"></script>

<!-- Template created and distributed by Colorlib -->
</body>
</html>