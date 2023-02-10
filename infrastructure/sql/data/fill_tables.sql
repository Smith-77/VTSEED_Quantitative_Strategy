--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

-- Started on 2023-02-08 22:31:14

--
-- TOC entry 209 (class 1259 OID 16421)
-- Name: test_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_data1 (
    date date NOT NULL,
    ticker character varying(10) NOT NULL,
    price real NOT NULL,
    market_cap real NOT NULL,
    fcf_ttm real,
    fcf_lq real,
    net_income_ttm real,
    net_income_lq real,
    operating_cash_flow_ttm real,
    total_assets real,
    beta_5y_mo_end real,
    roa_ttm real,
    net_income_ly real,
    total_assets_ly real,
    long_term_debt real,
    long_term_debt_ly real,
    current_ratio real,
    current_assets real,
    current_liabilities real,
    current_assets_ly real,
    current_liabilities_ly real,
    current_ratio_ly real,
    shares_outstanding real,
    shares_outstanding_ly real,
    gross_margin_percent_ttm real,
    gross_margin_percent_lq real,
    gross_margin_percent_ly real,
    asset_turnover_ratio real,
    asset_turnover_ratio_ly real,
    total_debt_to_total_equity_lq real,
    total_assets_lq real,
    total_revenue_lq real,
    roic_percent_ttm real,
    ebit_ttm real,
    ev real,
    p_to_b_daily real,
    p_to_e_daily real,
    ebita_ttm real,
    revenue_ttm real,
    operating_expenses_ttm real,
    gross_profit_ttm real,
    roa_percent_ly real,
    total_equity_lq real
);


ALTER TABLE public.test_data1 OWNER TO postgres;

--
-- TOC entry 3314 (class 0 OID 16421)
-- Dependencies: 209
-- Data for Name: test_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_data1 (date, ticker, price, market_cap, fcf_ttm, fcf_lq, net_income_ttm, net_income_lq, operating_cash_flow_ttm, total_assets, beta_5y_mo_end, roa_ttm, net_income_ly, total_assets_ly, long_term_debt, long_term_debt_ly, current_ratio, current_assets, current_liabilities, current_assets_ly, current_liabilities_ly, current_ratio_ly, shares_outstanding, shares_outstanding_ly, gross_margin_percent_ttm, gross_margin_percent_lq, gross_margin_percent_ly, asset_turnover_ratio, asset_turnover_ratio_ly, total_debt_to_total_equity_lq, total_assets_lq, total_revenue_lq, roic_percent_ttm, ebit_ttm, ev, p_to_b_daily, p_to_e_daily, ebita_ttm, revenue_ttm, operating_expenses_ttm, gross_profit_ttm, roa_percent_ly, total_equity_lq)
FROM '/docker-entrypoint-initdb.d/data/SP500_Test_Small_Time_1.0.csv'
DELIMITER ','
CSV HEADER;