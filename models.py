from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
db = SQLAlchemy()
import base64
from werkzeug.utils import secure_filename
from io import BytesIO


class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    findings = db.relationship('Findings', backref='project', cascade='all, delete-orphan')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'findings': [finding.to_dict() for finding in self.findings]
        }
class Findings(db.Model, SerializerMixin):
    __tablename__ = 'findings'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    title = db.Column(db.String(255))
    description = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    severity_id = db.Column(db.Integer, db.ForeignKey('severity.id'))
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'status': {'id': self.status.id, 'name': self.status.name} if self.status else None,
            'severity': {'id': self.severity.id, 'name': self.severity.name} if self.severity else None
        }
    def shallow_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'status': {'id': self.status.id, 'name': self.status.name} if self.status else None,
            'severity': {'id': self.severity.id, 'name': self.severity.name} if self.severity else None
        }
class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    findings = db.relationship('Findings', backref='category')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'findings': [finding.shallow_to_dict() for finding in self.findings]
        }
    
class Status(db.Model, SerializerMixin):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    findings = db.relationship('Findings', backref='status')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'findings': [finding.shallow_to_dict() for finding in self.findings]
        }
        
class Severity(db.Model, SerializerMixin):
    __tablename__ = 'severity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    findings = db.relationship('Findings', backref='severity')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'findings': [finding.shallow_to_dict() for finding in self.findings]
        }
class Image (db.Model, SerializerMixin):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(255))
    content_type=db.Column(db.String(255))
    data=db.Column(db.LargeBinary)
    finding_id = db.Column(db.Integer, db.ForeignKey('findings.id'),nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)
    