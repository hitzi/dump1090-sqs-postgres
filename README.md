# dump1090-sqs-postgres
Programs to capture the SBS1 (BaseStation) output from a dump1090 receiver and send it to a postgres database by way of Amazon SQS.

In my setup, a Raspberry Pi is set to receive Mode S messages (from aircraft) transmitted in the 1090 Mhz frequency. These messages are currently unlogged -- I have had extremely bad luck wearing out SD cards with "normal" levels of read/write operations. By pushing the log messages to SQS, the logging and archiving processes are effectively decoupled.


# Prerequisites
## An AWS account
The use of Amazon's SQS service implies ownership or access to an AWS account. New signups should go here: https://aws.amazon.com/.


## Two SQS queues (one active queue, one dead letter queue)
*dump1090_dlq*
* Default Visibility Timeout: 30 seconds
* Message Retention Period: 14 days
* Maximum Message Size: 1 KB
* Delivery Delay: 0 seconds
* Receive Message Wait Time: 0 seconds
* Use Redrive Policy: No

*dump1090*
* Default Visibility Timeout: 15 seconds
* Message Retention Period: 14 days
* Maximum Message Size: 1 KB
* Delivery Delay: 0 seconds
* Receive Message Wait Time: 0 seconds
* Use Redrive Policy: Yes
* Dead Letter Queue: dump1090_dlq
* Maximum Receives: 2


## IAM credentials that can access the SQS queue
The easiest way forward is to create an IAM user especially for this project and assign it the pre-existing policy "AmazonSQSFullAccess".

The most correct action is to create two IAM users: one with just enough access to push messages onto the queue, and another with just enough access to read messages and delete them from the queue.


## A dump1090 data source
There's a lot that goes into this, but in short this setup assumes a computer setup with the appropriate antenna and generating output in SBS1 format. https://github.com/MalcolmRobb/dump1090 is capable of generating this output.


## A postgres database
On the receiving/archiving end, a computer should be running a postgres database and setup with the provided commands. Once the database is setup, running *sqspoll.py* will poll the queue and insert the records into the messages table for archival and future analysis.

```bash
CREATE ROLE dump1090 WITH LOGIN PASSWORD 'dump1090';

CREATE DATABASE dump1090 OWNER dump1090 TEMPLATE template0;

CREATE TABLE messages (
    MessageType varchar(3),
    TransmissionType smallint,
    SessionID smallint,
    AircraftID smallint,
    HexIdent varchar(6),
    FlightID integer,
    DateMessageGenerated varchar(10),
    TimeMessageGenerated varchar(12),
    DateMessageLogged varchar(10),
    TimeMessageLogged varchar(12),
    Callsign varchar(8),
    Altitude integer,
    GroundSpeed numeric(5, 1),
    Track varchar(8),
    Latitude numeric(8, 5),
    Longitude numeric(8, 5),
    VerticalRate varchar(8),
    Squawk varchar(8),
    Alert varchar(8),
    Emergency varchar(8),
    SPI varchar(8),
    IsOnGround smallint
);

GRANT ALL ON messages TO dump1090;
```
