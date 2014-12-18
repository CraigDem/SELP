# Proposal #

Avaliable at /proposal/proposal.md

## Feedback ##

Will there be any marks lost for running functions primarily by loading a new page for every user action vs updating information asynchronously? Or is it left as a design decision?

My game will use time constraints to limit some purchases to once a day/week/month. Is it okay for me to include a script which will reset those timers to make it far easier to test? 

## General Info ##

Admin Profile:
Username : admin
Password : admin

## INSTALLATION INSTRUCTIONS ##

First, when in the base directory start a virtual environment with:

\# virtualenv -p /usr/bin/python2.7 env

Then activate the virtual environment

\# source env/bin/activate

Then install dependences 

\# pip install -r requirements.txt

then to run the server

\# python civ/civ/manage.py runserver 127.0.0.1:8000

Then open your chosen web browser and navigate to 127.0.0.1:8000

To run tests, 

\# python civ/civ/manage.py tests