import csv
import json


db_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/planets_backup.csv'

with open(db_path) as csv_file:
    csv_reader = csv.reader(csv_file)
    planet_coords = {row[9]: [float(row[13]), float(row[12])] for row in csv_reader if row[9]}

json.dump(planet_coords, open('planet_coords.json', 'w'))
