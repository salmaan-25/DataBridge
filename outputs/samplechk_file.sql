--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: file; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.file (
    name text,
    capital text,
    population text,
    area text,
    currency text,
    languages text,
    region text,
    subregion text,
    flag text
);


ALTER TABLE public.file OWNER TO postgres;

--
-- Data for Name: file; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.file (name, capital, population, area, currency, languages, region, subregion, flag) FROM stdin;
France	Paris	67364357	551695	Euro	['French']	Europe	Western Europe	https://upload.wikimedia.org/wikipedia/commons/c/c3/Flag_of_France.svg
Germany	Berlin	83240525	357022	Euro	['German']	Europe	Western Europe	https://upload.wikimedia.org/wikipedia/commons/b/ba/Flag_of_Germany.svg
United States	Washington, D.C.	331893745	9833517	USD	['English']	Americas	Northern America	https://upload.wikimedia.org/wikipedia/commons/a/a4/Flag_of_the_United_States.svg
Belgium	Brussels	11589623	30528	Euro	['Flemish', 'French', 'German']	Europe	Western Europe	https://upload.wikimedia.org/wikipedia/commons/6/65/Flag_of_Belgium.svg
\.


--
-- PostgreSQL database dump complete
--

