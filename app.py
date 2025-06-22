from models import db, Findings, Category, Status, Severity, Project
from flask_migrate import Migrate
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
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

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        projects = Project.query.all()
        return [project.to_dict() for project in projects]
    elif request.method == 'POST':
        data = request.get_json()
        project = Project(name=data['name'], description=data['description'],created_at=data['created_at'])
        db.session.add(project)
        db.session.commit()
        return {'message': 'Project created successfully'}, 201

@app.route('/project/<int:project_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return {'error': 'Project not found'}, 404
    if request.method == 'GET':
        return project.to_dict()
    
    elif request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
                
        project.updated_at = datetime.now()
        db.session.commit()
        return {'message': 'Project updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}, 200
    
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        categories = Category.query.all()
        return [category.to_dict() for category in categories]
    elif request.method == 'POST':
        data = request.get_json()
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return {'message': 'Category created successfully'}, 201
@app.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return {'error': 'Category not found'}, 404
    if request.method == 'GET':
        return category.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        category.name = data['name']
        category.updated_at = datetime.now()
        db.session.commit()
        return {'message': 'Category updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}, 200


@app.route('/severities', methods=['GET', 'POST'])
def severities():
    if request.method == 'GET':
        severities = Severity.query.all()
        return [severity.to_dict() for severity in severities]
    elif request.method == 'POST':
        data = request.get_json()
        severity = Severity(name=data['name'])
        db.session.add(severity)
        db.session.commit()
        return {'message': 'Severity created successfully'}, 201

@app.route('/severity/<int:severity_id>', methods=['GET', 'PUT', 'DELETE'])
def severity(severity_id):
    severity = Severity.query.get(severity_id)
    if not severity:
        return {'error': 'Severity not found'}, 404
    if request.method == 'GET':
        return severity.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        severity.name = data['name']
        severity.updated_at = datetime.now()
        db.session.commit()
        return {'message': 'Severity updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(severity)
        db.session.commit()
        return {'message': 'Severity deleted successfully'}, 200
    
if __name__ == '__main__':
    app.run(debug=True,port=6060)