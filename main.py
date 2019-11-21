# Script API Python menggunakan Flask dan flask_pymongo

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify, request

app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.config["MONGO_URI"] = "mongodb://mongo-admin:password@192.168.33.13:27017/restaurantDB?retryWrites=false&authSource=admin"
mongo = PyMongo(app)

@app.route('/restaurant', methods=['GET'])
def get_data():
    datas = mongo.db.restaurantcl.find()
    response = dumps(datas)
    return response

# Insert
@app.route('/restaurant', methods=['POST'])
def add_data():
    request_json = request.json
    data_nama = request_json["nama"]
    data_zipcode = request_json["zipCode"]
    data_neighborhood = request_json["neighborhood"]
    data_councilDistrict = request_json["councilDistrict"]
    data_policeDistrict = request_json["policeDistrict"]
    data_location = request_json["Location 1"]

    data_id = mongo.db.restaurantcl.insert({
        'nama' : data_nama,
        'zipCode' : data_zipcode,
        'neighborhood' : data_neighborhood,
        'councilDistrict' : data_councilDistrict,
        'policeDistrict' : data_policeDistrict,
        'Location 1' : data_location
    })

    response = jsonify('Data has added successfully. The id is {}'.format(data_id))
    response.status_code = 200
    return response

# Update
@app.route('/restaurant/<id>', methods=['PUT'])
def update_data(id):
    request_json = request.json
    data_id = request_json["_id"]
    data_nama = request_json["nama"]
    data_zipcode = request_json["zipCode"]
    data_neighborhood = request_json["neighborhood"]
    data_councilDistrict = request_json["councilDistrict"]
    data_policeDistrict = request_json["policeDistrict"]
    data_location = request_json["Location 1"]

    mongo.db.restaurantcl.update_one(
        {'_id': ObjectId(data_id['$oid']) if '$oid' in data_id else ObjectId(data_id)},
        {
            '$set' :
            {
                'nama' : data_nama,
                'zipCode' : data_zipcode,
                'neighborhood' : data_neighborhood,
                'councilDistrict' : data_councilDistrict,
                'policeDistrict' : data_policeDistrict,
                'Location 1' : data_location
            }
        }
    )

    response = jsonify('Data has updated successfully. The id is {}'.format(data_id))
    response.status_code = 200
    return response

# Delete
@app.route('/restaurant/<id>', methods=['DELETE'])
def delete_data(id):
    mongo.db.restaurantcl.delete_one({
        '_id': ObjectId(id)
    })
    
    response = jsonify('Data has deleted successfully. The id is {}'.format(id))
    response.status_code = 200
    return response

# Aggregation
@app.route('/restaurant/neighborhood', methods=['GET'])
def get_neighborhood():
    result = mongo.db.restaurantcl.aggregate([
        {
            "$group": {
                "_id": "$neighborhood",
                "count": {"$sum": 1}
            } 
        }
    ])

    response = dumps(result)
    return response


if __name__ == "__main__":
    app.run()