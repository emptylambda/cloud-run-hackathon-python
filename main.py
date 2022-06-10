
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request, jsonify

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def shouldFire(me, state):
    facing = me['direction']
    myX = me['x']
    myY = me['y']
    if facing == "E":
        for k in state:
            if state[k]['x'] > myX and state[k]['x'] < myX + 3:
                logging.info("SHOULD FIRE")
                return True
    if facing == "W":
        for k in state:
            if state[k]['x'] < myX and state[k]['x'] > myX - 3:
                logging.info("SHOULD FIRE")
                return True
    if facing == "N":
        for k in state:
            if state[k]['y'] < myY and state[k]['y'] > myX - 3:
                logging.info("SHOULD FIRE")
                return True
    if facing == "S":
        for k in state:
            if state[k]['y'] < myY and state[k]['y'] + myX + 3:
                logging.info("SHOULD FIRE")
                return True

    logging.info("SHOULD NOT FIRE")
    return False

def isSafeMove(me, size):
    # avoid going into corners
    return True

def state2Map(state):
    botLocs = []
    for k in state:
        botLocs.append((state[k]['x'], state[k]['y']))
    return botLocs

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']

def dodge(me, state):
    return 'F'

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    data = request.get_json()
    state = data['arena']['state']
    myUrl = data['_links']['self']['href']
    me    = state[myUrl]
    if(shouldFire(me, state)):
        return 'T'

    return  moves[random.randrange(len(moves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
