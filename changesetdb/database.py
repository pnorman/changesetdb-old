import psycopg2
import psycopg2.extras


class Database:
    def __init__(self, dbname, host, port, username):
        self.conn = psycopg2.connect(dbname=dbname, host=host, port=port,
                                     username=username)
        psycopg2.extras.register_hstore(self.conn)

        self.counter = 0

    def __del__(self):
        self.conn.commit()

    def createtables(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE EXTENSION IF NOT EXISTS hstore;\n'''
                    '''CREATE EXTENSION IF NOT EXISTS postgis;''')

        cur.execute('''CREATE TABLE osm_changeset_state ('''
                    '''last_sequence bigint,'''
                    '''last_timestamp timestamptz)''')

        cur.execute('''CREATE TABLE osm_changeset ('''
                    '''id bigint not null, user_id bigint,'''
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

    def droptables(self):
        cur = self.conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS '''
                    '''osm_changeset, osm_changeset_state, '''
                    '''osm_changeset_user, osm_changeset_discussion '''
                    '''CASCADE;''')

    def lock(self):
        ''' Lock out other instances with a lock'''
        pass

    def add_user(self, user):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO osm_changeset_user AS u (id, name) '''
                    '''VALUES (%s, %s) ON CONFLICT (id) DO UPDATE '''
                    '''SET name = EXCLUDED.name;''',
                    (user.id, user.name))

    def add_changeset(self, cs):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO osm_changeset (id, user_id, created_at, '''
                    '''closed_at, open, num_changes, '''
                    ''' min_lat, max_lat, min_lon, max_lon, '''
                    '''tags, geom) '''
                    '''VALUES (%s, %s, %s, '''
                    '''%s, %s, %s, '''
                    ''' %s, %s, %s, %s, '''
                    '''%s, %s)''',
                    (cs.id, cs.uid, cs.created_at,
                     cs.closed_at, cs.open, cs.num_changes,
                     cs.bounds.min_lat, cs.bounds.max_lat,
                     cs.bounds.min_lon, cs.bounds.max_lon,
                     cs.tags, str(cs.bounds)))
        self.counter += 1
        if self.counter % 10000 == 0:
            print("imported {}".format(self.counter))
            self.conn.commit()

    def copy_changeset(self, cs):
        self.add_changeset(cs)
