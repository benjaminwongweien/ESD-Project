--
-- PostgreSQL Init Script - User Microservice
--

-- @author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman, Low Louis
-- @team   - G3T4

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
-- Name: user; Type: TABLE; Schema: public; Owner: userms
--

CREATE TABLE public."user" (
    username character varying(80) NOT NULL,
    user_type character varying(80) NOT NULL,
    chat_id integer
);


ALTER TABLE public."user" OWNER TO userms;

--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: userms
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (username);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: userms
--

COPY public."user" (username, user_type, chat_id) FROM stdin;
0	driver	\N
user@user.com	user	\N
driver@driver.com	driver	\N
vendor@vendor.com	vendor	\N
faithkoh1997@gmail.com	user	\N
slypoon@gmail.com	vendor	\N
bentennisonrulez@gmail.com	driver	\N
\.


--
-- PostgreSQL database dump complete
--

