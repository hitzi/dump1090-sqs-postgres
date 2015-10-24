#!/usr/bin/env python

import sys
import boto.sqs
import os

sqs = boto.sqs.connect_to_region(os.environ['AWS_DEFAULT_REGION'])
queue = sqs.create_queue(os.environ['SQS_QUEUE'])

messages = list()
batch = list()

for line in sys.stdin:
  messages.append( line.rstrip(os.linesep) )
  if len(messages) == 10:
    # print ';'.join(messages)
    for i, message in enumerate(messages):
      batch.append( (i+1, message, 0) )
    queue.write_batch(batch)
    batch = list()
    messages = list()
