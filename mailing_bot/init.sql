--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2024-05-08 13:28:04

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
-- TOC entry 218 (class 1259 OID 87420)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id bigint NOT NULL,
    tg_id bigint
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 87419)
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO postgres;

--
-- TOC entry 4810 (class 0 OID 0)
-- Dependencies: 217
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- TOC entry 220 (class 1259 OID 87427)
-- Name: mailing_archive; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mailing_archive (
    id bigint NOT NULL,
    user_id bigint,
    mailing_text character varying(2048),
    mailing_photo character varying(2048),
    mailing_date date
);


ALTER TABLE public.mailing_archive OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 87426)
-- Name: mailing_archive_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mailing_archive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mailing_archive_id_seq OWNER TO postgres;

--
-- TOC entry 4811 (class 0 OID 0)
-- Dependencies: 219
-- Name: mailing_archive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mailing_archive_id_seq OWNED BY public.mailing_archive.id;


--
-- TOC entry 216 (class 1259 OID 87410)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    tg_id bigint,
    nickname character varying(255),
    date_joined date,
    confirmed boolean DEFAULT false NOT NULL,
    is_block boolean DEFAULT false NOT NULL,
    channel_date_joined date
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 87409)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4812 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4647 (class 2604 OID 87423)
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- TOC entry 4648 (class 2604 OID 87430)
-- Name: mailing_archive id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mailing_archive ALTER COLUMN id SET DEFAULT nextval('public.mailing_archive_id_seq'::regclass);


--
-- TOC entry 4644 (class 2604 OID 87413)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4802 (class 0 OID 87420)
-- Dependencies: 218
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, tg_id) FROM stdin;
\.


--
-- TOC entry 4804 (class 0 OID 87427)
-- Dependencies: 220
-- Data for Name: mailing_archive; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mailing_archive (id, user_id, mailing_text, mailing_photo, mailing_date) FROM stdin;
\.


--
-- TOC entry 4800 (class 0 OID 87410)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, tg_id, nickname, date_joined, confirmed, is_block, channel_date_joined) FROM stdin;
\.


--
-- TOC entry 4813 (class 0 OID 0)
-- Dependencies: 217
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_id_seq', 6, true);


--
-- TOC entry 4814 (class 0 OID 0)
-- Dependencies: 219
-- Name: mailing_archive_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mailing_archive_id_seq', 15, true);


--
-- TOC entry 4815 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- TOC entry 4652 (class 2606 OID 87425)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- TOC entry 4654 (class 2606 OID 87434)
-- Name: mailing_archive mailing_archive_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mailing_archive
    ADD CONSTRAINT mailing_archive_pkey PRIMARY KEY (id);


--
-- TOC entry 4650 (class 2606 OID 87417)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4655 (class 2606 OID 87435)
-- Name: mailing_archive user_id_pk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mailing_archive
    ADD CONSTRAINT user_id_pk FOREIGN KEY (user_id) REFERENCES public.users(id) NOT VALID;


-- Completed on 2024-05-08 13:28:04

--
-- PostgreSQL database dump complete
--

