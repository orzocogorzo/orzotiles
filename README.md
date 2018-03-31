INSTRUCTIONS TO SETUP A TILESERVERGL SERVER WITH CUSTOM DATA SOURCE AND STYLES

START THE PROJECT

1. Create project folder
    
        git clone git@code.bestiario.org:lucas/tileserverGL.git && cd tileserverGL && mkdir data && mkdir build && mkdir backup



INSTALL DEPENDENCIES

1. Build npm environment

        sudo npm install -g n
        sudo n stable (install last version of node)
	sudo n 6.14.1 (install and use requested version)
        sudo npm install --upgrade npm
        sudo npm install -g \
        node-gyp \
        node-pre-gyp \
        nvm \
        yarn

        source ~/.profile
        
        n 6.14.1
	yarn init -y

2. Install dev libraries
	
        sudo apt-get install  \
          apt-transport-https
          curl \
          unzip \
          build-essential  \
          python \
          libcairo2-dev \
          libgles2-mesa-dev \
          libgbm-dev libllvm3.9 \
          libprotobuf-dev \
          libxxf86vm-dev \
          xvfb \
          graphviz \ 
          sqlite3 \
          zlib1g-dev \ 
          cmake \
          libosmium2-dev \ 
          git \
          postgresql-client \
          wget \
          ca-certificates \
          osmctools \
          osmosis \
          libleveldb-dev \
          libgeos-dev \
          mason \
          libmapnik-dev
    
        sudo apt-get clean



SETUP POSTGRES DB

0. Install dependencies

    0.1. Install PostgreSQL and PostGIS dependencies
      
        apt-get -qq -y --no-install-recommends install \
          autoconf \
          automake \
          autotools-dev \
          bison \
          dblatex \
          docbook-mathml \
          docbook-xsl \
          gdal-bin \
          libcunit1-dev \
          libkakasi2-dev \
          libtool \
          pandoc \
          xsltproc \
          libgdal-dev \
          libjson0-dev \
          libproj-dev \
          libxml2-dev \
          postgresql-server-dev-all
          
        sudo apt-get clean

1. Install development dependencies packages

	1.0. Add dependencies folder
	
        mkdir devDependencies && cd devDependencies
	    
	1.1. Get GEOS project from http://download.osgeo.org/geos/geos-3.6.0.tar.bz2
	
        curl -o geos-3.6.0.tar.bz2 http://download.osgeo.org/geos/geos-3.6.0.tar.bz2 && \
        mkdir geos && tar xf geos-3.6.0.tar.bz2 -C geos --strip-component=1 \
        && sudo ./configure && sudo make && sudo make install
             
	1.2. Get World Location Names UTF Dictonary from https://github.com/JuliaLang/utf8proc.git
	        
        git clone https://github.com/JuliaLang/utf8proc.git && cd utf8proc && \
        sudo make && sudo make install && sudo ldconfig
	        
	1.3. Get Mapnik German Dictionary repository from https://github.com/openmaptiles/mapnik-german-l10n.git
	
        git clone https://github.com/openmaptiles/mapnik-german-l10n.git \
        && cd mapnik-german-l10n && sudo make && sudo make install
	        
	1.4. Get Protobuf project repository from https://github.com/google/protobuf.git
	
        git clone https://github.com/google/protobuf.git \
        && cd protobuf && sudo ./autogen.sh && sudo ./configure && sudo make && sudo make check \
        && sudo make install && sudo ldconfig
	        
	1.5. Get Protobuf C project repository from https://github.com/protobuf-c/protobuf-c.git
	
        git clone https://github.com/protobuf-c/protobuf-c.git && cd protobuf-c && sudo \
        ./autogen.sh && sudo ./configure && sudo make && sudo make install
        
    1.6. Return to the root directory
	

2. Create DB and install extensions

	2.0. Create a postgreSQL user like your system user name to make easier the work
	
        sudo su postgres && psql -c "CREATE USER admintile WITH SUPERUSER LOGIN PASSWORD {{password}};"
        exit (for exit superuser)
	    
	2.0. Create the DB dependencies folder create DB role and the database 
	    
        mkdir pgsql-extensions && cd pgsql-extensions && psql -c "CREATE DATABASE tileserver;"
	
	2.1. Extend our DB with the required extensions
	
        psql -d tileserver -c "CREATE EXTENSION postgis; \
        CREATE EXTENSION hstore; CREATE EXTENSION unaccent; \
        CREATE EXTENSION fuzzystrmatch; \
        CREATE EXTENSION osml10n; \
        CREATE EXTENSION pg_stat_statements;"

3. Add functions from vt-utils

	3.0. Extend the DB with vt-utils functions from https://github.com/mapbox/postgis-vt-util.git 
	    
        git clone https://github.com/mapbox/postgis-vt-util.git && cd postgis-vt-utils && /
        psql -d tileserver -f postgis-vt-util.sql && cd ..

4. Add language functions

	4.1. Extend DB with openmaptiles project language functions
	    
        git clone https://github.com/openmaptiles/import-sql.git && \
        cd import-sql && psql -d tileserver -f language.sql && cd ..
        
    4.2 Return to the root directory
        


INSTALL SCHEMA

1. Clone openmaptiles from git to use it as a schema example

    1.0. Schema directory example
   
           openmaptiles/
            \_ layers/ (layer definitions folders)
                \_ aeroway (layer definition folder)
                    |_ aeroway.yaml (layer definition)
                    |_ layer.sql (sql functions)
                    |_ mapping.yaml (schema mapping data)
                    |_ boundary (layer definition folder)
                    |_ etc
            |_ openmaptiles.yaml (tileset definition pointing to layers)
        
    
    1.1. Copy directory from GIT
    
        git clone https://github.com/klokantech/openmaptiles.git && cd openmaptiles \
        && mv ./layers .. && mv ./openmaptiles.yaml ../tileset.yaml && cd .. && sudo rm -rf openmaptiles

2. Install openmaptiles-tools 

    2.1. openmaptiles-tools are the tools to build the mbtiles based on the schema
    
        pip install openmaptiles-tools 
        
    or
        
        pip install git+https://github.com/openmaptiles/openmaptiles-tools"


BUILD MBTILES

0. Download the data from Geofabrik

    0.1. Now our directory structure looks like this
    
           tilserverGL/
            |_ layers
            |_ openmaptiles.yaml
            |_ index.html
            |_ devDependencies
            |_ node_modues
            |_ package.json
            |_ data
            |_ build
            |_ yarn-error.log
            |_ yarn.lock
            |_ pgsql-extensions
            
            
    0.1. Save data into its folder from http://download.geofabrik.de/ in osm.pbf format
    
        cd data && curl -o {{regionName}}.osm.pbf http://download.geofabrik.de/{{regionName}}.osm.pbf

1. Import complementary data to complete the schema data sources

    1.0. Create a folder for complementary datasources
    
        mkdir schemaData && cd schemaData
        
    1.1 Import water data
    
    1.1.1. Download the data from data from www.openstreetmapdata.com

        mkdir osmWaterData && cd osmWaterData \
        && wget --quiet http://data.openstreetmapdata.com/water-polygons-split-3857.zip \
        && unzip -oj water-polygons-split-3857.zip -d . \
        && rm water-polygons-split-3857.zip \
        && wget --quiet http://data.openstreetmapdata.com/simplified-water-polygons-complete-3857.zip \
        && unzip -oj simplified-water-polygons-complete-3857.zip -d . \
        && rm simplified-water-polygons-complete-3857.zip
    
    1.1.2. Get import instructions from https://raw.githubusercontent.com/openmaptiles/import-water/master/import-water.sh and save it in the folder

    1.1.3. Modify the file declaring the next variables before the two variables yet declareds on the file

        POSTGRES_PASSWORD="{{psql password}}"
        POSTGRES_HOST="localhost"
        POSTGRES_PORT="5432"
        POSTGRES_DB="tileserver"
        POSTGRES_USER="{{your user name}}"
        IMPORT_DATA_DIR="./"
    
    1.1.4. Execute the import instructions

        ./import-water.sh && cd ..
        
    1.2. Import lakelines data
        
    1.2.1. Download data from https://github.com/lukasmartinelli/osm-lakelines
        
        mkdir lakeLinesData && cd lakeLinesData \
        && wget --quiet -L -P . https://github.com/lukasmartinelli/osm-lakelines/releases/download/v0.9/lake_centerline.geojson \
        
    1.2.2. Get import instructions from https://raw.githubusercontent.com/openmaptiles/import-lakelines/master/import_lakelines.sh and save it in the folder
    1.2.3. Modify the file adding the newxt variables
        
        IMPORT_DIR="./"
        POSTGRES_PASSWORD="{{psql password}}"
        POSTGRES_HOST="localhost"
        POSTGRES_PORT="5432"
        POSTGRES_DB="tileserver"
        POSTGRES_USER="{{your user name}}"
        
    1.2.4. Execute the import instructions
    
        ./import-lakelines.sh && cd ..
        
    1.3. Import natural-earth data 
    1.3.1 Download the data from http://naciscdn.org
    
        mkdir naturalEarthData && cd naturalEarthData |
        && wget --quiet http://naciscdn.org/naturalearth/packages/natural_earth_vector.sqlite.zip \
        && unzip -oj natural_earth_vector.sqlite.zip -d .
        && rm natural_earth_vector.sqlite.zip
        
    1.3.2. Get import instructions from https://raw.githubusercontent.com/openmaptiles/import-natural-earth/master/import-natural-earth.sh and save it in the folder. Get also the clean DB instructions from https://raw.githubusercontent.com/openmaptiles/clean-natural-earth/master/import-natural-earth.sh
            
    1.3.3. Modify the file adding the newxt variables

        NATURAL_EARTH_DB="./natural_earth_vector.sqlite"
        POSTGRES_PASSWORD="{{psql password}}"
        POSTGRES_HOST="localhost"
        POSTGRES_PORT="5432"
        POSTGRES_DB="tileserver"
        POSTGRES_USER="{{your user name}}"
        
    1.3.4. Execute import instructions
    
        ./import-natural-earth.sh && cd ..
        
    1.4. Import OSM borders data
    
    1.4.1. Download data from https://github.com/openmaptiles/import-osmborder.
    
        mkdir osmBoderData && cd osmBorderData \
        && wget -O pgfutter https://github.com/lukasmartinelli/pgfutter/releases/download/v1.1/pgfutter_linux_amd64 \
        && chmod +x pgfutter \
        && mv pgfutter /usr/local/bin/ \
        && wget -O ./osmborder_lines.csv.gz https://github.com/openmaptiles/import-osmborder/releases/download/v0.4/osmborder_lines.csv.gz \
        
    1.4.2. Get import instructions from https://raw.githubusercontent.com/openmaptiles/import-osmborder/master/import/import_osmborder_lines.sh and save it in the folder.
    1.4.3. Modify the file adding the newxt variables
        
        IMPORT_DIR="./"
        POSTGRES_PASSWORD="{{psql password}}"
        POSTGRES_HOST="localhost"
        POSTGRES_PORT="5432"
        POSTGRES_DB="tileserver"
        POSTGRES_USER="{{your user name}}"
        
    1.4.4. Execute import instructions
    
        ./import-osmborder.sh && cd ..
            
    1.5. Return to root directory

2. Build the tm2source file

	2.0. Make tm2source folder into build directory

        mkdir -p build/tileset.tm2source
	    
	2.1. Use generate-tm2source to export the tmsource definition file inside the folder. tm"source file maps the DB tables structure and our tileset layers definitions
	    
        generate-tm2source tileset.yaml --host="localhost" --port=5432 --database="tileserver" \ 
        --user="orzo" --password="Contrasenya92_" > build/tileset.tm2source/data.yml

3. Map the data using the schema structure

	3.1. Use generate-imposm3 to export the import schema file to transform osm.pbf file into postgis tables following our schema definition
	    
        generate-imposm3 tileset.yaml >build/mapping.yaml

4. Build sql methods to extract data from the DB throw the schema especifications

	4.1. Use henerate-sql tool to build sql methods to import to our DB and allow it to export data based on our schema especifications
	    
        generate-sql tileset.yaml > build/tileset.sql

5. Install imposm3 tool to import data from tm2source file to a PostGIS db
	5.0. Make a folder to contain GO repositories
    
        mkdir go

    5.1. Point GOPATH to the new folder
    
        export GOPATH=$(pwd)/go && export GOROOT=$HOME/go
        
	5.2. Get imposm package with GO and save it on $GOPATH/src folder
	    
        go get github.com/omniscale/imposm3
	    
	5.3. Tell go to install the new package
	    
        go install github.com/omniscale/imposm3/cmd/imposm3
        
	5.4. Add GO bin folder to the PATH
	    
        export PATH=$PATH:$GOPATH/bin

6. Import osm with imposm3
	6.1. Use imposm3 to import data from the pbf (protobufer) to our DB
        
        imposm3 import -connection postgis://{{psqlUser}}:{{psqlPassword}}@localhost:5432/tileserver -mapping build/mapping.yaml / 
        -read data/{{regionName}}.osm.pbf -write

7. Extend DB with schema queries
	7.0. imposm3 import tables into schema import. It's important to move data to public schema
		
        psql -d tileserver -c "\dt .import" > build/fixschema.sql
		
        touch build/fixschema.py
        gedit build/fixschema.py
        copy this code:
            
        ```
          import os.path as path
          file = os.path.join(os.path.abspath(__file__),'fixschema.sql')
          queries = ''
          queryTmpl = 'ALTER TABLE {0} SET SCHEMA public;\n"
          tables = open(file).read().split('\n')

          for table in tables:
            if 'import' in table:
              tableName = table.split('|')[1].strip()
              query = queryTmplt.format(tableName)
              queries = queries + query
			
          with open(file,'w') as output:
            output.write(queries)
        ```
        save
		
        python build/fixschema.py		
        psql -d tileserver -f fixschema.sql
				
					

	7.1. Import built functions to the DB
	    
        psql -d tileserver -f build/tileset.sql

8. Generate mbtiles
    8.0. Install tilelive-copy from npm.

        yarn add --save-dev tl@0.8.1 \
            @mapbox/tilelive@^5.12.6 \
            @mapbox/tilelive-bridge@^2.5.1 \
            @mapbox/tilelive-mapnik@^0.7.0 \
            @mapbox/tilelive-vector@^3.10.1 \
            mapnik@^3.6.2 \
            tilelive-tmsource@^0.6.1 \
            tileserver-gl@^2.2.0 \
            tl@^0.10.1
        
	8.1. Register tmsource and mbtiles protocols on tilelive.js file.
		
		gedit node_modules/tilelive/lib/tilelive.js
		add "mbtiles": require("mbtiles"), "tmsource": require("tilelive-tmsource") in protocol dictionary
		save

	8.2. Execute tilelive-copy binary to transform tmsource file into mbtiles getting data from the DB.
	    
	    tilelive-copy --scheme=pyramid --bounds="{{get bounds from http://boundingbox.klokantech.com/ in csv format}}" \
    		--timeout="-1800000" --concurrency="-10" --minzoom="{{minzoom(low)}}" --maxzoom="{{maxzoom(high)}}" \
    		"tmsource://./build/openmaptiles.tm2source/data.yml" "mbtiles://./data/{{regionName}}.mbtiles"

	8.2. If problems with tilelive, go throw log , identify which package has problems, go to its folder and try to npm rebuild or npm install.

	8.3. If tilelive-copy failes, try with tl copy -z {{minZoom}} -Z {{maxZoom}} -b "{{boundingbox}} --scheme=pyramid tmsource://./build/openmaptiles.tm2source mbtiles://./data/{{regionName}}.mbtiles
	

GET VECTOR STYLES

1. Add a folder to palce all our styles and download predefined styles

    1.1. Add the styles folder
    
        mkdir styles && cd styles
    
    1.2. Download styles from the next repositories
    
        git clone https://github.com/openmaptiles/dark-matter-gl-style
        git clone https://github.com/openmaptiles/fiord-color-gl-style
        git clone https://github.com/openmaptiles/klokantech-basic-gl-style
        git clone https://github.com/openmaptiles/klokantech-3d-gl-style
        git clone https://github.com/openmaptiles/toner-gl-style
        git clone https://github.com/openmaptiles/positron-gl-style
        git clone https://github.com/openmaptiles/osm-bright-gl-style
        
    1.3. Return to the root directory
    
GET FONTS

1. To setup the server you should declare path to fonts in the config file
    1.1. Get default fonts from node_modules/tilelive-gl directoru

        cp -R node_modules/tileserver-gl/fonts .

INSTALL SERVER

1. Get tileserverGl project from npm repository

    1.0. Install de package
        
        yarn add tileserver-gl --save
        
    1.1. Test
        
        tileserver-gl
        
    1.2. If some package fails, read the log and identify which package raise error, go to its folder on node_models and run:
    
        npm install OR npm rebuild

2. Write config file
    2.1. Get example from https://tileserver.readthedocs.io/en/latest/config.html

3. run tileserver-gl inside a folder with config file and open localhost:8080 to see the result


TEST PROJECT

9. Test the environment
	9.0. Setup tileserver-gl on project folder where config.json is placed
	9.1. Setup python -m SimpleHTTPServer
	9.2. Go to localhost:8000

GENERATE CUSTOM STYLES

1. Style especification on https://www.mapbox.com/mapbox-gl-js/style-spec/
2. Download the editor from https://github.com/maputnik/editor
        
        git clone https://github.com/maputnik/editor && mv editor maputnik && cd maputnik

3. Install and start the editor
        
        yarn install && yarn run start
