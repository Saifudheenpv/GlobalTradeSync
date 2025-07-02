from fastapi import FastAPI
import json

app = FastAPI()

with open("cargo_data.json", "r") as f:
    cargo_data = json.load(f)

@app.get("/cargo/{cargo_id}")
async def get_cargo_status(cargo_id: str):
    return cargo_data.get(cargo_id, {"error": "Cargo not found"})