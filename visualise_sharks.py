"""
Program to visualise shark attack data using Bokeh
"""

import pandas as pd
from read_csv_file import read_shark_file, read_world_file
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import PRGn, RdYlGn
from bokeh.transform import linear_cmap,factor_cmap
from bokeh.layouts import row, column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
import numpy as np
from bokeh.models.tools import HoverTool

# specify how to output the plot(s)
output_file("example.html")



# read csv file
sharks_df = read_file('attacks.csv')

# create ColumnDataSource from DataFrame
# source = ColumnDataSource(sharks_df)

# create list of all different activities
country_list = sharks_df.groupby('Country')
# country_list = [i for i in country_list if i != 0]
country_list.head(20)


# create a figure object
# p = figure(width=900,
#         height=600,
#         tools="pan,reset,save,box_select,zoom_in,zoom_out",
#         x_range=x_range,
#         y_range=y_range,
#         )
#



# add a circle renderer to this figure
# p.circle(x='Year',
#         y='Country',
#         source=source)
#
# # add tooltips
# # example: when hovering over this will show the activities people were doing in specific countries
# hover = HoverTool()
# hover.tooltips = """
#     <div>
#     <h3>@Country</h3>
#     <div><strong>Activity: </strong>@Activity</div>
#     </div>
# """
#
# p.add_tools(hover)



# display the figure
# show(p)
