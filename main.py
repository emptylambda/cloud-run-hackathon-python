
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

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']
pureMoves = [ 'F', 'L', 'R']

def shouldFire(direction, x, y, state):
    if direction == "E":
        logger.info("facing EAST")
        for k in state:
            if state[k]['y'] == y and state[k]['x'] < x and state[k]['x'] > x - 4:
                logger.info("shouldFire")
                return True

    if direction == "W":
        logger.info("facing W")
        for k in state:
            if state[k]['y'] == y and state[k]['x'] > x and state[k]['x'] < x + 4:
                logger.info("shouldFire")
                return True

    if direction == "N":
        logger.info("facing N")
        for k in state:
            if state[k]['x'] == x and state[k]['y'] > y and state[k]['y'] < y + 4:
                logger.info("shouldFire")
                return True

    if direction == "S":
        logger.info("facing S")
        for k in state:
            if state[k]['x'] == x and state[k]['y'] < y and state[k]['y'] > y - 4:
                logger.info("shouldFire")
                return True


    # for k in state:
    #     logger.info("{}: ({}, {})".format(k, state[k]['x'], state[k]['y']))
    logger.info("Find NO shouldFire")
    return False

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    data = request.get_json()
    state = data['arena']['state']
    myUrl = data['_links']['self']['href']
    me    = state[myUrl]
    logger.info("{} {} {}".format(me['x'], me['y'], me['direction']))
    if(shouldFire(me['direction'], me['x'], me['y'], state)):
        return 'T'

    return  pureMoves[random.randrange(len(pureMoves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
