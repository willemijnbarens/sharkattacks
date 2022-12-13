"""
Program to visualise shark attack data in a world map using Folium
"""

import pandas as pd
from read_csv_file import read_shark_file, read_world_file
import folium
import webbrowser
import math

# read csv file with location coordinates
sharks_df = read_world_file('worldcities.csv')

# delete cases without coordinates
sharks_df = sharks_df.drop(sharks_df[sharks_df.lat == 0.0].index)

# calculate on what coordinates to open the map
middle = [sharks_df['lat'].mean(), sharks_df['lng'].mean()]
m = folium.Map(location=middle, zoom_start=4)

for _, row in sharks_df.iterrows():
    # add list of activities to the popups
    popup = sharks_df.loc[(sharks_df['lat'] == row['lat']) & (sharks_df['lng'] == row['lng']), 'Activity']
    popup = popup.tolist()

    # set variable for amount of shark attacks in total per area
    number_of_shark_attacks = len(popup)

    # remove duplicates
    popup = list(dict.fromkeys(popup))
    # create string from list
    text = ', '.join(str(v) for v in popup)
    # convert string to html
    popContent = folium.Html(text, script=True)

    # set area variable based on available location information
    if row['Area'] != 0:
        area = row['Area']
    else:
        area = row['Country']

    # set variable for fatalities
    fatalities = row['fatalities']

    folium.CircleMarker(
        location=[row['lat'], row['lng']],

        # make the circles bigger according to the number of shark attacks per area
        radius= math.sqrt(number_of_shark_attacks + 10),

        # set tooltips and popups with relevant information
        tooltip=f'<b>{area}</b><br><br>Number of fatal shark attacks: {fatalities}',
        popup = folium.Popup(popContent,
                         min_width=500,
                         max_width=500),

        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)

#Display the map
m.save("map.html")
webbrowser.open("map.html")
