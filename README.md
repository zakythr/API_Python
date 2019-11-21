# API_Python

Aplikasi CRUD yang diimplementasikan pada MongoDB Cluster adalah aplikasi API (Application Programming Interface) menggunakan bahasa pemograman Python.

![](https://www.tertiarycourses.com.sg/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/p/y/python-flask-web-development-essential-training.jpg)

Flask adalah framework web untuk Python, yang menyediakan fungsionalitas untuk membangun aplikasi web, termasuk mengelola request HTTP dan merender template. Implementasi kali ini akan menggunakan Flask untuk membuat API menggunakan bahasa pemrograman Python.

API yang dibuat berisi beberapa operasi dasar seperti :

- Read
- Create
- Update
- Delete
- Agregasi (count dan sum)

Dan pengujian API menggunakan aplikasi POSTMAN

<h4>Connect Database</h4>

- Langkah Pertama, connect ke dalam database MongoDB.

```
app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.config["MONGO_URI"] = "mongodb://mongo-admin:password@192.168.33.13:27017/restaurantDB?retryWrites=false&authSource=admin"
```

<h4>Operasi READ</h4>

```
@app.route('/restaurant', methods=['GET'])
def get_data():
    datas = mongo.db.restaurantcl.find()
    response = dumps(datas)
    return response
```
Digunakan untuk menampilkan semua data, dengan menggunakan metode **GET** dan *endpoint* ```/restaurant```.

![](Postman/Postman1.PNG)

<h4>Operasi INSERT/CREATE</h4>

```
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
 ```
 Endpoint yang digunakan ```/restaurant``` dan metode yang digunakan adalah **POST**. Data yang dikirimkan berupa data JSON.
 
 ![](Postman/PostmanInsert.PNG)
 
 <h4>Operasi UPDATE</h4>
 
 ```
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
 ```
 Operasi update untuk memperbarui satu data dengan parameter berupa ObjectId. Data yang dikirim berupa **JSON** dengan atribut dan value baru yang mau di-update. Dengan *endpoint* ```/restaurant/<id>``` dan parameter berupa ObjectId, metode yang digunakan **PUT**.
 
 ![](Postman/PostmanUpdate.PNG)
 ![](Postman/PostmanUpdate1.PNG)
 ![](Postman/PostmanUpdate2.PNG)
 
<h4>Operasi DELETE</h4>

```
# Delete
@app.route('/restaurant/<id>', methods=['DELETE'])
def delete_data(id):
    mongo.db.restaurantcl.delete_one({
        '_id': ObjectId(id)
    })
    
    response = jsonify('Data has deleted successfully. The id is {}'.format(id))
    response.status_code = 200
    return response
```

Operasi delete untuk menghapus data berdasarkan ObjectId. Dengan *endpoint* ```/restaurant/<id>``` parameternya berupa ObjectId dan metode yang digunakan adalah **DELETE**.

![](Postman/PostmanDelete.PNG)

<h4>Operasi Agregasi</h4>

```
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
```

Operasi agregrasi yang melibatkan dua operasi yaitu group dan sum. Tujuanany untuk menghitung berapa banyak data berdasarkan neighborhood, Dengan menggunakan *endpoint* ```/restaurant/neighborhood```.

 ![](Postman/PostmanAgregasi.PNG)
