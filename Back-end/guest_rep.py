import db.for_guest as for_guest
global item

def handle_guest_message(message: str, id_orders: int) -> str:
    global item

    message = message.lower()
    if message.endswith("."):
        message = message.rstrip('.')

    if "i'd like a" in message:
        item = message.split("i'd like a")[-1].strip()
        positions = for_guest.get_menu_positions()
        if item in positions:
            for_guest.creating_items(id_orders, item)
            if for_guest.get_dish_type(item) and for_guest.chek_upsell_mes(id_orders):
                mes, item = for_guest.send_upsell_mes(id_orders)
                return mes
            else:
                return "Would you like anything else?"
        else:
            return "Choose something from the menu."

    if "i don't want a" in message:
        item = message.split("i don't want a")[-1].strip()
        return for_guest.delete_items(id_orders, item)

    if "that's all" in message:
        return for_guest.get_total(id_orders)

    if "yes" in message:
        for_guest.creating_items(id_orders, item)
        return "Would you like anything else?"

    if "no" in message:
        return "Would you like anything else?"

    else:
        return "I don't understand."
