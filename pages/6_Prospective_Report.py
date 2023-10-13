import streamlit as st
import matplotlib.pyplot as plt
import base64
from io import BytesIO


st.set_page_config(layout="wide")

# Updated CSS for refined design
st.write("""
<style>
    /* General styling */
    .reportview-container {
        flex-direction: column;
        background-color: #f9f9f9; /* Light gray background */
    }
    .big-font {
        font-size: 24px !important;
    }
    .blue-font {
        color: #2C3E50;  /* Dark Blue Color */
    }

    /* Styling for the Review of Assets section */
    .asset-box {
        border: 1px solid #d1d1d1;
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0;
        background-color: #ffffff; /* White background for content boxes */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-font blue-font'>KS Investments</div>", unsafe_allow_html=True)
st.markdown("### Prospective Report Prepared for John Doe")

# Section 1: Review of Assets with Updated Design
st.write("## Review of Assets")

# Layout columns for this section
col1, col2, col3 = st.columns(3)

# Pie chart content for the left column
pie_chart_content = """
<div class='asset-box'>
    <h3>Asset Allocation</h3>
    Placeholder for Pie Chart
</div>
"""

# Net Worth Summary content for the middle column
net_worth_data = {
    "Equities": "$50,000.00",
    "Fixed Income": "$40,000.00",
    "House": "$40,000.00",
    "Cash Flows": "$3,000.00"
}
net_worth_content = "<div class='asset-box'><h3>Net Worth Summary</h3>"
for key, value in net_worth_data.items():
    net_worth_content += f"<p>{key}: {value}</p>"
net_worth_content += "</div>"

# Transactions and Cash Flow content for the right column
transactions_data = {
    "Date": ["Jan-24", "Feb-24", "Mar-24"],
    "Amount": ["$6,000", "$7,500", "$8,000"],
    "Description": ["Vacation", "Cottage Down Payment", "Lump Sum Mortgage Payment"]
}
transactions_content = "<div class='asset-box'><h3>Transactions and Cash Flow</h3><table>"
for idx in range(len(transactions_data["Date"])):
    transactions_content += f"<tr><td>{transactions_data['Date'][idx]}</td><td>{transactions_data['Amount'][idx]}</td><td>{transactions_data['Description'][idx]}</td></tr>"
transactions_content += "</table></div>"

# Display the content in the columns
col1.markdown(pie_chart_content, unsafe_allow_html=True)
col2.markdown(net_worth_content, unsafe_allow_html=True)
col3.markdown(transactions_content, unsafe_allow_html=True)




# Section 2: Cash Flow Projection Timeline
st.write("## Cash Flow Projection Timeline")

# Placeholder data for cash flow projection
dates = ["Jan-24", "Feb-24", "Mar-24", "Apr-24", "May-24"]
cash_flow = [6000, 6500, 7000, 7500, 8000]

# Calculate average cash flow
average_cash_flow = sum(cash_flow) / len(cash_flow)

# Calculate the difference from the average for each cash flow value
difference_from_average = [cf - average_cash_flow for cf in cash_flow]

# Plotting the bar chart where x-axis represents the average cash flow
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(dates, difference_from_average, color=['g' if diff > 0 else 'r' for diff in difference_from_average])

# Highlighting the zero line to represent average
ax.axhline(y=0, color='black', linestyle='-')
ax.set_title("Difference from Average Cash Flow")
ax.set_ylabel("Difference from Average")
ax.set_xlabel("Time Period")
ax.text(0.02, 0.95, f'Average Cash Flow: ${average_cash_flow:.2f}', transform=ax.transAxes, fontsize=10)

# Display positive differences above bars
for bar in bars:
    yval = bar.get_height()
    if yval > 0:
        ax.text(bar.get_x() + bar.get_width()/2, yval + 50, round(yval, 2), ha='center', va='bottom', fontsize=8)

fig.tight_layout()
# Save the bar chart figure as an image
buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)

# Encode the image to Base64
encoded_image = base64.b64encode(buffer.getvalue()).decode()


# Displaying the bar chart in a styled box
bar_chart_content = f"""
<div class='asset-box'>
    <h3>Cash Flow Projection</h3>
    <img src="data:image/png;base64,{encoded_image}" alt="Bar Chart" style="width:100%;"/>
</div>
"""
st.markdown(bar_chart_content, unsafe_allow_html=True)


#st.write("""
#Note: This is the updated design for Section 2 with a bar chart and average cash flow line.
#""")

# Section 3: Scheduling
st.write("## Scheduling")

# Layout columns for this section
col1, col2 = st.columns(2)

# Goal-Based Schedule in the left column

goals = [
    {"goal": "Vacation", "date": "Jan-24", "status": "on time"},
    {"goal": "Cottage Down Payment", "date": "Feb-24", "status": "delay"},
    {"goal": "Lump Sum Mortgage Payment", "date": "Mar-24", "status": "danger"}
]

# Define colors for each status
status_colors = {
    "on time": "green",
    "delay": "yellow",
    "danger": "red"
}


# Action Plans in the right column

action_plans = [
    {"plan": "TFSA Contribution", "date": "Jan-24"},
    {"plan": "RRSP Contribution", "date": "Feb-24"},
    {"plan": "Spouse RRSP Contribution", "date": "Mar-24"}
]

goal_based_content = "<div class='asset-box'><h3>Goal-Based Schedule</h3>"
for goal in goals:
    goal_based_content += f"<p style='background-color: {status_colors[goal['status']]}; padding: 5px; margin: 5px 0;'>{goal['goal']} - {goal['date']}</p>"
goal_based_content += "</div>"

# Action Plans content for the right column
action_plans_content = "<div class='asset-box'><h3>Action Plans</h3>"
for plan in action_plans:
    action_plans_content += f"<p>{plan['plan']} - {plan['date']}</p>"
action_plans_content += "</div>"

# Display the content in the columns for Section 3
col1, col2 = st.columns(2)
col1.markdown(goal_based_content, unsafe_allow_html=True)
col2.markdown(action_plans_content, unsafe_allow_html=True)


#st.write("""
#Note: This is the design for Section 3. Color-coding and placeholder data are used for demonstration.
#""")

# Section 4: Notes and Comments
st.write("## Notes and Comments")
st.text_area("Add your notes here...")

#st.write("""
#Note: This completes the design for Section 4 and the entire dashboard.
#""")

