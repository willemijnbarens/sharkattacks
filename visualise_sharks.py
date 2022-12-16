"""
Program to visualise shark attack data over the years using Bokeh
"""

import pandas as pd
import numpy as np
from read_csv_file import read_shark_file, read_world_file
from sklearn.linear_model import LinearRegression
from bokeh.io import curdoc
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row
from bokeh.models.tools import HoverTool

model = LinearRegression()

# save plot in html file
output_file("attacks_over_time.html")

# function to fit data
def fitting(df, x, y, new_column):
    years = df[x].to_numpy()
    attacks = df[y].to_numpy()
    years = years.reshape(-1, 1)
    attacks = attacks.reshape(-1, 1)

    model.fit(years, attacks)
    fitted = model.predict(years)

    # add column
    df[new_column] = fitted

    return df

# read csv file
sharks_df = read_shark_file('attacks.csv')

# count the amount of shark attacks and fatalities per year
count = sharks_df.groupby(['Year'])['Year'].count()
fatalities = sharks_df.groupby(['Year'])['Fatal'].apply(lambda x: (x=='y').sum())

# merge the 2 new pandas series together
grouped = pd.concat([count,fatalities],axis=1)
grouped = grouped.rename(columns={'Year': 'Count'})
# drop data with missing year value
grouped = grouped.drop(0)

# add column with percentage of fatalities in relation to number of attacks
grouped['Fatalities_percentage'] = ((grouped['Fatal'] / grouped['Count']) * 100).round(2)
# add years as column instead of index
grouped = grouped.reset_index()


# add fitted data to the DataFrame to show the linear regression
grouped = fitting(grouped, 'Year', 'Count', 'Fitted_attacks')
grouped = fitting(grouped, 'Year', 'Fatal', 'Fitted_fatalities')

print(grouped)

# create first figure
p1 = figure(title="Shark Attacks per Year", x_axis_label='year', y_axis_label='occurences',
    x_range=(1800, 2020), y_range=(-10, 150), width=1000,
    tools= ['zoom_in', 'zoom_out', 'pan', 'reset', 'hover'])

# add lines to first figure
p1.line(grouped['Year'], grouped['Count'], legend_label="Attacks", color="blue", line_width=2)
p1.line(grouped['Year'], grouped['Fatal'], legend_label="Fatalities", color="red", line_width=2)

# add fitted lines to first figure
p1.line(grouped['Year'], grouped['Fitted_attacks'],
    legend_label="Linear regression attacks", color="lightblue", line_width=2)
p1.line(grouped['Year'], grouped['Fitted_fatalities'],
    legend_label="Linear regression fatalities", color="lightcoral", line_width=2)

# create second figure
p2 = figure(title= 'Percentage of Fatal Shark Attacks per Year', x_axis_label='year',
    y_axis_label='Percentage', x_range=(1800, 2020), y_range=(0, 100), width=1000,
    tools= ['zoom_in', 'zoom_out', 'pan', 'reset', 'hover'])

# add lines to second figure
p2.line(grouped['Year'], grouped['Fatalities_percentage'],
    legend_label="Percentage of Fatal Attacks", color="blue", line_width=2)


# set legend in the top left corner
p1.legend.location = "top_left"
# set theme
curdoc().theme = "night_sky"

# display figure and fit to screen
show(row(children=[p1, p2], sizing_mode="scale_width"))
