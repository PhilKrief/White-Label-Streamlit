import pandas as pd
import streamlit as st
import numpy as np
from utils import * 
from finance_functions import * 
import matplotlib.pyplot as plt


def reindex_list(order, total_list):
    """function receives two lists, order and total_list. It returns a list with the elements of order and the elements of total_list that are not in order, to the end of the list"""
    diff = list(set(total_list) - set(order))
    order = order + diff

    return order


#Title
st.title("Net Worth Summary")

#import net worth data
df = pd.read_excel("Net Worth Data.xlsx", sheet_name="Sheet1")

#Add options for the user to choose from
option = st.selectbox(
    'Which client would you like to see?',
    df.Client.unique())

#split the page in 2 columns
col1, col2 = st.columns(2)

#Filter Data for client
df = df[df.Client == option]    

#
data = df.groupby(['Asset Type',	'Asset Ownership',	'Asset Category',	'Account institution',	'Account type'])[['Book Value', 'Fair Market Value']].sum()



account_types = list(data.index.get_level_values(4).unique())
account_types_order = ["Cash Account", "Non Registered", "RRSP", "TFSA", "Primary Residence", "Vacation Residence"]
account_types_order = reindex_list(account_types_order, account_types)
data = data.reindex(account_types_order, level="Account type")

asset_categories = list(data.index.get_level_values(2).unique())
asset_categories_order = ["Cash", "Investments", "Properties", "Other"]
asset_categories_order = reindex_list(asset_categories_order, asset_categories)
data = data.reindex(asset_categories_order, level="Asset Category")


asset_ownerships = list(data.index.get_level_values(1).unique())
asset_ownerships_order = ["Personal", "Joint", "Corporate"]
asset_ownerships_order = reindex_list(asset_ownerships_order, asset_ownerships)
data = data.reindex(asset_ownerships_order, level="Asset Ownership")

asset_types = list(data.index.get_level_values(0).unique())
asset_types_order = ["Liquid", "Fixed Assets"]
asset_types_order = reindex_list(asset_types_order, asset_types)
data = data.reindex(asset_types_order, level="Asset Type")


data = data.reset_index()
data_total = data[['Book Value', 'Fair Market Value']].sum()



# Format Streamlit App and Tables

account_institution = []
final_table = pd.DataFrame(columns=['Assets', 'Book Value', 'Fair Market Value'])

for asset_type in asset_types_order:
    final_table.loc[len(final_table), "Assets"] = asset_type
    final_table.loc[len(final_table)-1, "Book Value"] = data[data['Asset Type'] == asset_type]['Book Value'].sum()
    final_table.loc[len(final_table)-1, "Fair Market Value"] = data[data['Asset Type'] == asset_type]['Fair Market Value'].sum()
    for asset_ownership in asset_ownerships_order:
        final_table.loc[len(final_table), "Assets"] = asset_ownership
        final_table.loc[len(final_table)-1, "Book Value"] = data[(data['Asset Type'] == asset_type) & (data['Asset Ownership'] == asset_ownership)]['Book Value'].sum()
        final_table.loc[len(final_table)-1, "Fair Market Value"] = data[(data['Asset Type'] == asset_type) & (data['Asset Ownership'] == asset_ownership)]['Fair Market Value'].sum()
        for asset_category in asset_categories_order:
            final_table.loc[len(final_table), "Assets"] = asset_category
            dummy = data[(data['Asset Type'] == asset_type) & (data['Asset Ownership'] == asset_ownership) & (data['Asset Category'] == asset_category)]
            final_table.loc[len(final_table)-1, "Book Value"] = dummy['Book Value'].sum()
            final_table.loc[len(final_table)-1, "Fair Market Value"] = dummy['Fair Market Value'].sum()
            if len(dummy) > 0:
                for i in range(len(dummy)):
                    final_table.loc[len(final_table), "Assets"] = dummy.iloc[i]['Account institution']+" - "+dummy.iloc[i]['Account type']
                    account_institution.append(dummy.iloc[i]['Account institution']+" - "+dummy.iloc[i]['Account type'])
                    final_table.loc[len(final_table)-1, "Book Value"] = dummy.iloc[i]['Book Value']
                    final_table.loc[len(final_table)-1, "Fair Market Value"] = dummy.iloc[i]['Fair Market Value']

final_table= final_table.replace(0,np.nan)
final_table = final_table.dropna()

# Format the 'Value' column as dollars (with dollar signs and commas)
final_table['Book Value'] = final_table['Book Value'].map('${:,.2f}'.format)
# Format the 'Value' column as dollars (with dollar signs and commas)
final_table['Fair Market Value'] = final_table['Fair Market Value'].map('${:,.2f}'.format)
            
# Define custom CSS for styling the table
custom_css = """
<style>
    table {
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    th {
        background-color: #f2f2f2;
    }
    th:first-child, td:first-child {
        padding-left: 16px;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .bold {
        font-weight: bold;
    }
</style>
"""

# Convert the DataFrame to HTML
final_table['Assets'] = final_table['Assets'].apply(lambda x: '&nbsp;&nbsp;' + x if x in asset_ownerships_order else x)

final_table['Assets'] = final_table['Assets'].apply(lambda x: '&nbsp;&nbsp;' + x if x in asset_categories_order else x)

final_table['Assets'] = final_table['Assets'].apply(lambda x: '&nbsp;&nbsp;&nbsp;&nbsp;' + x if x in account_institution else x)



fig, ax = plt.subplots()
pie_data = df.groupby(['Asset Class'])[['Fair Market Value']].sum().reset_index()
total_value = pie_data['Fair Market Value'].sum()

# Calculate the weight column (as a percentage of the total)
pie_data['Weight (%)'] = round((pie_data['Fair Market Value'] / total_value) * 100,2)

# Sort the data by weight descending
ax.pie(pie_data['Fair Market Value'], labels=pie_data['Asset Class'],  startangle=90)
#ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart using Streamlit
col2.pyplot(fig)

pie_data.loc[len(pie_data), "Asset Class"] = "Total"
pie_data.loc[len(pie_data)-1, "Fair Market Value"] = pie_data['Fair Market Value'].sum()
pie_data.loc[len(pie_data)-1, "Weight (%)"] = round(pie_data['Weight (%)'].sum(),0)

pie_data['Fair Market Value'] = pie_data['Fair Market Value'].map('${:,.2f}'.format)  

# Identify and make the "Total" row bold



pie_data.loc[pie_data['Asset Class'] == 'Total', 'Fair Market Value'] = pie_data.loc[pie_data['Asset Class'] == 'Total', 'Fair Market Value'].apply(lambda x: f'<span class="bold">{x}</span>')

pie_data.loc[pie_data['Asset Class'] == 'Total', 'Weight (%)'] = pie_data.loc[pie_data['Asset Class'] == 'Total', 'Weight (%)'].apply(lambda x: f'<span class="bold">{x}</span>')

pie_data.loc[pie_data['Asset Class'] == 'Total', 'Asset Class'] = pie_data.loc[pie_data['Asset Class'] == 'Total', 'Asset Class'].apply(lambda x: f'<span class="bold">{x}</span>')

print(pie_data)

pie_html = pie_data.to_html(classes='table',escape=False, index=False) 
# Combine the custom CSS and table HTML
styled_pie = custom_css + pie_html

# Render the styled HTML using st.markdown
col1.markdown(styled_pie, unsafe_allow_html=True)

# Convert the DataFrame to HTML
table_html = final_table.to_html(classes='table',escape=False, index=False) 
# Combine the custom CSS and table HTML
styled_html = custom_css + table_html

# Render the styled HTML using st.markdown
st.markdown(styled_html, unsafe_allow_html=True)