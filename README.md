Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

# Cyclist Performance

Cyclist Performance is a free Performance Management tool 
for cyclists (and potentially runners in future) with emphasis on analysing cardiovascular 
and metabolic effects of training with power.

Besides, learning purpose (more on that below) in my cycling training journey I needed a simple 
way to analyse and visualize progress of my ability to recover after various training efforts.
I'm talking mainly about post-interval Heart Rate (HR) recovery and HR drift spanning across weeks 
and month of training. More ideas to come.  


Cyclist Performance is deployed on a free Heroku Dyno and is [available](https://cyclist-performance.herokuapp.com/) for use (may take a while to load if Dyno has fallen asleep). You can either create your account and authorize application to get your cycling rides data from [Strava](http://strava.com) or 
play with test dataset based on my own rides. 

This is  mainly a learning project as part of my Open Source Society University [journey](https://github.com/Zepp333333/OSSU "Sergei's OSSU Journey").

Purpose: Gain experience of building a web application by doing along with learning and exercise 
different concepts, techniques and  frameworks. Here is the ever-growing list of things:
- Python
   - OOP
   - Abstract Classes / Interfaces
   - Dataclasses
   - Type hinting 
   - Decorators
   - Pandas basics
   - Package and requirements management
   - requests lib
- Design Patterns in general, including following implemented in the application:
   - Abstract Factory
   - Observer (tbd)
   - Strategy (tbd)
- git basics
- Unit and Functional testing (Pytest)
- Pylint
- Flask basics
   - SQLAlchemy basics
   - Flask migrate
   - Basics of html, css, jinja2, Bootstrap
- Plotly/Dash
- SwaggerClient
- Web Hooks (tbd)
- Packaging and deployment (Heroku)


I've got a lots of inspiration from https://intervals.icu. 
My kudos to David for making such a beautiful and powerful platform. 



# Installation - Heroku:
1. Set environment variables (`heroku config`):

    `export SECRET_KEY='your long key'`
    
    `export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'` or `'potrgresql://...'`
    
    `export EMAIL_USER="your@email"`
    
    `export EMAIL_PASS="your_pass" `
    
    `export STRAVA_AUTH_URL="https://www.strava.com/oauth/authorize"`
    
    `export STRAVA_APP_CLIENT_ID="your_strava_app_id"`
    
    `export STRAVA_APP_CLIENT_SECRET='your_strava_app_client_secret'`
    
    `export STRAVA_APP_REDIRECT_URI="http:<HOSTNAME>/exchange_token"`
    
    `export FLASK_APP="cycperf:create_app()"`


2. `git push heroku master`




