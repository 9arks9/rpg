import json
from inventory import Inventory

# Załaduj dane mikstur
with open("data/items/potions.json", encoding="utf-8") as f:
    POTIONS = json.load(f)

def uzyj(gracz, potion_id):
    # Szukaj mikstury w ekwipunku gracza
    inv = gracz.inventory
    for item in inv.ekwipunek:
        if isinstance(item, dict) and item.get("id") == potion_id:
            ilosc = item.get("ilosc", 1)
            if ilosc > 0:
                efekt = item.get("efekt", 0)
                do_uleczenia = min(efekt, gracz.max_hp - gracz.hp)
                if do_uleczenia <= 0:
                    print("Masz już pełne zdrowie!")
                    return False
                gracz.increase_hp(do_uleczenia)
                print(f"Użyto {item['nazwa']}! Odzyskano {do_uleczenia} HP.")
                if ilosc == 1:
                    inv.ekwipunek.remove(item)
                else:
                    item["ilosc"] = ilosc - 1
                inv.save_ekwipunek()
                return True
            else:
                print("Brak mikstury!")
                return False
    print("Nie masz tej mikstury!")
    return False
