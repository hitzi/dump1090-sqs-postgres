#!/usr/bin/env python

import boto3
import psycopg2 as dbapi2
import os

# Make a DB connection
try:
    db = dbapi2.connect (host=os.getenv('DUMP1090_HOST', 'dump1090'), database=os.getenv('DUMP1090_DATABASE', 'dump1090'), user=os.getenv('DUMP1090_USER', 'dump1090'), password=os.getenv('DUMP1090_PASSWORD', 'dump1090'))
except:
    print "I am unable to connect to the database"
cur = db.cursor()

# Get the service resource
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=os.getenv('SQS_QUEUE', 'dump1090'))

while True:
    # Process messages by printing out the message body
    for message in queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=20):

        # Convert (comma separated) message into an array of values
        field = '{0}'.format(message.body).rstrip().split(',')

        # Not all valid messages have been handled. For example:
        # STA,,5,179,400AE7,10103,2008/11/28,14:58:51.153,2008/11/28,14:58:51.153,RM

        MessageType = field[0]
        TransmissionType = None if field[1] == '' else field[1]
        SessionID = None if field[2] == '' else field[2]
        AircraftID = None if field[3] == '' else field[3]
        HexIdent = None if field[4] == '' else field[4]
        FlightID = None if field[5] == '' else field[5]
        DateMessageGenerated = None if field[6] == '' else field[6]
        TimeMessageGenerated = None if field[7] == '' else field[7]
        DateMessageLogged = None if field[8] == '' else field[8]
        TimeMessageLogged = None if field[9] == '' else field[9]
        Callsign = None if field[10] == '' else field[10]
        Altitude = None if field[11] == '' else field[11]
        GroundSpeed = None if field[12] == '' else field[12]
        Track = None if field[13] == '' else field[13]
        Latitude = None if field[14] == '' else field[14]
        Longitude = None if field[15] == '' else field[15]
        VerticalRate = None if field[16] == '' else field[16]
        Squawk = None if field[17] == '' else field[17]
        Alert = None if field[18] == '' else field[18]
        Emergency = None if field[19] == '' else field[19]
        SPI = None if field[20] == '' else field[20]
        IsOnGround = None if field[21] == '' else field[21]

        # Insert the message into the database
        query = "INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (MessageType, TransmissionType, SessionID, AircraftID, HexIdent, FlightID, DateMessageGenerated, TimeMessageGenerated, DateMessageLogged, TimeMessageLogged, Callsign, Altitude, GroundSpeed, Track, Latitude, Longitude, VerticalRate, Squawk, Alert, Emergency, SPI, IsOnGround)
        cur.execute(query, data)
        db.commit()

        # Print out the body
        #print('{0}'.format(message.body))

        # Let the queue know that the message is processed by deleting
        message.delete()
