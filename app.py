import pandas as pd
import streamlit as st
from utils import *

common_elements_investmentora()

def main():
    # Add custom CSS styles
   st.markdown(
        """
        <style>
        /* Add your custom CSS styles here */
        .custom-header {
            font-size: 24px;
            color: #000000;
            margin-bottom: 16px;
        }
        .section {
            background-color: #f7f7f7;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True, )

    # Title and Introduction
    #Page Titles
   
   page_header("Analysis and Automation Tool")



   # Overview Section

   overview_html = f"""<div class="section">
   <div class="custom-header">Overview</div>
   <p>This tool allows wealth managers to: attribute a risk profile based on a questionnaire, compare the attributed portfolio to its benchmark while calculating key financial metrics (Alpha, Beta, Sharpe Ratio, etc.), as well as create a portfolio and view its performance over time, calculate key financial metrics and compare it to a chosen benchmark.</p>
   </div>"""

   st.markdown(overview_html, unsafe_allow_html=True)
   st.write("---")  # Horizontal line for visual separation
   guide_html = f"""<div class="section">
   <div class="custom-header">User Guide</div>
   <p>Questionnaire : User can input personal data, while answering a questionnaire. The tool will then recommend a risk profile that is associated with a model portfolio</p> 
    <p>Private Mandates : User can choose from a list of model portfolios and view performance compared to a benchmark, financial metrics</p>
    <p>External Portfolio : User can input a portfolio with tickers and allocations, and view performance compared to a chosen benchmark as well as financial metrics </p></div>"""
   st.markdown(guide_html, unsafe_allow_html=True)
   st.write("---")  # Horizontal line for visual separation

   GPD = st.radio("Would you like to continue with model portfolios ", ("Yes", "No"))

   if GPD=="Yes":
      guide = st.radio(" ", ("I would like to fill out the questionnaire", "I would like to choose my own portfolio"), label_visibility="hidden")
      if GPD and (guide == "I would like to fill out the questionnaire"):
         st.markdown('<a href="https://investmentora.streamlit.app/Information" target="_self" >Questionnaire</a>', unsafe_allow_html=True)
      if GPD and (guide == "I would like to choose my own portfolio"):  
         st.markdown('<a href="https://investmentora.streamlit.app/Model_Portfolios" target="_self">Model Portfolios</a>', unsafe_allow_html=True)
   else:
      st.markdown('<a href="https://investmentora.streamlit.app/External_Portfolios" target="_self">External Portfolios</a>', unsafe_allow_html=True)


if __name__ == "__main__":
   main()





