#%%
import simplekml
import pandas as pd

#%%
#CSV of populated cities obtained from: https://simplemaps.com/data/world-cities
cities_df = pd.read_csv('worldcities.csv')
cities_by_population = cities_df.sort_values(by=['population'], ascending=False)
highly_populated_cities = cities_by_population[cities_by_population.population > 2650000]
highly_populated_cities.head()

#%%
population_kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon49.png'
style.iconstyle.scale = 1.8
style.labelstyle.scale = 1.8

columns_needed = highly_populated_cities[['city','lat','lng']]
for value in columns_needed.values:
    point = population_kml.newpoint(name=value[0], coords=[(value[2],value[1])])

    point.style = style

population_kml.save('populated_cites.kml')

#%%
density_kml = simplekml.Kml()

ground = density_kml.newgroundoverlay(name='Population Density')
ground.icon.href = 'population_density_colormap.png'
ground.latlonbox.north = 90
ground.latlonbox.south = -90
ground.latlonbox.east =  180
ground.latlonbox.west =  -180

density_kml.save('population_density.kml')

#%%
camera = simplekml.Kml()
pnt = camera.newpoint()
pnt.camera.latitude = 38
pnt.camera.longitude = -99
pnt.camera.altitude = 4750000

camera.save("camera.kml")