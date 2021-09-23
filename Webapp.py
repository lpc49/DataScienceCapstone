# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#defining the pie charts for task 2
#for the option 'ALL' we show the percentage of success per site
data_all = spacex_df[['Launch Site','class']]
data_all = data_all.groupby(['Launch Site']).sum()/data_all[['class']].sum()

#for the other options we show the success rate for the selected option
data_each = spacex_df[['Launch Site','class']]
data_each = data_each.groupby(['Launch Site']).sum()/data_each.groupby(['Launch Site']).count()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0 kg',
                                        2500: '2 500 kg',
                                        5000: '5 000 kg',
                                        7500: '7 500 kg',
                                        10000: '10 000 kg'},
                                    value=[2500 , 8000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
 
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data_all, values='class', 
        names=data_all.index, 
        title='Total successful launches by site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data_selected_site = pd.DataFrame({'class': [1-data_each.at[entered_site, 'class'], data_each.at[entered_site, 'class']] },
                                            index = ['Failure','Success'])
        fig = px.pie(data_selected_site, values='class', 
        names=data_selected_site.index, 
        title='Total successful launches for site '+entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between payload and success for all sites')
        fig.update_xaxes(range=payload_range)
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        # return the outcomes piechart for a selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between payload and success for site '+entered_site)
        fig.update_xaxes(range=payload_range)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
