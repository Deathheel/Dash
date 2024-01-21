import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px


st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")


# Connect to the MySQL database (replace placeholders with your credentials)
engine = create_engine('mysql://sql12678617:FtL1h1vtpZ@sql12.freesqldatabase.com/sql12678617')

# Cached function for efficient data retrieval
def update_data():
    with engine.connect() as conn:
        df = pd.read_sql_table('data', conn)
    return df

df = update_data()


def get_targets_for_position(position):
    if position == "Sales Senior":
        return {"leads": 52, "prospect": 36, "hot": 24, "spk": 12, "do": 6}
    elif position == "Sales Trainee":
        return {"leads": 52, "prospect": 12, "hot": 8, "spk": 4, "do": 2}
    # Add target logic for other positions as needed
    else:
        return {}  # Handle cases where position has no targets

def group_month_year(month):
    month = pd.to_datetime(month)  # Convert to datetime object
    return f"{month.strftime('%b')} {month.year}"

st.session_state.selected_staff = None
st.session_state.available_months = None

def filter_months(selected_staff):
    st.session_state.available_months = df[df['nama'] == selected_staff]['bulan'].dt.strftime('%b %Y').unique()

# Sidebar for filtering, using original bulan values
st.sidebar.title("Filter Data")
selected_staff = st.sidebar.selectbox("Select Staff", df['nama'].unique())

if selected_staff != st.session_state.selected_staff:
    filter_months(selected_staff)  # Update available months if staff selection changes
    st.session_state.selected_staff = selected_staff

selected_month = st.selectbox("Select Month & Year", st.session_state.available_months, key="month_year", format_func=group_month_year)

# Filter data based on selections
filtered_df = df[df['nama'] == selected_staff]  # Filter by nama first
filtered_df = filtered_df[filtered_df['bulan'].dt.strftime('%b %Y') == selected_month]  # Filter by bulan after nama
# Display filtered data, formatting bulan only for display
st.title(":bar_chart: Sales Staff Performance for " + str(pd.to_datetime(selected_month).strftime("%B %Y")))

st.dataframe(filtered_df)

# Calculate additional performance metrics
selected_position = filtered_df['jabatan'].iloc[0]  # Use 'jabatan' for position
selected_position_targets = get_targets_for_position(selected_position)

if selected_position_targets:
    leads_actual = filtered_df['leads'].sum()
    st.metric("Leads", leads_actual, f"({leads_actual / selected_position_targets['leads'] * 100:.2f}% of Target)")

    prospect_actual = filtered_df['prospect'].sum()
    st.metric("Prospect", prospect_actual, f"({prospect_actual / selected_position_targets['prospect'] * 100:.2f}% of Target)")

    hot_actual = filtered_df['hot'].sum()
    st.metric("Hot", hot_actual, f"({hot_actual / selected_position_targets['hot'] * 100:.2f}% of Target)")

    spk_actual = filtered_df['spk'].sum()
    st.metric("SPK", spk_actual, f"({spk_actual / selected_position_targets['spk'] * 100:.2f}% of Target)")

    do_actual = filtered_df['do'].sum()
    st.metric("DO", do_actual, f"({do_actual / selected_position_targets['do'] * 100:.2f}% of Target)")


# Add filtering controls for the chart (separate from sidebar)
st.markdown("##")
st.title(":bar_chart: Chart Filters")
st.markdown("##")

# Filter months based on selected staff, disregarding sidebar month
filtered_months_for_chart = df[df['nama'] == st.session_state.selected_staff]['bulan'].dt.strftime('%b %Y').unique()

bulan_selection = st.multiselect("Select Months", options=filtered_months_for_chart)
metric_selection = st.multiselect("Select Metrics", options=['leads', 'prospect', 'hot', 'spk', 'do'], default=['leads'])

# Filter data for the chart based on selected staff and chart-specific months
# Filter data for the chart based on selected staff and chart-specific months
filtered_df_for_chart = df[df['nama'] == st.session_state.selected_staff]  # Filter by nama first

if bulan_selection:  # Check if any months are selected
    bulan_selection_dates = pd.to_datetime([f"01 {month}" for month in bulan_selection])
    filtered_df_for_chart = filtered_df_for_chart[filtered_df_for_chart['bulan'].dt.to_period('M').isin(bulan_selection_dates.to_period('M'))]

    # Create and update the chart layout only if bulan_selection_dates is defined
    fig = px.line(
        filtered_df_for_chart,
        x=filtered_df_for_chart['bulan'].dt.strftime('%b %Y'),
        y=metric_selection,
        category_orders=filtered_df_for_chart['bulan'].dt.strftime('%b %Y'),
        title="Sales Performance Over Time",
    )

    fig.update_layout(xaxis_range=(bulan_selection_dates.min(), bulan_selection_dates.max()))
    # Optional: Customize bar colors and patterns
    fig.update_traces(
        marker_color=["blue"],
    )

    st.plotly_chart(fig)

    st.dataframe(filtered_df_for_chart)
