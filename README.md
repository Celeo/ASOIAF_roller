# ASOIAF_roller

An online dice roller web app for the ASOIAF tabletop RPG.

## Installation

This app has two components: a front-end in Vue.JS and a back-end in Python using the Flask framework. To install:

1. Install Python3, Node, and npm

2. `cd front && npm install && npm run build`

3. `cd back && . env/bin/activate && pip install -r requirements.txt`

## Running

1. `cd back && . env/bin/activate && nohup ./run.py &`

2. `cd front && npm run dev`
