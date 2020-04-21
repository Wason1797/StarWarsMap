# StarWarsMap

This is the repo where we build a map of the Star Wars Galaxy using neo4j

In the first steps of the project we are foccusing on designing a graph structure that connects all available planets in the galaxy. Taking into account known hyperspace routes, grids and sectors.

We are using this [map](http://www.swgalaxymap.com/search/) for reference.

After we complete the graph generation process we can store this data on neo4j with the same structure.

Ideally we can also build a web application to show the map. Where also you will be able to plot a route between two planets and traverse the galaxy far far away.

## Avilable data used for this map

The information for this map is contained on this json files:

- /data/grid_db.json
- /data/hyperlanes_db.json
- /data/regions_db.json

You can also find a csv file taken from [This Dataset](https://hbernberg.carto.com/tables/planets/public) which belongs to the author of the map mentioned above.
To generate the json files you can also use the script provided in /scripts/data_transformation/generate_json.py


## To Run the current version of the map

You need to install [Python 3.7.X](https://www.python.org/downloads/)

Install virtualenv if you prefer: `pip install virtualenv`

Create a new virtualenv with `virtualenv venv`

Activate the virtualenv with `/venv/Scripts/activate` in Windows or `source /venv/bin/activate` on unix based systems

Install the requierements with `pip install -r requirements.txt`

Run the plot with `python -m scripts.graph.transform_db_to_graph`

A figure will be displayed showing the current state of the map.