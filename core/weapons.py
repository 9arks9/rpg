import json
from inventory import Inventory

with open("data/items/weapons.json", encoding="utf-8") as f:
    WEAPONS = json.load(f)

def zaloz(gracz, weapon_id):
    inv = gracz.inventory
    for item in inv.ekwipunek:
        if isinstance(item, dict) and item.get("id") == weapon_id:
            inv.ekwipunek.remove(item)
            inv.ekwipunek_na_sobie.append(item)
            inv.save_ekwipunek()
            inv.save_ekwipunek_na_sobie()
            print(f"Założono broń: {item['nazwa']}")
            return True
    print("Nie masz tej broni w ekwipunku!")
    return False
