import csv

csv_planets = csv.reader(open('data/Star Wars Galaxy Map Grid Coordinates - planets.csv'), delimiter=',')
csv_coords = csv.reader(open('data/planets_backup.csv'), delimiter=',')

coord_file = sorted(row[9] for row in csv_coords)
db_file = sorted(row[0] for row in csv_planets)

with open('compare.csv', 'w') as compare_file:
    compare_file.writelines([f'{name1},{name2}\n' for name1, name2 in zip(db_file, coord_file)])
