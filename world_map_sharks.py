"""
Program to visualise shark attack data in a world map using Folium
"""

import pandas as pd
from read_csv_file import read_shark_file, read_world_file
import folium
import webbrowser
import math
from collections import Counter

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

    # create list with the 6 most common activities
    c = Counter(popup)
    top5 = c.most_common(6)
    # only keep first element of tuples and remove missing data
    top5 = [x[0] for x in top5 if x[0] != 0]

    # check if 5 activities were found
    while len(top5) < 5:
        top5.append('No data')

    # create html with the top 5 activities
    popContent = f"""
        <h2>Most common activities</h2>
        <ol>
            <li>{top5[0]}</li>
            <li>{top5[1]}</li>
            <li>{top5[2]}</li>
            <li>{top5[3]}</li>
            <li>{top5[4]}</li>
        </ol>
        """

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
