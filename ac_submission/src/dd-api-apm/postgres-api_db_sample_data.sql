-- create api database
--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Debian 12.2-2.pgdg100+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)

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
-- Name: users; Type: TABLE; Schema: public; Owner: datadog
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(30),
    email character varying(30)
);


ALTER TABLE public.users OWNER TO datadog;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: datadog
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO datadog;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: datadog
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: datadog
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: datadog
--

COPY public.users (id, name, email) FROM stdin;
1	Jerry	jerry@example.com
2	George	george@example.com
3	Tom	tom@example.com
4	Mary	mary@example.com
5	Sue	sue@example.com
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: datadog
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: datadog
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

