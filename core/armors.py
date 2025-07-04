import json
from inventory import Inventory

with open("data/items/armors.json", encoding="utf-8") as f:
    ARMORS = json.load(f)

def zaloz(gracz, armor_id):
    inv = gracz.inventory
    for item in inv.ekwipunek:
        if isinstance(item, dict) and item.get("id") == armor_id:
            inv.ekwipunek.remove(item)
            inv.ekwipunek_na_sobie.append(item)
            inv.save_ekwipunek()
            inv.save_ekwipunek_na_sobie()
            print(f"Założono zbroję: {item['nazwa']}")
            return True
    print("Nie masz tej zbroi w ekwipunku!")
    return False
