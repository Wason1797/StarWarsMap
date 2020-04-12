import csv
import json

db_path = 'D:/wason/Documents/Trabajos Universidad/Proyectos y Soluciones/StarWarsMap/data/Star Wars Galaxy Map Grid Coordinates - planets.csv'

database = {
    'regions': {
    }
}

with open(db_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        region_name = row[3] if row[3] else "Unidentified Region"
        sector_name = row[2] if row[2] else f"Unidentified Sector {region_name}"
        if row[3] not in database['regions']:
            database['regions'][region_name] = {
                'sectors': {
                    sector_name: {
                        'grids': {
                            row[1]: {
                                'planets': [
                                    row[0]
                                ]
                            }
                        }
                    }
                }
            }
        elif row[2] not in database['regions'][row[3]]['sectors']:
            database['regions'][row[3]]['sectors'][sector_name] = {
                'grids': {
                    row[1]: {
                        'planets': [
                            row[0]
                        ]
                    }
                }
            }
        elif row[1] not in database['regions'][row[3]]['sectors'][row[2]]['grids']:
            database['regions'][row[3]]['sectors'][row[2]]['grids'][row[1]] = {
                'planets': [
                    row[0]
                ]
            }
        else:
            database['regions'][row[3]]['sectors'][row[2]]['grids'][row[1]]['planets'].append(row[0])

json.dump(database, open('formatted_planet_db.json', 'w'))
