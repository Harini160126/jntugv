"""
Database models for PyTech Arena
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize database
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class StudentProfile(db.Model):
    """Student profile model"""
    __tablename__ = 'student_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    gpa = db.Column(db.Float, nullable=False, default=0.0)
    skills = db.Column(db.Text, nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    placement_status = db.Column(db.String(50), nullable=False, default='Not Placed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref="student_profile")
    
    def __repr__(self):
        return f'<StudentProfile {self.user_id}>'

class JobPosting(db.Model):
    """Job posting model"""
    __tablename__ = 'job_posting'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)  # Full-time, Internship, Part-time
    salary_range = db.Column(db.String(100), nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    application_process = db.Column(db.Text, nullable=True)
    visit_date = db.Column(db.DateTime, nullable=True)
    visit_time = db.Column(db.String(100), nullable=True)
    venue = db.Column(db.String(200), nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobPosting {self.title}>'

class JobApplication(db.Model):
    """Job application model"""
    __tablename__ = 'job_application'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Applied')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref="job_applications")
    job = db.relationship("JobPosting", backref="applications")
    
    def __repr__(self):
        return f'<JobApplication {self.user_id}-{self.job_id}>'

class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default="info")  # info, success, warning, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref="notifications")
    
    def __repr__(self):
        return f'<Notification {self.user_id}>'

class Company(db.Model):
    """Company model for recruiters"""
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    logo_letter = db.Column(db.String(10), default="C")
    gradient = db.Column(db.String(200), default="linear-gradient(135deg, #0033a0 0%, #00b4d8 100%)")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'

class PlacementDrive(db.Model):
    """Placement drive model"""
    __tablename__ = 'placement_drive'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlacementDrive {self.name}>'

# Association table for many-to-many relationship between drives and companies
drive_companies = db.Table('drive_companies',
    db.Column('drive_id', db.Integer, db.ForeignKey('placement_drive.id'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True)
)
