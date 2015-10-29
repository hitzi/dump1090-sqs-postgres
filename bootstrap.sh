#!/bin/bash

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt-get update
sudo apt-get install wget ca-certificates -y

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update

sudo apt-get install postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4 libpq-dev -y

# Create user, database, and table within database
# psql CREATE ROLE dump1090 WITH LOGIN PASSWORD 'dump1090';
# psql CREATE DATABASE dump1090 OWNER dump1090 TEMPLATE template0;

# CREATE TABLE messages (
#     MessageType varchar(3),
#     TransmissionType smallint,
#     SessionID smallint,
#     AircraftID smallint,
#     HexIdent varchar(6),
#     FlightID integer,
#     DateMessageGenerated varchar(10),
#     TimeMessageGenerated varchar(12),
#     DateMessageLogged varchar(10),
#     TimeMessageLogged varchar(12),
#     Callsign varchar(8),
#     Altitude integer,
#     GroundSpeed numeric(5, 1),
#     Track varchar(8),
#     Latitude numeric(8, 5),
#     Longitude numeric(8, 5),
#     VerticalRate varchar(8),
#     Squawk varchar(8),
#     Alert varchar(8),
#     Emergency varchar(8),
#     SPI varchar(8),
#     IsOnGround smallint
# );

# Example INSERT statement:
# INSERT INTO messages (MessageType, TransmissionType, SessionID, AircraftID, HexIdent, FlightID, DateMessageGenerated, TimeMessageGenerated, DateMessageLogged, TimeMessageLogged, Callsign, Altitude, GroundSpeed, Track, Latitude, Longitude, VerticalRate, Squawk, Alert, Emergency, SPI, IsOnGround) VALUES ('MSG', 4, 111, 11111, 'A9520E', 111111, '2015/09/27', '15:22:56.428', '2015/09/27', '15:22:56.418', null, null, 168, 36, null, null, 0, null, null, null, null, 0);

sudo apt-get install python-setuptools -y # get easy_install
sudo easy_install pip
sudo pip install awscli

awscli --configure

# vagrant@vagrant-ubuntu-trusty-64:~/.aws$ cat config
# [default]
# region = us-east-1

# vagrant@vagrant-ubuntu-trusty-64:~/.aws$ cat credentials
# [default]
# aws_access_key_id = AKIA****************
# aws_secret_access_key = A**************************************Z

sudo pip install boto3
