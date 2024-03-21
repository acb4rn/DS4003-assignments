# %% [markdown]
# ### Assignment #5: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:         
# 
# A dropdown menu that allows the user to select `country`      
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# 
# A slider that allows the user to select `year`       
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset    
# 
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A5_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
#importing dependencies
import pandas as pd 
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output

# %%
#load dataset 
gap = pd.read_csv('gdp_pcap.csv')
gap.head()

# %%
#melting data to add a year column and gdp column
gap_long = gap.melt(id_vars = 'country', 
                    var_name= 'year', 
                    value_name= 'gdp')
gap_long.head()

# %%
gap_long['year'] #checking the datatype of year

# %%
gap_long['year'] = gap_long['year'].astype('int') #type casting to integer

# %%
gap_long['year'].describe() #checking the conversion worked

# %%
#creating a function to convert the string gdp data to a float in the same units
def str_conversion(input_str):  
    input_str = str(input_str)
    if input_str[-1] == 'k': #identifying the values that need to be transformed
        input_str = input_str[:-1] #removing the 'k' 
        input_str = float(input_str) *1000 #multiplying by 1000 to make all values in the same unit
    return input_str

gap_long['gdp'] = gap_long['gdp'].apply(str_conversion).apply(float) #applying function to the whole column and transforming into a float

gap_long['gdp'] #double checking that the function and float applied correctly 

# %%
#loading the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server = app.server

# %%
#generating the app
app.layout = html.Div([
    html.H1("GDP Per Capita By Country"), #adding a header
    html.Div(children = "The Gapminder dataset compiles GDP per capita data for countries around the world from 1800 to 2100. Gapminder uses data from the World Bank between 1990 and 2016 and uses estimates from economic history reasearchers. Furthermore, for the years after 2022 Gapminder forecasts data based on the current economic growth of countries. This app displays the gapminder data no a graph and contains a dropdown and slider that are not connected to the graph."),
    html.Br(), #adding a line break to separate components
    html.Div(dcc.Dropdown(
        id = "country-dropdown", #creating dropdown
        multi = True, 
        options = [{ 'label': country, 'value': country} for country in gap_long['country'].unique()], #options are from the gap dataset
        value = [], #setting the default to an empty list because .isin() only works for lists 
        placeholder = "Select a Country" #using a placeholder instead of a default value
    ), className = "five columns"), #maximum number of columns to fit both slider and dropdown 
    html.Div(dcc.RangeSlider(
        id = "range-slider", #creating slider
        min = gap_long['year'].min(axis = 0), #minimum year
        max = gap_long['year'].max(axis = 0), # maximum year 
        value = [1924,2024], #setting default to a 100 year period ending in the current year
        marks={1800: {'label':'1800'}, 1900: {'label':'1900'}, 2000: {'label':'2000'}, 2100: {'label':'2100'}}, #adding marks by every 100 years
    tooltip={"placement": "bottom", "always_visible": True} #tooltip so the user can see the numbers of the slider
    ), className = "five columns"), 
    html.Br(),
    html.Br(), #adding space between the slider/dropdown and the graph
    html.Div(dcc.Graph( id = 'gdp-scatter'
    ), className = 'twelve columns')
], className = 'row')

#creating the callback for the interactive components
@app.callback(
    Output('gdp-scatter', 'figure'),  #output is the interactive scatter plot
    Input('country-dropdown', 'value'), #first input is the dropdown 
    Input('range-slider', 'value')) #second input is the range slider
def update_graph(countries, selected_years): #creating the function for the new dataframe based on the inputs
    df = gap_long[gap_long["country"].isin(countries)] #using .isin() to filter through the selected countries and extract from the melted df
    df = df.loc[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])] #filtering the above df by the two values from the range slider

    fig = px.line(df, x = 'year', y = 'gdp', color = 'country', title = 'GDP Per Capita') #creating the graph based on the inputs
    fig.update_layout(xaxis_title = 'Year', yaxis_title = "GDP Per Capita (USD)") #adding axis titles

    return fig

# run the app using the jupyter_mode="tab" parameter and debug=True
if __name__ == '__main__':
    app.run_server(jupyter_mode='tab', debug=True)


