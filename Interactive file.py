# Importing my modules
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Reading in the Dataset as a CSV
df = pd.read_csv(r"C:\Users\Dell\Desktop\Pandas assignments\IOT-temp.csv")  # Update with the correct file path

# Converting the date  column to date time so I can use just the month.
df["noted_date"] = pd.to_datetime(df["noted_date"], format='mixed')

# Month names for filtering
df["Month"] = df["noted_date"].dt.strftime('%B')

# Created a Dash app
app = Dash(__name__)

# Dashboard Layout
app.layout = html.Div([
    html.H1("Temperature Readings", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in df["Month"].unique()],
        value=df["Month"].unique()[0],  # Opening selection
        clearable=False,
        style={'width': '50%'}
    ),

    dcc.Graph(id='scatter-plot')
])

# Callback to update scatter plot based on selected month
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('month-dropdown', 'value')
)
def update_scatter(selected_month):
    # Filter data based on selected month
    filtered_df = df[df["Month"] == selected_month]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x="noted_date",
        y="temp",
        color="id",  # Different colors for different id logs
        title=f"Temperature Readings in {selected_month}",
        labels={"noted_date": "Date", "temp": "Temperature (°C)"},
        hover_data=["id"]
    )

    return fig

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)