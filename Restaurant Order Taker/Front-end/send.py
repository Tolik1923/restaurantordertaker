import requests

def send_user_input_to_fastapi(message, id_orders):
    fastapi_url = f"http://app:80/guest/{id_orders}"   
    response = requests.post(fastapi_url, json={"message": message})
    response_data = response.json()
    bot_message = response_data.get("message", "No message from the bot found.")
    return bot_message

def take_id_order():
    id_orders = requests.get("http://app:80/guest").text
    return id_orders

def take_ststs():
    res_1 = requests.get("http://app:80/admin/submitted_orders")
    res_2 = requests.get("http://app:80/admin/general")
    stats = res_1.json()
    general = res_2.json()
    return stats, general
