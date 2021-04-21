# This file is the application's entry point
import os

from app.__init__ import create_app

# Import 'create_app' function from 'app/init.py'
# the value of 'config_name' is taken from the 'FLASK_CONFIG' OS environment variable
# 08/03/2021 - REPLACED 'FLASK_CONFIG' WITH THE REAL ENVIRONMENT VARIABLE NAME 'FLASK_ENV'
config_name = os.getenv('FLASK_ENV')

# We create the app by running the create_app function and passing the configuration name
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

# 08/03/2021 - FILE RENAMED FROM 'app.py' TO 'run.py'
