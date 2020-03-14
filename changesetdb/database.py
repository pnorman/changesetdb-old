import psycopg2


class Database:
    def __init__(self, dbname, host, port, username):
        self.conn = psycopg2.connect(dbname=dbname, host=host, port=port,
                                     username=username)

    def createtables(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE EXTENSION IF NOT EXISTS hstore;\n'''
                    '''CREATE EXTENSION IF NOT EXISTS postgis;''')

        cur.execute('''CREATE TABLE osm_changeset_state ('''
                    '''last_sequence bigint,'''
                    '''last_timestamp timestamptz)''')

        cur.execute('''CREATE TABLE osm_changeset ('''
                    '''id bigint not null, user_id bigint not null,'''
                    '''created_at timestamptz, closed_at timestamptz,'''
                    '''open boolean, num_changes integer,'''
                    '''min_lat numeric(10,7), max_lat numeric(10,7),'''
                    '''min_lon numeric(10,7), max_lon numeric(10,7),'''
                    '''tags hstore, geom Geometry(POLYGON,4326) );''')

        cur.execute('''CREATE TABLE osm_changeset_user ('''
                    '''id bigint primary key, name text);''')

        cur.execute('''CREATE TABLE osm_changeset_discussion ('''
                    '''id bigint not null, user_id bigint not null,'''
                    '''date timestamptz not null, text text not null)''')

        self.conn.commit()

    def droptables(self):
        cur = self.conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS '''
                    '''osm_changeset, osm_changeset_state, '''
                    '''osm_changeset_discussion CASCADE;''')

        self.conn.commit()

    def add_user(self, user):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO osm_changeset_user AS u (id, name) '''
                    '''VALUES (%s, %s) ON CONFLICT (id) DO UPDATE '''
                    '''SET name = EXCLUDED.name;''',
                    (user.id, user.name))
        self.conn.commit()
