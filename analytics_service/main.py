from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone

app = FastAPI()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="globaltradesync",
            user="postgres",
            password="shanu9090",
            host="globaltradesync-db",
            port="5432",
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/analytics/{cargo_id}")
async def get_analytics(cargo_id: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT last_updated FROM inventory WHERE cargo_id = %s", (cargo_id,))
        result = cur.fetchone()
        cur.close()
        if not result or "last_updated" not in result:
            raise HTTPException(status_code=404, detail=f"Cargo {cargo_id} not found")
        last_updated = result["last_updated"]
        # Convert naive datetime to offset-aware (assume UTC)
        last_updated_aware = last_updated.replace(tzinfo=timezone.utc)
        delivery_time = (datetime.now(timezone.utc) - last_updated_aware).total_seconds() / 3600
        return {"cargo_id": cargo_id, "delivery_time_hours": round(delivery_time, 2)}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        if conn:
            conn.close()