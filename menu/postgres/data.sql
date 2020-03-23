--
-- PostgreSQL Init Script - Menu Microservice
--

-- @Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
-- @Team   - G3T4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: food; Type: TABLE; Schema: public; Owner: easydeliverymenudb
--

CREATE TABLE public.food (
    vendor_id integer NOT NULL,
    food_id integer NOT NULL,
    food_name character varying(80) NOT NULL,
    food_description text,
    food_image character varying(80),
    food_price real NOT NULL,
    food_label character varying(80),
    availability boolean NOT NULL,
    listed boolean NOT NULL
);


ALTER TABLE public.food OWNER TO easydeliverymenudb;

--
-- Name: food_food_id_seq; Type: SEQUENCE; Schema: public; Owner: easydeliverymenudb
--

CREATE SEQUENCE public.food_food_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.food_food_id_seq OWNER TO easydeliverymenudb;

--
-- Name: food_food_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: easydeliverymenudb
--

ALTER SEQUENCE public.food_food_id_seq OWNED BY public.food.food_id;


--
-- Name: vendor; Type: TABLE; Schema: public; Owner: easydeliverymenudb
--

CREATE TABLE public.vendor (
    vendor_id integer NOT NULL,
    vendor_name character varying(80) NOT NULL,
    vendor_description text,
    vendor_location character varying(80) NOT NULL,
    vendor_image character varying(80)
);


ALTER TABLE public.vendor OWNER TO easydeliverymenudb;

--
-- Name: vendor_vendor_id_seq; Type: SEQUENCE; Schema: public; Owner: easydeliverymenudb
--

CREATE SEQUENCE public.vendor_vendor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vendor_vendor_id_seq OWNER TO easydeliverymenudb;

--
-- Name: vendor_vendor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: easydeliverymenudb
--

ALTER SEQUENCE public.vendor_vendor_id_seq OWNED BY public.vendor.vendor_id;


--
-- Name: food food_id; Type: DEFAULT; Schema: public; Owner: easydeliverymenudb
--

ALTER TABLE ONLY public.food ALTER COLUMN food_id SET DEFAULT nextval('public.food_food_id_seq'::regclass);


--
-- Name: vendor vendor_id; Type: DEFAULT; Schema: public; Owner: easydeliverymenudb
--

ALTER TABLE ONLY public.vendor ALTER COLUMN vendor_id SET DEFAULT nextval('public.vendor_vendor_id_seq'::regclass);


--
-- Data for Name: food; Type: TABLE DATA; Schema: public; Owner: easydeliverymenudb
--

COPY public.food (vendor_id, food_id, food_name, food_description, food_image, food_price, food_label, availability, listed) FROM stdin;
1	1	Handmade Coleslaw	Fresh white cabbage, grated carrots, white onions,red peppers & mayo	food/1/1	2.95	western,side dish	t	t
1	2	Mixed lead slide salad	Mixed lead salad with a choice of dressing 	food/1/2	7.88	salad,side dish	t	t
1	3	Corn on the cob 	Fresh chargrilled corn on the cob 	food/1/3	3.99	side dish	t	t
1	4	Pit Wings	Our BBQ chicken wings, marinated for up to 48 hours & smothered in a choiece of hot sauce or pit saruce	food/1/4	10	BBQ	t	t
1	5	Banaoffee pie 	Vanillla cream, banana,biscuit, caramet sauce, topped with whipped cream 	food/1/5	4.8	side dish	t	t
2	6	Strawberry Cheesecake	Vanilla ice cream, strawberry coulis, biscuit	food/2/6	5.9	fruit,dessert	t	t
2	7	Bramley appl3 pie 	Vanilla ice cream, bramley apple compote, biscuit, topped with whipped cream 	food/2/7	5.2	fruit,dessert	t	t
2	8	Brownie & Waffle	Vanilla ice cream, chocolate sauce, brownie, waffle, toffee sauce, topped with whipped cream 	food/2/8	6.6	fruit,dessert	t	t
2	9	Children's ice cream	Vanilla ice cream with a choice of strawberry or chocolate sauce	food/2/9	4.5	fruit,dessert	t	t
2	10	Denver Chips 	Handmade chips topped with our "slow n low' 6 hour cooked marinated pulled pork, melted cheese & HBC BBQ pit sauce	food/2/10	4.95	handmade, chip	t	t
3	11	Hipster Chips	Handmade chips topped with jalapeno slaw, finished with Siriacha mayo & fresh spring onions 	food/3/11	3.95	chip, handmade	t	t
3	12	Classic beef 	Our original HBC burger relish, mayo, lettuce, tomato&red onion	food/3/12	6.65	meat, main dish	t	t
3	13	Cheese Classic 	Mature cheddar, our original HBC burger relish, mayo, lettuce, tomato& red onion	food/3/13	7.55	vege,main dish	t	t
3	14	Peaut butter & Bacon	Peanut butter, smoked bacon, chilli jam, lettuce, tomato & red onion	food/3/14	8.35	meat,main dish	t	t
3	15	Cheese & Bacon	Mature cheddar, smoked bacon,our msokey barbecue, relish,mayo, lettuce, tomato & red onion	food/3/15	8.85	meat,main dish	t	t
4	16	Mapo Tofu	Squishy, savoury soft goodness.	food/4/16	8.85	spicy, meat, main dish	t	t
4	17	Mixed Penang Curry	Stir fried with coconut milk, with curry paste and bring it to a boil. This is our amazing curry.	food/4/17	8.75	spicy, meat	t	t
4	18	Orange Chicken	A burst of fruity flavour infused the the most amazing chicken. Carefully handpicked by our finest chefs.	food/4/18	8.75	meat, main dish	t	t
4	19	Mixed Stir Fry Beef	Juicy and tender yet firm. Our olive wagyu beef is world class.	food/4/19	8.75	meat, main dish	t	t
4	20	Fried Pork Rice	Fried rice with the familiar flavour of Wok Hey. A flavour burt in your mouth on the first bite.	food/4/20	7.85	meat, vege	t	t
5	21	Blue Cheese & Bacon	HBC blue cheese mayo, smoked bacon, mayo, lettuce, tomato& red onion	food/5/21	8.85	meat, main dish	t	t
5	22	Avocado & Bacon 	Hand crushed avocado, smoked bacon, mayo, lettue, tomato & red onion 	food/5/22	8.75	vege, main dish,meat	t	t
5	23	Peppered Beef 	Onion rings, flat mushroom, caramelised red onion reslish, peppercom sauce, mayo, rocket. Tomato, & red onion 	food/5/23	8.85	meat, main dish, western	t	t
5	24	Macho Barbecue Beef, Cheese & Bacon	Two beef patties, mature cheddar, smoked bacon, our smoky barbecue relish, mayo, lettuce, tomato & RED IONIPN 	food/5/24	11.95	meat, main dish,vege	t	t
5	25	American BBQ Bacon Stuffed	Handmade patty stuffed with Swiss cheese, topped with somke bacon, HBC BBQ pit sauce, mayo, shredded iceberg lettuce & red onion	food/5/25	9.85	meat, main dish, BBQ,western	t	t
\.


--
-- Data for Name: vendor; Type: TABLE DATA; Schema: public; Owner: easydeliverymenudb
--

COPY public.vendor (vendor_id, vendor_name, vendor_description, vendor_location, vendor_image) FROM stdin;
1	HJFC	Finger Licking Good!	68 Orchard Rd, Plaza Singapura, #B1-21/22, Singapore 238839	vendor/1
2	Mom's Kitchen	Take a break from your busy business schedules or need a boost before heading back to your school works or simply just enjoying a leisurely family outing; do drop by here to enjoy a great bowl of your favourite dessert. In Mom's Kitchen, we remain committed to serve fresh and tasty desserts. And we stay open every day to serve to all our customers’ needs. So come visit us soon.	5 Cross St, Unit 01-30, Singapore 048418	vendor/2
3	Purple Sage	Purple Sage cooks a range of delicious dishes from fresh, local produce. Using a high level of technical skill, they are able to achieve fusion of flavours by taking a modern twist on traditional recipes. Their food contains only the finest, natural ingredients and contains less oil & less salt.	157 Pandan Loop, Singapore 128355	vendor/3
4	Broth Asia	Broth Asia soup makes you feel warm inside. Happy, safe, comforted, and at home. Each one is unique, an expression of the culture that inspired it and the home cooking that created it.	252 North Bridge Road, #B1-62 Rafffles City Shopping Centre, 179103, 179103	vendor/4
5	Fusion Spoon	Fusion Spoon is a unique casual dining place for families and friends Visitors can enjoy a wide selection of affordable food and beverages from various cuisine choices such as Western, Asian and Japanese. There is also a waffle and Korean bingsu ice kiosk at Fusion Spoon, for those looking for a little treat after a day out in the Gardens.	Singapore Botanic Gardens, Tanglin Gate, 1 Cluny Rd, #B1-00, 259569	vendor/5
\.


--
-- Name: food_food_id_seq; Type: SEQUENCE SET; Schema: public; Owner: easydeliverymenudb
--

SELECT pg_catalog.setval('public.food_food_id_seq', 25, true);


--
-- Name: vendor_vendor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: easydeliverymenudb
--

SELECT pg_catalog.setval('public.vendor_vendor_id_seq', 5, true);


--
-- Name: food food_pkey; Type: CONSTRAINT; Schema: public; Owner: easydeliverymenudb
--

ALTER TABLE ONLY public.food
    ADD CONSTRAINT food_pkey PRIMARY KEY (food_id, vendor_id);


--
-- Name: vendor vendor_pkey; Type: CONSTRAINT; Schema: public; Owner: easydeliverymenudb
--

ALTER TABLE ONLY public.vendor
    ADD CONSTRAINT vendor_pkey PRIMARY KEY (vendor_id);


--
-- Name: food food_vendor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: easydeliverymenudb
--

ALTER TABLE ONLY public.food
    ADD CONSTRAINT food_vendor_id_fkey FOREIGN KEY (vendor_id) REFERENCES public.vendor(vendor_id);


--
-- PostgreSQL database dump complete
--

