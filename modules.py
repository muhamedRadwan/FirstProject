# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()


class User(Base, UserMixin):
    """ 
        Table For USers(Admin,Employee)
        Type Field Have This Value ADMIN , CLIENT, EMPLOYEE
    """
    __tablename__ = "user"
    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    picture = Column(String, default=u'users/default.png')
    username = Column(String, unique=True, nullable=False)
    email = Column(String(100), unique=True)
    type = Column(String(10), nullable=False)
    password_hash = Column(String, nullable=True)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Device(Base):
    """ This Table For Devices in Company"""
    __tablename__ = 'device'
    name = Column(String(100))
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer,nullable=False)


class DeviceEmployee(Base):
    """This Table Have Device and Employee That will Work on it
        The Status if False That make The device Isn't installed
         if issues True Then Go To table Issue
    """
    __tablename__ = 'device_employee'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    address = Column(String(500), nullable=False)
    status = Column(Boolean, default=False)
    phone = Column(String(20))
    client_name = Column(String(100), nullable=False)
    issues = Column(Boolean, default=False)
    addtion = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    device_id = Column(Integer, ForeignKey('device.id'))
    user = relationship(User)
    device = relationship(Device)
    message = Column(String)


class Issue(Base):
    """Table Isuues If Employee Find Any Issue For this Device"""
    __tablename__ = 'issue'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    issue = Column(String, nullable=False)
    device_employee_id = Column(Integer, ForeignKey('device_employee.id'))
    device_employee = relationship(DeviceEmployee)

engine = create_engine('sqlite:///DataStore.db')
Base.metadata.create_all(engine)
