from fastapi import FastAPI
import asyncio

import db.creation_db as creation_db
import db.creation_table as creation_table
import db.exsport_menu as exsport_menu
from guest_rep import handle_guest_message
import modules
import db.for_guest as for_guest
import db.for_admin as for_admin

app = FastAPI()

chat_sessions = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to Restaurant Order Taker"}

@app.on_event("startup")
async def startup_db():
    await asyncio.sleep(10)
    creation_db.create_database()
    creation_table.create_database_objects()
    exsport_menu.import_menu_from_csv()

@app.on_event("shutdown")
async def clean_menu():
    exsport_menu.menu_cleaning()

@app.get("/guest")
async def create_id():
    return for_guest.creating_order()

@app.post("/guest/{id_orders}")
async def guest_part(request: modules.GuestMessage, id_orders: int):
    response = handle_guest_message(request.message, id_orders)
    for_guest.input_history(request.message, response, id_orders)
    return {"message": response} 

@app.get("/admin/submitted_orders")
async def admin_part():
    stats = for_admin.get_all_submitted_orders()
    return stats

@app.get("/admin/general")
async def admin_part():
    general = for_admin.get_general_order_stats()
    return general 
