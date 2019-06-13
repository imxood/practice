from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app)

class Upload(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        print(args)
        file = args['file']
        return "hello.7z", 201

api.add_resource(Upload, '/upload')

if __name__ == "__main__":
    app.run(debug=True)

