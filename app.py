from models import db, Findings, Category, Status, Severity, Project, Image, Users,Roles,Permissions
from flask_migrate import Migrate
from flask import Flask, request, jsonify, url_for, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import os
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.utils import secure_filename
from io import BytesIO

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
    
    
@app.route('/findings', methods=['GET', 'POST'])
def findings():
    if request.method == 'GET':
        findings = Findings.query.all()
        return [finding.shallow_to_dict() for finding in findings]
    elif request.method == 'POST':
        data = request.get_json()
        finding = Findings(title=data['title'], description=data['description'], project_id=data['project_id'], category_id=data['category_id'], severity_id=data['severity_id'])
        db.session.add(finding)
        db.session.commit()
        return {'message': 'Finding created successfully'}, 201

@app.route('/finding/<int:finding_id>', methods=['GET', 'PUT', 'DELETE'])
def finding(finding_id):    
    finding = Findings.query.get(finding_id)
    if not finding:
        return {'error': 'Finding not found'}, 404
    if request.method == 'GET':
        return finding.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        finding.title = data['title']
        finding.description = data['description']
        finding.project_id = data['project_id']
        finding.category_id = data['category_id']
        finding.severity_id = data['severity_id']
        finding.updated_at = datetime.now()
        db.session.commit()
        return {'message': 'Finding updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(finding)
        db.session.commit()
        return {'message': 'Finding deleted successfully'}, 200
    
@app.route('/delete/all/findings', methods=['DELETE'])
def delete_all_findings():
    Findings.query.delete()
    db.session.commit()
    return {'message': 'All findings deleted successfully'}, 200

@app.route('/api/uploadFile', methods=['POST'])
def upload_file():
    file = request.files.get('image')
    if not file:
        return jsonify({'success': 0, 'message': 'No file uploaded'}), 400

    filename = secure_filename(file.filename)
    content_type = file.content_type
    data = file.read()

    image = Image(
        filename=filename,
        content_type=content_type,
        data=data
    )
    db.session.add(image)
    db.session.commit()

    image_url = url_for('get_image', image_id=image.id, _external=True)

    return jsonify({
        'success': 1,
        'file': {
            'url': image_url
        }
    }), 200
    
@app.route('/api/image/<int:image_id>')
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(BytesIO(image.data), mimetype=image.content_type)

@app.route('/api/deleteImage/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'success': 1}), 200

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = Users.query.all()
        return [user.to_dict() for user in users]
    elif request.method == 'POST':
        data = request.get_json()
        user = Users(name=data['name'], email=data['email'], password=data['password'], role_id=data['role_id'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    if request.method == 'GET':
        return user.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']
        user.role_id = data['role_id']
        user.updated_at = datetime.now()
        db.session.commit()
        return {'message': 'User updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    
@app.route('/roles', methods=['GET', 'POST'])
def roles():
    if request.method == 'GET':
        roles = Roles.query.all()
        return [role.to_dict() for role in roles]
    elif request.method == 'POST':
        data = request.get_json()
        role = Roles(name=data['name'])
        db.session.add(role)
        db.session.commit()
        return {'message': 'Role created successfully'}, 201
    
@app.route('/role/<int:role_id>', methods=['GET', 'PUT', 'DELETE'])
def role(role_id):
    role = Roles.query.get(role_id)
    if not role:
        return {'error': 'Role not found'}, 404
    if request.method == 'GET':
        return role.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        role.name = data['name']
        db.session.commit()
        return {'message': 'Role updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(role)
        db.session.commit()
        return {'message': 'Role deleted successfully'}, 200
    
@app.route('/permissions', methods=['GET', 'POST'])
def permissions():
    if request.method == 'GET':
        permissions = Permissions.query.all()
        return [permission.to_dict() for permission in permissions]
    elif request.method == 'POST':
        data = request.get_json()
        permission = Permissions(name=data['name'])
        db.session.add(permission)
        db.session.commit()
        return {'message': 'Permission created successfully'}, 201
    
@app.route('/permission/<int:permission_id>', methods=['GET', 'PUT', 'DELETE'])
def permission(permission_id):
    permission = Permissions.query.get(permission_id)
    if not permission:
        return {'error': 'Permission not found'}, 404
    if request.method == 'GET':
        return permission.to_dict()
    elif request.method == 'PUT':
        data = request.get_json()
        permission.name = data['name']
        db.session.commit()
        return {'message': 'Permission updated successfully'}, 200
    elif request.method == 'DELETE':
        db.session.delete(permission)
        db.session.commit()
        return {'message': 'Permission deleted successfully'}, 200
    
@app.route('/roles/<int:role_id>/permissions', methods=['GET', 'POST'])
def role_permissions(role_id):
    role = Roles.query.get(role_id)
    if not role:
        return {'error': 'Role not found'}, 404

    if request.method == 'GET':
        return [permission.to_dict() for permission in role.permissions]

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'permission_id' not in data:
            return {'error': 'permission_id is required'}, 400

        permission = Permissions.query.get(data['permission_id'])
        if not permission:
            return {'error': 'Permission not found'}, 404

        if permission in role.permissions:
            return {'message': 'Permission already assigned to role'}, 200

        role.permissions.append(permission)
        db.session.commit()
        return {'message': 'Permission added to role successfully'}, 201
if __name__ == '__main__':
    app.run(debug=True,port=6060)