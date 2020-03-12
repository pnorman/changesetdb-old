# ChangesetDB

## About
ChangesetDB is a simple XML parser written in python that takes the weekly changeset metadata dump file from http://planet.openstreetmap.org/ and shoves the data into a simple postgres database so it can be queried.

It can also keep a database created with a weekly dump file up to date using minutely changeset diff files available at http://planet.osm.org/replication/changesets/

## Setup

For local development

```sh
python3 -m venv venv
. venv/bin/activate
pip install --editable .
changesetdb
```

ChangesetMD requires a PostgreSQL database with PostGIS and hstore. It will attempt to install these extensions if they are not found.

```sh
createdb changesets
```

In production you should use a dedicated user with write access to the tables and run queries with a read-only user.

## Usage
The first time you run it, you will need to include the -c | --create option to create the table:

```sh
changesetdb -d <database> -c
```

The create function can be combined with the file option to immediately parse a file.

```sh
changesetdb -d <database> -f /tmp/changeset-latest.osm
```

If no other arguments are given, it will access postgres using the default settings of the postgres client, typically connecting on the unix socket as the current OS user. Use the ``--help`` argument to see optional arguments for connecting to postgres.


## License
Copyright (C) 2012 Toby Murray
Copyright (C) 2020 Paul Norman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU Affero General Public License for more details: http://www.gnu.org/licenses/agpl.txt

