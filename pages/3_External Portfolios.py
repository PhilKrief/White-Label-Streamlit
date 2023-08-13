import pandas as pd
import streamlit as st
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import matplotlib.pyplot as plt
import copy 
from datetime import datetime, timedelta
import requests
from utils import *
from finance_functions import *


key = "d8eabf9ca1dec61aceefd4b4a9b93992"
common_elements_investmentora()
page_header("Example of External Portfolio")


start_date = st.sidebar.date_input("Start Date: ")
end_date = st.sidebar.date_input("End Date: ")
#key = st.sidebar.text_input("API KEY: ")

df = pd.DataFrame(columns=['Ticker', 'Allocation'],index=np.arange(2))

edited_df = st.experimental_data_editor(df, num_rows="dynamic")
tickers = edited_df['Ticker'].tolist()

bench = st.selectbox(
    'Which benchmark will you choose ?',
    ('SPY', 'QQQ', 'DIA', "IWM"))

bench_prices = get_monthly_stock_portfolio_prices([bench], key)
bench_returns = calculate_returns(bench_prices)
bench_returns = bench_returns.rename({bench: "BenchmarkReturns"}, axis=1)

portfolio_prices = get_monthly_stock_portfolio_prices(tickers, key)
portfolio_returns = calculate_returns(portfolio_prices)

allocations = allocation_df(edited_df, portfolio_returns)
portfolio_returns = calculate_portfolio_returns(allocations, portfolio_returns)
portfolio_returns = portfolio_returns.rename("PortfolioReturns")
portfolio_returns = portfolio_returns.to_frame()


portfolio_returns = portfolio_returns[::-1]
bench_returns = bench_returns[::-1] 
######

st.session_state["periodes"] = st.sidebar.multiselect("QWhat time periiod would you like to calculate the financial metrics",options=[1,3,5,10], default=1)

indice = st.sidebar.checkbox("Would you like to include the benchmark? ")
million = st.sidebar.checkbox("Would you like to see the performance in millions? ")

fees = st.sidebar.number_input("Annual Fees")
risk_free_rate = st.sidebar.number_input("Risk Free Rate", value=0.02)
indices_df = pd.DataFrame(index = bench_returns.index, columns=['Marché monétaire'])
indices_df['Marché monétaire'] = float(risk_free_rate)/12

    
graph_df = pd.DataFrame()
graph_df.index = portfolio_returns.index

if fees: 
    monthly = fees / 1200
    portfolio_returns = portfolio_returns - monthly

financial_metrics = pd.DataFrame()
financial_metrics['Index'] = ['Fonds', 'Date de début', 'Date de fin', 'Rendement brut (période)', 'Rendement indice (période)', 'Rendement brut (annualisée)', 'Rendement indice (annualisée)', 'Valeur ajoutée (période)', 'Valeur ajoutée annualisée', 'Risque actif annualisé', 'Ratio information', 'Beta', 'Alpha annualisé', 'Ratio sharpe', 'Coefficient de corrélation', 'Volatilité annualisée du fonds', "Volatilité annualisée de l'indice"]

bench_returns = bench_returns.rename({"BenchmarkReturns": "PortfolioReturns"}, axis=1)
metrique = financial_metric_table(st.session_state["periodes"], portfolio_returns, bench_returns, indices_df, "PortfolioReturns")
cols = [i for i in list(metrique.columns) if i != 'Index']
financial_metrics[cols] = metrique[cols]

financial_metrics.set_index("Index", inplace=True)

percentage_rows = ["Rendement brut (période)", "Rendement indice (période)", "Rendement brut (annualisée)", "Rendement indice (annualisée)", "Valeur ajoutée (période)", "Valeur ajoutée annualisée","Volatilité annualisée du fonds", "Volatilité annualisée de l'indice"]
number_rows  = ["Risque actif annualisé", "Ratio information", "Beta", "Alpha annualisé", "Ratio sharpe", "Coefficient de corrélation"]

for row in percentage_rows:
    financial_metrics.loc[row,] = financial_metrics.loc[row,].astype(float)
    financial_metrics.loc[row,] = financial_metrics.loc[row,].apply('{:.2%}'.format)
for row in number_rows:
    financial_metrics.loc[row,] = financial_metrics.loc[row,].astype(float)
    financial_metrics.loc[row,] = financial_metrics.loc[row,].apply('{:.2}'.format)

return_rows = ["Rendement brut (période)", "Rendement indice (période)", "Rendement brut (annualisée)", "Rendement indice (annualisée)", "Valeur ajoutée (période)", "Valeur ajoutée annualisée"]

risk_rows = ["Risque actif annualisé", "Ratio information", "Beta", "Alpha annualisé", "Ratio sharpe", "Coefficient de corrélation", "Volatilité annualisée du fonds", "Volatilité annualisée de l'indice"]

return_metrics = financial_metrics.loc[return_rows,]
risk_metrics = financial_metrics.loc[risk_rows,]


return_rows_en = {"Rendement brut (période)":"Gross Return (Period)", "Rendement indice (période)":"Benchmark Return (Period)", "Rendement brut (annualisée)":"Gross Return (Annualized)", "Rendement indice (annualisée)":"Benchmark Return (Annualized)", "Valeur ajoutée (période)":"Added Value (Period)", "Valeur ajoutée annualisée":"Added Value (Annualized)"}
risk_rows_en = {"Risque actif annualisé":"Annualized Active Risk", "Ratio information":"Information Ratio", "Beta":"Beta", "Alpha annualisé":"Annualized Alpha", "Ratio sharpe":"Sharpe Ratio", "Coefficient de corrélation":"Correlation Coefficient", "Volatilité annualisée du fonds":"Annualized Volality", "Volatilité annualisée de l'indice":"Benchmark Annualized Volality"}

return_metrics.rename(index=return_rows_en, inplace=True)
risk_metrics.rename(index=risk_rows_en, inplace=True)

rendement_mandat = ((1 + portfolio_returns).cumprod())
rendement_bench = ((1 + bench_returns).cumprod())
print(rendement_bench)
if million:
    rendement_mandat_graph = rendement_mandat * 1000000
    rendement_bench_graph = rendement_bench * 1000000
else:
    rendement_mandat_graph = rendement_mandat 
    rendement_bench_graph = rendement_bench 


#profile = st.session_state['profile']
graph_df['PortfolioReturns'] = rendement_mandat_graph['PortfolioReturns']
if indice:
    graph_df['BenchmarkReturns'] = rendement_bench_graph['PortfolioReturns']

        
st.line_chart(graph_df)
return_col, risk_col = st.columns([1, 1])
return_col.markdown("<h2 style='text-align: center;'>Returns</h2>", unsafe_allow_html=True)
return_col.dataframe(return_metrics, use_container_width=True)

risk_col.markdown("<h2 style='text-align: center;'>Risks</h2>", unsafe_allow_html=True)
risk_col.dataframe(risk_metrics, use_container_width=True)


