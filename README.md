# ASOIAF_roller

An online dice roller web app for the ASOIAF tabletop RPG.

## Installation

This app has two components: a front-end in Vue.JS and a back-end in Python using the Flask framework. To install:

1. Install Python3, Node, and npm

2. `cd front && npm install`

3. `cd back && . env/bin/activate && pip install -r requirements.txt`

## Running

### Development

1. `cd back && . env/bin/activate && nohup ./run.py &`

2. `cd front && npm run dev`

### Production

For production, build the frontend component with `npm run build` and point your server to the `index.html` file. Run the backend in the same manner as during development.
