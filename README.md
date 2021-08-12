Copyright (c) 2021. Sergei Sazonov. All Rights Reserved





# Installation:
1. Set-up environment variables:

    `export SECRET_KEY='your long key'`
    
    `export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'`
    
    `export EMAIL_USER="your@email"`
    
    `export EMAIL_PASS="your_pass" `
    
    `export STRAVA_AUTH_URL="https://www.strava.com/oauth/authorize"`
    
    `export STRAVA_APP_CLIENT_ID="your_strava_app_id"`
    
    `export STRAVA_APP_CLIENT_SECRET='your_strava_app_client_secret'`
    
    `export STRAVA_APP_REDIRECT_URI="http:<HOSTNAME>/exchange_token"`
    
    `export FLASK_APP="cycperf:create_app()"`


2. run 
   
   `flask db upgrade`
   
    `cd generated/python && python setup.py install && cd ../..`


