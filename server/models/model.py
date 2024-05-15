from ext.ext import db
from datetime import datetime

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parameters = db.relationship('Parameter', backref='device', lazy=True)

class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type_ = db.Column(db.String(50), nullable=False)
    data_readings = db.relationship('DataReading', backref='parameter', lazy=True)

class DataReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameter.id'), nullable=False)
    value = db.Column(db.String(100))
    timestamp = db.Column(db.String(100), nullable=False)
