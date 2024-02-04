# Create the Virtual Environment

export WORKON_HOME=~/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3.10 water_pipeline

# activate the virtual environment

source ~/.virtualenvs/water_pipeline/bin/activate

# This will use the same Python version of the virtualenv

pip install Django==4.0

# GDAL installation (follow following steps)

Before installing the GDAL Python libraries, you’ll need to install the GDAL development libraries.
sudo apt-get install libgdal-dev

You’ll also need to export a couple of environment variables for the compiler.

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

Now you can use pip to install the Python GDAL bindings.
pip install GDAL==3.4.1

Give the path in django setting: This is the optional step
if os.name == 'nt':
VENV_BASE = os.environ['VIRTUAL_ENV']
os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo') + ';' + os.environ['PATH']
os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(**file**).resolve().parent.parent

# postgres installation with the postgis

# It is a standard task that we need to update our system prior to the installation

sudo apt update

# Now let’s install PostgreSQL and all its dependency files

sudo apt install postgresql postgresql-contrib

# Let’s start the service

sudo systemctl start postgresql

# Create a new PostgreSQL role and database

sudo -i -u postgres
psql
CREATE USER mappers with password 'mappers123';
CREATE DATABASE digitalmap;

# Now switch to your ubuntu user and enter following command.

# Note: You must install the postgis version associated with installed postgresql

sudo apt-get install postgresql-16-postgis-3

# Connect to the your database you are wanting to install extension

\c digitalmap
GRANT ALL PRIVILEGES ON SCHEMA public TO mappers;
CREATE EXTENSION postgis;

# If you want to give the ownership of new table to mappers user, please execute the following code in the postgresql command line

-- Grant ownership of new tables in the "public" schema to the "mappers" user
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
GRANT ALL ON TABLES TO mappers;

# if you want to make superuser to the new user

-- Grant all privileges on all databases to the farm user
ALTER USER farm WITH SUPERUSER;

# Geoserver installation and auto startup

sudo -u root -i
sudo apt-get update

# Geoserver currently only supports JAVA-JRE-8, you can install it by typing

sudo apt-get install openjdk-8-jdk
sudo apt-get install openjdk-8-jre

# To cross-check installation, type

java -version

# We’ll create a new directory and put GeoServer in it

cd /usr/share
mkdir geoserver
cd geoserver
wget https://build.geoserver.org/geoserver/main/geoserver-main-latest-bin.zip

# The next step is to unzip the geoserver-main-latest-bin.zip.

unzip geoserver-main-latest-bin.zip

# Finally, we’ll set up a variable to make it workable

echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
. ~/.profile

# and make sure that the user is the owner of this folder as well

sudo chown -R USER_NAME /usr/share/geoserver/

# If you want to auto start the geoserver on booting you should follow following steps also

# Create a systemd service unit file. For example, let's assume you want to start a script called startup.sh in the /usr/share/geoserver/bin/ directory:

# Create a new service unit file with the .service extension in the /etc/systemd/system/ directory. You can use a text editor to create the file:

sudo nano /etc/systemd/system/geoserver-startup.service

# Add the following content to the file (adjust the ExecStart line to point to your script or command):

[Unit]
Description=Start GeoServer on Boot

[Service]
Environment="GEOSERVER_HOME=/usr/share/geoserver"
ExecStart=/usr/share/geoserver/bin/startup.sh

[Install]
WantedBy=multi-user.target

# Reload systemd to pick up the changes:

sudo systemctl daemon-reload

# Enable the service to start on boot:

sudo systemctl enable geoserver-startup

# Start the service for the current session:

sudo systemctl start geoserver-startup
#To check the status of the service:
sudo systemctl status geoserver-startup

# Allow cross origin resource sharing (CORS)

sudo apt install vim
sudo vim web.xml

# use arrow keys to move down until you find a line with CORS in Jetty written.Once you find it, Uncomment the code and again search for CORS, Since we are not using tomcat, you can keep CORS related to tomcat commented. You can find the third and final code for CORS.
