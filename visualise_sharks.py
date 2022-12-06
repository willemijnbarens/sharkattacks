"""
Program to visualise shark attack data using Bokeh
"""

from read_csv_file import read_file
from bokeh.plotting import figure, output_file, show

sharks_df = read_file('attacks.csv')


# create a figure object
p = figure(width=900, height=600, tools="pan,reset,save,box_zoom")

# add a line renderer to this figure
p.line(x=sharks_df['Year'].value_counts().sort_index(ascending=True).index, y=sharks_df['Year'].value_counts().sort_index(ascending=True))

# specify how to output the plot(s)
output_file("example.html")

# display the figure
show(p)
