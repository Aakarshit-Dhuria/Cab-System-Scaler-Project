from .database import db


class SourceToDestination(db.Model):
    __tablename__ = "sourceToDestination"

    source = db.Column(db.String, primary_key=True, nullable=False)
    destination = db.Column(db.String, primary_key=True, nullable=False)
    time = db.Column(db.Integer, nullable=False)


class Cabs(db.Model):
    __tablename__ = "cabs"
    
    cabId = db.Column(db.Integer, primary_key=True, nullable=False)
    cabName = db.Column(db.String, nullable=False)
    pricePerMinute = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)
    bookings = db.relationship("Bookings", backref="cabs")


class Bookings(db.Model):
    __tablename__ = "bookings"

    cabId = db.Column(db.Integer, db.ForeignKey("cabs.cabId"), primary_key=True)
    userEmail = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    bookedTill = db.Column(db.String, nullable=False)
