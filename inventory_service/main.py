from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="globaltradesync",
            user="postgres",
            password="shanu9090",
            host="globaltradesync-db-service",
            port="5432",
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/inventory/{cargo_id}")
async def get_inventory(cargo_id: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE cargo_id = %s", (cargo_id,))
        result = cur.fetchone()
        cur.close()
        if not result:
            raise HTTPException(status_code=404, detail=f"Cargo {cargo_id} not found")
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        if conn:
            conn.close()