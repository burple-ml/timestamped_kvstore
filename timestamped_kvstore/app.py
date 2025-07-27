from contextlib import asynccontextmanager
from fastapi import FastAPI
from timestamped_kvstore.models import KeyTimestamp, UpdateValue
import psycopg2


# very sloppy might delete later!
def connect_db():
    conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="postgres-db",
            port="5432")
    return conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # set up something
    conn = connect_db()
    with conn.cursor() as cur:
        sql = '''
                CREATE TABLE IF NOT EXISTS public.kvstore(
                    key VARCHAR(50),
                    value VARCHAR(50),
                    timestamp BIGINT, 
                    PRIMARY KEY(key,timestamp)
                );
            '''
        cur.execute(sql)
        conn.commit()
        print("table created")
    yield
    # destroy something


app = FastAPI(lifespan=lifespan)


@app.put("/")
def put_data(req_body: UpdateValue):
    ''' a very sloppy route to do the upsert '''
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute(
                """
                INSERT INTO public.kvstore (key, value, timestamp)
                VALUES (%s, %s, %s)
                ON CONFLICT (key, timestamp)
                DO UPDATE SET value = EXCLUDED.value;
                """,
                (req_body.key, req_body.value, req_body.timestamp)
                )
        conn.commit()
    return {"status": "committed", "data": req_body}


@app.get("/")
def get_data(req_body: KeyTimestamp):
    ''' a very sloppy route to do the lookup '''
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT value
            FROM public.kvstore
            WHERE key = %s AND timestamp <= %s
            ORDER BY timestamp DESC
            LIMIT 1;
            ''',
            (req_body.key, req_body.timestamp))
        row = cur.fetchone()
    return row[0] if row is not None else ""
