import plotly.express as px
import json

'''
pedestrians = [
{
    "machine": "T2ME55 Copacabana Base 20",
    "latitude": "-22.91358000",
    "longitude": "-43.16705000",
    "total": 212
},
{
    "machine": "T2ME55 Copacabana Base 02",
    "latitude": "-22.96269989",
    "longitude": "-43.16669846",
    "total": 176
},
{
    "machine": "T2ME55 Copacabana Base 04",
    "latitude": "-22.96380043",
    "longitude": "-43.16979980",
    "total": 74
},
{
    "machine": "T2ME55 Copacabana Base 06",
    "latitude": "-22.96479988",
    "longitude": "-43.17210007",
    "total": 80
}
]

print(type(pedestrians))
print(type(pedestrians[0]))

print(pedestrians[0])
'''


def heatMap5():
   
    fig = px.scatter_mapbox(

        type="scattermapbox",
        hoverinfo= "text",

        #us_cities, 
        lat="lat", 
        lon="lon", 
        hover_name="City", 
        hover_data=["State", "Population"],
        color_discrete_sequence=["fuchsia"], 
        
        height=300
        )
    
    fig.update_layout(
        mapbox=dict(
            #center: { lat: center.latitude, lon: center.longitude }, 
            center=dict(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=3,
            style='open-street-map'
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
        )
   
    fig.update_geos(
        fitbounds='locations', 
        visible= True, 
        showland= True)
    fig.show()

