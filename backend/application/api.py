from flask import jsonify, request, send_file
from flask_restful import Resource, fields, marshal_with, reqparse
import sys
from application.models import *
from application.database import db
from application.workers import sendEmail
from datetime import datetime, timedelta
import heapq


def findAllCities():
    cities = set()
    roads = db.session.query(SourceToDestination).all()
    roadsLength = len(roads)

    for i in range(0, roadsLength):
        city1 = roads[i].source
        city2 = roads[i].destination
        cities.add(city1)
        cities.add(city2)

    return list(cities)


class CitiesAPI(Resource):
    def get(self):
        cities = findAllCities()
        cities.sort()

        return cities, 200


INF = sys.maxsize
V = len(findAllCities())

def calculateTime(source, destination):
    pq = []
    heapq.heappush(pq, (0, source))

    time = [INF] * V
    time[ord(source) - 65] = 0

    while pq:
        currentTime, currentCity = heapq.heappop(pq)

        if currentCity == destination:
            break

        availableRoads = (
            db.session.query(SourceToDestination)
            .filter(
                (SourceToDestination.source == currentCity)
                | (SourceToDestination.destination == currentCity)
            )
            .all()
        )

        for i in range(0, len(availableRoads)):
            currentRoad = availableRoads[i]
            nextCity = (
                currentRoad.destination
                if currentRoad.source == currentCity
                else currentRoad.source
            )

            if (
                time[ord(nextCity) - 65]
                > time[ord(currentCity) - 65] + currentRoad.time
            ):
                time[ord(nextCity) - 65] = (
                    time[ord(currentCity) - 65] + currentRoad.time
                )
                heapq.heappush(pq, (time[ord(nextCity) - 65], nextCity))

    return time[ord(destination) - 65]


tripTimeParser = reqparse.RequestParser()
tripTimeParser.add_argument("source")
tripTimeParser.add_argument("destination")


class TripTimeAPI(Resource):
    def post(self, cabName=None):
        args = tripTimeParser.parse_args()
        source = args.get("source", None)
        destination = args.get("destination", None)

        time = calculateTime(source, destination)
        print(time)
        return {"time": time}, 200


def updateAvailability():
    now = datetime.now()
    currentTime = now.strftime("%d/%m/%Y, %H:%M")

    # First We will clear all the boookings which have been completed and update availability
    completedBookings = (
        db.session.query(Bookings).filter(Bookings.bookedTill <= currentTime).all()
    )

    for i in range(0, len(completedBookings)):
        currentCab = (
            db.session.query(Cabs)
            .filter(Cabs.cabId == completedBookings[i].cabId)
            .first()
        )
        currentCab.available = True
        # db.session.delete(completedBookings[i])

    db.session.commit()


def findAvailableCabs():
    updateAvailability()

    # Now we will return all the available cabs
    availableCabs = db.session.query(Cabs).filter(Cabs.available == True).all()
    return availableCabs


def addBooking(cab, userEmail, source, destination, tripTime=0):
    cab.available = False

    bookedTill = datetime.now() + timedelta(minutes=tripTime)
    bookedTill = bookedTill.strftime("%d/%m/%Y, %H:%M")

    newBooking = Bookings(
        cabId=cab.cabId,
        userEmail=userEmail,
        source=source,
        destination=destination,
        bookedTill=bookedTill,
    )
    db.session.add(newBooking)
    db.session.commit()


addBookingParser = reqparse.RequestParser()
addBookingParser.add_argument("cabId")
addBookingParser.add_argument("userEmail")
addBookingParser.add_argument("tripTime")
addBookingParser.add_argument("source")
addBookingParser.add_argument("destination")


class AddBookingsAPI(Resource):
    def post(self):
        args = addBookingParser.parse_args()
        cabId = args.get("cabId", None)
        userEmail = args.get("userEmail", None)
        source = args.get("source", None)
        destination = args.get("destination", None)
        tripTime = args.get("tripTime", None)
        tripTime = int(tripTime)

        user = (
            db.session.query(Bookings).filter(Bookings.userEmail == userEmail).first()
        )
        if user:
            return {}, 400

        cab = db.session.query(Cabs).filter(Cabs.cabId == cabId).first()
        tripPrice = cab.pricePerMinute * tripTime
        addBooking(cab, userEmail, source, destination, tripTime)

        try:
            sendEmail(userEmail, "Your cab is booked.", tripTime, tripPrice)
        except Exception as e:
            print("Mail not sent.")
        return {}, 200


cabFields = {
    "cabId": fields.Integer,
    "cabName": fields.String,
    "pricePerMinute": fields.Integer,
    "available": fields.Boolean,
}


addCabParser = reqparse.RequestParser()
addCabParser.add_argument("cabName")
addCabParser.add_argument("pricePerMinute")

editCabParser = reqparse.RequestParser()
editCabParser.add_argument("cabId")
editCabParser.add_argument("cabName")
editCabParser.add_argument("pricePerMinute")


class CabDetailsAPI(Resource):
    @marshal_with(cabFields)
    def get(self, cabId=None):
        if cabId is None:
            updateAvailability()
            cabs = db.session.query(Cabs).all()
            return cabs, 200

        cab = db.session.query(Cabs).filter(Cabs.cabId == cabId).first()
        return cab, 200

    @marshal_with(cabFields)
    def put(self, cabId):
        args = editCabParser.parse_args()
        cabName = args.get("cabName", None)
        pricePerMinute = args.get("pricePerMinute", None)

        cab = db.session.query(Cabs).filter(Cabs.cabId == cabId).first()
        if cabName is not None:
            cab.cabName = cabName
        if pricePerMinute is not None:
            cab.pricePerMinute = pricePerMinute

        db.session.commit()
        return cab, 201

    @marshal_with(cabFields)
    def post(self):
        args = addCabParser.parse_args()
        cabName = args.get("cabName", None)
        pricePerMinute = args.get("pricePerMinute", None)

        if cabName is None:
            return {"message": "Please provide a name for this cab."}, 400

        if pricePerMinute is None:
            return {"message": "Please provide a price per minute for this cab."}, 400

        newCab = Cabs(cabName=cabName, pricePerMinute=pricePerMinute, available=True)

        db.session.add(newCab)
        db.session.commit()
        return newCab, 201

    @marshal_with(cabFields)
    def delete(self, cabId):
        cab = db.session.query(Cabs).filter(Cabs.cabId == cabId).first()
        db.session.delete(cab)
        db.session.commit()
        return cab, 200


class AvailableCabsAPI(Resource):
    def get(self):
        updateAvailability()

        cabs = db.session.query(Cabs).filter(Cabs.available == True).all()

        if len(cabs) == 0:
            return {
                "message": "No cab is available right now. Please try again in some time."
            }, 400
        else:
            return marshallCabs(cabs)


@marshal_with(cabFields)
def marshallCabs(cabs):
    return cabs
