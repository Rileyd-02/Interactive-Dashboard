#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv("/Users/rileydouglas/Downloads/Video_Games.csv")
df


# In[3]:


#finding null values 
df.isnull().sum()


# In[4]:


#deleting all null values
data = df.dropna()
print(data)


# In[5]:


#sorting the dataset according to years
sorted_data = data.sort_values(by='Year')
sorted_data


# In[6]:


sorted_data.isnull().sum()


# In[7]:


# filtering the data for the dash app
start_year = 2005
end_year = 2015

# Filter out rows with years outside the specified range
filtered_data = sorted_data[(sorted_data['Year'] >= start_year) & (sorted_data['Year'] <= end_year)]
filtered_data

# Save the filtered dataset to a CSV file
filtered_data.to_csv('filtered_dataset.csv', index=False)


# In[8]:


#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output         
import dash_bootstrap_components as dbc  


# Load the dataset
df = pd.read_csv("/Users/rileydouglas/filtered_dataset.csv")

# Initialize the Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Create the layout with multiple tabs
app.layout = html.Div([
    html.H1("Analysis of Video Game sales from 2005 to 2015"),
    dcc.Tabs(children=[
        dcc.Tab(label='Line Chart for video games by year', children=[
            html.H2('Line Chart'),

            # Dropdown for variable selection            
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
                value=df['Year'].min()  
            ),
            
            dcc.Graph(id='line-chart')
            
        ]),

        dcc.Tab(label='Scatter Plot for video games', children=[
            html.H2('Scatter Plot'),
            # Radio button
            dcc.RadioItems(
                id='scatter-plot-radio',
                options=[{'label': col, 'value': col} for col in ['Other_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales','Critic_Score']],
                value='Global_Sales'  
            ),
            # Scatter plot
            dcc.Graph(id='scatter-plot')
        ]),

        dcc.Tab(label='Interactive Charts for video games', children=[
            html.H2('Interactive Charts'),

            html.Div([
                # Chart 1
                dcc.Graph(
                    id='chart1',
                    figure=px.bar(df, x='Genre', y='Critic_Score')
                ),
                # Chart 2
                dcc.Graph(
                    id='chart2',
                    figure=px.scatter(df, x='User_Score', y='Critic_Score')
                )
            ])
        ]),
        

        dcc.Tab(label='Custom Graph for video games', children=[
            html.H2('Custom Pie Chart'),
            # Bar graph component
            dcc.Graph(
                id='custom-pie-chart',
                figure=px.pie(df, names='Genre', title='Genre Distribution for All Years')
            ),
            dcc.Graph(
                id='custom-bar-graph',
                # Update the figure to create a bar graph
                figure=px.bar(df, x='Genre', y='Critic_Score', title='Critic Score by Genre')
            )
        ])
    ]),
       
    # HTML tag for attribution
    html.Footer(
        'Created by: Riley Douglas - COHNDDS231f-001'
    )
])


# Callback for line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(year):
    filtered_df = df[df['Year'] == year]
    platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().reset_index()

    fig = {
        'data': [
            {'x': platform_sales['Platform'], 'y': platform_sales['Global_Sales'], 'type': 'line', 'name': 'Global Sales'}
        ],
        'layout': {
            'title': f'Video Game Sales by Platform for {year}',
            'xaxis': {'title': 'Platform'},
            'yaxis': {'title': 'Global Sales'}
        }
    }
    return fig

# Callback scatter plot
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    dash.dependencies.Input('scatter-plot-radio', 'value'))
def update_scatter_plot(selected_var):
    # correlation
    correlation = df[['Global_Sales', selected_var]].corr().iloc[0, 1]

    # Update the scatter plot
    fig = px.scatter(df, x='Global_Sales', y=selected_var, title=f'Correlation is {correlation:.2f} in relation to global sales')

    return fig

# Callback to update the scatter plot based on the selected bar in the bar graph
@app.callback(
    dash.dependencies.Output('chart2', 'figure'),
    dash.dependencies.Input('chart1', 'clickData'))
def update_scatter_plot_with_click(click_data):
    if click_data is None:
        # If no data is clicked, show the original scatter plot
        fig = px.scatter(df, x='Genre', y='Critic_Score', title='Critic Score and Game Genre',
                         labels={'Genre': 'Genre', 'Critic_Score': 'Critic Score'})
    else:
        # Retrieve the selected category from the clicked data
        selected_category = click_data['points'][0]['x']

        # Filter the dataset based on the selected category
        filtered_df = df[df['Genre'] == selected_category]

        # Create the updated scatter plot
        fig = px.scatter(filtered_df, x='User_Score', y='Critic_Score',
                         title=f'Critic and User score of {selected_category}',
                         labels={'User_Score': 'User Score', 'Critic_Score': 'Critic Score'})

    return fig

# Callback for updating the Custom Pie Chart
@app.callback(
    Output('custom-pie-chart', 'figure'),
    [Input('year-dropdown', 'value')]  
)
def update_custom_pie_chart(year):
    filtered_df = df[df['Year'] == year]
    genre_distribution = filtered_df['Genre'].value_counts()

    fig = px.pie(
        names=genre_distribution.index,
        values=genre_distribution.values,
        title=f'Genre Distribution for {year}'
    )
    return fig

# Callback for updating the Custom Bar Graph
@app.callback(
    Output('custom-bar-graph', 'figure'),
    [Input('year-dropdown', 'value')]  
)
def update_custom_bar_graph(year):
    filtered_df = df[df['Year'] == year]
    genre_avg_scores = filtered_df.groupby('Genre')['Critic_Score'].mean().reset_index()

    fig = px.bar(
        genre_avg_scores, x='Genre', y='Critic_Score',
        title=f'Critic Score by Genre for {year}',
        labels={'Genre': 'Genre', 'Critic_Score': 'Critic Score'}
    )
    return fig



# Run the application
if __name__ == '__main__':
    app.run_server(port=8273)


# In[ ]:




