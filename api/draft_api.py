from itertools import chain
from flask_cors import CORS
from flask import Flask, jsonify
from scripts.graph.transform_db_to_graph import get_region_db


app = Flask(__name__)
CORS(app)


@app.route('/planets', methods=['GET'])
def get_planets():
    region_path = './data/regions_db.json'
    regions = get_region_db(region_path)
    return jsonify([planet.to_dict() for planet in
                    chain.from_iterable(region.planets for region in regions)])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
