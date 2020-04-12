import csv
import json

db_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/planets.csv'


csv_file = csv.reader(open(db_path), delimiter=',')

db = dict()
grid_db = dict()

for row in csv_file:
    region_name = row[10] if row[10] else "Uncharted Region"
    sector_name = row[1] if row[1] else f"Uncharted Sector In {region_name}"
    grid_name = row[6]
    planet_name = row[3]
    planet_coords = [float(coord) for coord in row[7:9]]
    planet_map = [{'name': planet_name, 'coords': planet_coords}]
    data = {
        sector_name: planet_map
    }
    if region_name not in db:
        db[region_name] = data
    elif sector_name not in db[region_name]:
        db[region_name].update(data)
    else:
        db[region_name][sector_name].extend(data[sector_name])

    if grid_name not in grid_db:
        grid_db[grid_name] = planet_map
    else:
        grid_db[grid_name].extend(planet_map)

json.dump(db, open('regions_db.json', 'w'))
json.dump(grid_db, open('grid_db.json', 'w'))
