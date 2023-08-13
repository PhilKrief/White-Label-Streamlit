import yfinance as yf
from yahooquery import Ticker
from finance_functions import *
import pandas as pd
import numpy as np
import streamlit as st


def get_stock_evolution(company_name, num_simulations, period):
    # Get the stock information
    stock = yf.Ticker(company_name)

    # Get historical market data
    hist = stock.history(period=period, interval='1mo')
    hist['Returns'] = hist.Open.pct_change()

    average_return = hist['Returns'].mean()
    std_dev = hist['Returns'].std()

    simulation_returns = np.random.normal(average_return, std_dev, size=(len(hist), num_simulations))
    df = pd.DataFrame(simulation_returns, index=hist.index)
    print(df)

    df['Returns'] = df.mean(axis=1)

    df = df[['Returns']]
    df['cumul_return'] = (df['Returns'] + 1).cumprod()
    return df

def investment_amount(df, initial_amount, monthly_contribution, fees):
    # User input: initial investment amount and monthly contribution
    monthly_fees = fees/1200
    
    # Calculate total portfolio value
    df = df.reset_index()
    df['Portfolio Value'] = 0
    df.loc[0, 'Portfolio Value'] = initial_amount
    df['Net_Returns'] = df['Returns'] - monthly_fees

    for i in range(1,len(df)):
        previous_value = df.loc[i - 1, 'Portfolio Value']
        monthly_returns = 1 + df.loc[i, 'Net_Returns']
        df.loc[i, 'Portfolio Value'] = (previous_value + monthly_contribution) * monthly_returns
    df = df.set_index('Date')
    print(df)
    return df


if 'simulation' not in st.session_state:
    st.session_state['simulation'] = []
if 'initial_amount' not in st.session_state:
    st.session_state['initial_amount'] = []
if 'monthly_contribution' not in st.session_state:
    st.session_state['monthly_contribution'] = []
if 'fees' not in st.session_state:
    st.session_state['fees'] = []
if 'datafile' not in st.session_state:
    st.session_state['datafile'] = []
    
st.title("Scenario Analysis App")

owndata = st.sidebar.checkbox("Want to use your own data?")
st.session_state["datafile"] = st.sidebar.file_uploader("Please upload an excel file: ", type=['xlsx'])

st.sidebar.write("Portfolio 1")
initial_amount = st.sidebar.number_input("Initial Investment for 1st Portfolio")
monthly_contributions = st.sidebar.number_input("Monthly Contributions for 1st Portfolio")
fees = st.sidebar.number_input("Annual Fees for 1st Portfolio", step = 0.1, format="%0.3f")
st.sidebar.write("Portfolio 2")
initial_amount2 = st.sidebar.number_input("Initial Investment for 2nd Portfolio")
monthly_contributions2 = st.sidebar.number_input("Monthly Contributions for 2nd Portfolio")
fees2 = st.sidebar.number_input("Annual Fees for 2nd Portfolio", step = 0.1, format="%0.3f")


if owndata:
    if not st.session_state['datafile']:
        st.warning("Please upload your own data")
    else:
        # Create an ExcelFile object using pandas
        excel_file = pd.ExcelFile(st.session_state.datafile)

        # Get the sheet names from the Excel file
        sheet_names = excel_file.sheet_names
        sheet = st.selectbox(
            'Which sheet has the returns data?', sheet_names)
        data = pd.read_excel(st.session_state.datafile, sheet_name=sheet)
        date_col = st.selectbox("Which column has the date information", data.columns)
        data.rename({date_col:"Date"}, axis = 1, inplace=True)
        data.set_index("Date", inplace=True)
        portfolio_col = st.selectbox("Which column has the portfolio information", data.columns)
        
        df = data[[portfolio_col]]
        df.rename({portfolio_col:"Returns"}, axis = 1, inplace=True)
        df['cumul_return'] = (df['Returns'] + 1).cumprod()
        
        
        #data_editted =  st.data_editor(data)
        

else:
    simulations = int(st.sidebar.number_input("Number of simulations"))
    period = st.sidebar.selectbox("Which time period would you like to use?", options = ('10y', '1d',"5d","1mo","3mo","6mo","1y","2y","5y","ytd","max"))
    if simulations and period:
        ETF = st.selectbox(
            'Which index would you like to simulate?',
            ('SPY', 'QQQ', 'DIA', "IWM"))
    
        if st.button("Generate simulation"):
            df = get_stock_evolution(ETF, simulations, period)
            st.session_state['simulation'] = df
    else: 
        st.warning("Please select the number of simulations and period")
    
    if len(st.session_state['simulation'])>=1:
        df = st.session_state['simulation']

    if initial_amount:
        st.session_state.initial_amount.append(initial_amount)

    if monthly_contributions:
        st.session_state.monthly_contribution.append(monthly_contributions)

    if fees:
        st.session_state.fees.append(fees)

    if initial_amount2:
        st.session_state.initial_amount.append(initial_amount2)

    if monthly_contributions2:
        st.session_state.monthly_contribution.append(monthly_contributions2)

    if fees2:
        st.session_state.fees.append(fees2)


if initial_amount and monthly_contributions and fees:
    df = investment_amount(df, initial_amount, monthly_contributions, fees)
    df = df.rename({"Portfolio Value":"Portfolio 1 Value"}, axis=1)
    df2 = investment_amount(df, initial_amount2, monthly_contributions2, fees2)
    df2 = df2.rename({"Portfolio Value":"Portfolio 2 Value"}, axis=1)

    graph = pd.DataFrame([df['Portfolio 1 Value'], df2['Portfolio 2 Value']]).T
    print(graph)
    st.line_chart(graph)
    #st.line_chart()
    
    # Get final values of portfolios broken down by contributions and cap gains
    df = df.reset_index()
    final_amount = df.loc[len(df)-1, 'Portfolio 1 Value']
    st.write(f"The final portfolio 1 value with an initial investment of {initial_amount:,.2f} and monthly contributions of {monthly_contributions:,.2f} is equal to $ {final_amount:,.2f}. \n The final portfolio 1 has a capital invested of {(initial_amount+monthly_contributions*len(df)):,.2f} and {(final_amount-(initial_amount+monthly_contributions*len(df))):,.2f} of capital gains")

    df2 = df2.reset_index()
    final_amount2 = df2.loc[len(df2)-1, 'Portfolio 2 Value']
    st.write(f"The final portfolio 2 value with an initial investment of {initial_amount2:,.2f} and monthly contributions of {monthly_contributions2:,.2f} is equal to $ {final_amount2:,.2f}. \n The final portfolio 1 has a capital invested of {(initial_amount2+monthly_contributions2*len(df2)):,.2f} and {(final_amount2-(initial_amount2+monthly_contributions2*len(df))):,.2f} of capital gains")

    st.write(f"The difference in the two scenarios is. \n ")

    differences = pd.DataFrame(([initial_amount, initial_amount2, (initial_amount-initial_amount2)], 
                                [monthly_contributions, monthly_contributions2, monthly_contributions-monthly_contributions2],
                                [initial_amount+monthly_contributions*len(df), initial_amount2+monthly_contributions2*len(df2), initial_amount+monthly_contributions*len(df) - (initial_amount2+monthly_contributions2*len(df2))],
                                [final_amount-(initial_amount+monthly_contributions*len(df)), final_amount2-(initial_amount2+monthly_contributions2*len(df2)), final_amount-(initial_amount+monthly_contributions*len(df))- (final_amount2-(initial_amount2+monthly_contributions2*len(df2)))],
                                [final_amount, final_amount2, final_amount-final_amount2]),
                            columns=['Portfolio 1', 'Portfolio 2', 'Difference'], 
                            index = ['Initial Amount', 'Contribution', 'Total Amount Invested', 'Capital Gains', 'Final Amount'])
    st.dataframe(differences)


elif 'df' in locals():
    st.line_chart(df['cumul_return'])
else:
    st.warning("Please generate a simulation")






