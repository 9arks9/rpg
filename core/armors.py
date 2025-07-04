import json
from inventory import Inventory

with open("data/items/armors.json", encoding="utf-8") as f:
    ARMORS = json.load(f)

def zaloz(gracz, armor_id):
    inv = gracz.inventory
    # Pobierz item do założenia
    item_to_wear = None
    for item in inv.ekwipunek:
        if isinstance(item, dict) and item.get("id") == armor_id:
            item_to_wear = item
            break
    if not item_to_wear:
        print("Nie masz tej zbroi w ekwipunku!")
        return False
    slot = item_to_wear.get("slot", "zbroja")
    # Sprawdź czy slot już zajęty i podmień
    for item in inv.ekwipunek_na_sobie[:]:
        if item.get("slot", "zbroja") == slot:
            inv.ekwipunek_na_sobie.remove(item)
            inv.ekwipunek.append(item)
            print(f"Zdjęto: {item.get('nazwa')} ({slot})")
    inv.ekwipunek.remove(item_to_wear)
    item_to_wear["slot"] = slot
    inv.ekwipunek_na_sobie.append(item_to_wear)
    inv.save_ekwipunek()
    inv.save_ekwipunek_na_sobie()
    print(f"Założono: {item_to_wear['nazwa']} ({slot})")
    return True
