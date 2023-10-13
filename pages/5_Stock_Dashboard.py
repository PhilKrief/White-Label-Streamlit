import streamlit as st

# Define the number of rows and columns
num_rows = 3
num_cols = 3

# Create an empty 2D list to store table data
table_data = [['' for _ in range(num_cols)] for _ in range(num_rows)]

# Display a text input widget for each cell in the table
for i in range(num_rows):
    for j in range(num_cols):
        table_data[i][j] = st.text_input(f'Cell ({i+1}, {j+1})', table_data[i][j])

# You can add CSS styling here if needed
# st.markdown("""
# <style>
#    /* Your CSS styles here */
# </style>
# """, unsafe_allow_html=True)

# Display the table-like structure
st.table(table_data)
