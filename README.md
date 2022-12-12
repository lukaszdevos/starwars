# Star Wars Application
Simple app allows to collect, resolve and inspect information about characters in the Star Wars universe from the SWAPI.
SWAPI - hosted by https://github.com/phalt/swapi 


## Run app
created on `Python 3.10.4`

### Set up environment variables:
```
SECRET_KEY=your_secret_key
DEBUG=False
SWAPI_URL=http://localhost:8000
```

### Run commands 
1. `make install` - to install requirements packages
2. `make build` - to build necessary migrations 
3. `make runserver` to run development server

### Important!
1. Run swapi app https://github.com/phalt/swapi, default run on http://localhost:8000
2. Run make runserver, default run on http://localhost:8001