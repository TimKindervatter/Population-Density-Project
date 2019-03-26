#%%
import simplekml
import pandas as pd

#%%
#CSV of populated cities obtained from: https://simplemaps.com/data/world-cities
cities_df = pd.read_csv('worldcities.csv')
cities_by_population = cities_df.sort_values(by=['population'], ascending=False)
highly_populated_cities = cities_by_population[cities_by_population.population > 500000]
highly_populated_cities.head()

#%%
population_kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon49.png'

columns_needed = highly_populated_cities[['city','lat','lng']]
for value in columns_needed.values:
    point = population_kml.newpoint(name=value[0], coords=[(value[2],value[1])])

    point.style = style

population_kml.save('populated_cites.kml')

#%%
density_kml = simplekml.Kml()

ground = density_kml.newgroundoverlay(name='Population Density')
ground.icon.href = 'population_density.png'

density_kml.save('population_density.kml')