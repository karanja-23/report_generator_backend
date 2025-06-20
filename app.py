from models import db, Findings, Category, Status, Severity, Project
from flask_migrate import Migrate
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config ['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.route('/')
def index():
    return "Welcome to the API"

@app.route('/projects', methods=['GET'])
def projects():
    projects = Project.query.all()
    return [project.to_dict() for project in projects]

@app.route('/project/<int:project_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return {'error': 'Project not found'}, 404
    if request.method == 'GET':
        return project.to_dict()
    elif request.method == 'POST':
        data = request.get_json()
        project.name = data['name']
        project.description = data['description']
        db.session.commit()
        return {'message': 'Project created successfully'}, 200
    elif request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'created_at' in data:
            project.created_at = data['created_at']
        if 'updated_at' in data:
            project.updated_at = data['updated_at']
        db.session.commit()
        return {'message': 'Project updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}, 200
    

if __name__ == '__main__':
    app.run(debug=True,port=6060)