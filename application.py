"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014
"""

# Start with a basic flask app webpage.
from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def getLogLines(self):
        #infinite loop of magical random numbers
        while not thread_stop_event.isSet():
            client = KafkaClient("10.0.0.3:9092")
            consumer = SimpleConsumer(client, "my-producer", "alarm")

            for message in consumer:
                print message.message.value
                socketio.emit('newmessage', {'message': message.message.value}, namespace='/test')
                sleep(self.delay)

    def run(self):
        self.getLogLines()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print "Starting Thread"
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000)
