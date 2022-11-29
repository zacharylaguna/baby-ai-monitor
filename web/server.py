# CORS error will happen if dev-machine.link:5000 instead of www.dev-machine.link:5000

from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

stuff = False

import threading
import queue
from datetime import datetime
from PIL import Image

MAXSIZE=10

q = queue.Queue()

# helper method
def printHTML(q):
    printed = ''
    li = list(q.queue)
    for item in li:
        printed += '<p>' + item + '</p>'
    return printed

@app.route('/')
def init():
    global stuff
    # return 'Hello, World!' + str(stuff)
    return render_template('index.html')

# in order to properly implement /output 
# we must send a JSON object from flask containing two lists of equal length. 
# One list for the timestamp and one list for the activated or deactivated message
# the receiving JavaScript code can use this JSON object in order to iterate through and put in HTML
# ( if we use response text and we can JSON.parse(this.responseText) )
# potential problem : multiple clients will have overlapping times pushed to queue
# solution : change the return value to just time + alert status; multiple logs handled on the client (javascript)
@app.route('/deprecated-output')
def deprecatedOutput():
    global stuff
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if q.qsize() >= MAXSIZE:
        q.get() # delete one from queue
    if stuff == False:
        q.put(current_time + ' alarm <span style="color:green"> deactivated </span>')
    else:
        q.put(current_time + ' alarm <span style="color:red"> activated </span>')
    return printHTML(q)
    # str(list(q.queue))


@app.route('/output')
def output():
    global stuff
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if stuff == False:
        return {'time' : current_time, 'status' : 'deactivated'}
    else:
        return {'time' : current_time, 'status' : 'activated'}

# asynchronous update
@app.route('/activate')
def alert():
    global stuff
    stuff = True
    return 'alert activated'

# asynchronous update
@app.route('/deactivate')
def unalert():
    global stuff
    stuff = False
    return 'alert deactivated'

# get sound resource
@app.route('/audio/<path:filename>')
def download_audio(filename):
    return send_from_directory('./audio/', filename)

# get image resource
@app.route('/images/<string:filename>/<string:hash>')
def download_image(filename, hash):
    return send_from_directory('./images/', filename)

@app.route("/upload_image", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)

    img.save('images/im-received.jpg') # not file.save() bc of the filestream being not reset to 0
    
    return {'msg': 'success', 'size': [img.width, img.height]}


