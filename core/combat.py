from player import Gracz
from enemy import Przeciwnik
import random

def walcz(gracz: Gracz, przeciwnik: Przeciwnik):
    print(f"\n⚔️ Walka: {gracz.nazwa} vs {przeciwnik.nazwa}")
    print(f"{gracz.nazwa} HP: {int(gracz.hp)} | {przeciwnik.nazwa} HP: {int(przeciwnik.hp)}")

    while gracz.hp > 0 and przeciwnik.hp > 0:
        input("\n👉 Naciśnij Enter, aby zaatakować...")

        # Gracz atakuje
        obrazenia, czy_kryt = gracz.zadaj_obrazenia_z_krytem()
        przeciwnik.hp = max(0, przeciwnik.hp - obrazenia)
        print(f"🗡️ {gracz.nazwa} zadaje {obrazenia} obrażeń!", end=" ")
        if czy_kryt:
            print("💥 CIOS KRYTYCZNY!")
        else:
            print()
        print(f"❤️ {przeciwnik.nazwa} ma teraz {int(przeciwnik.hp)} HP")

        if przeciwnik.hp <= 0:
            print(f"\n✅ {gracz.nazwa} pokonał {przeciwnik.nazwa}!")
            xp = przeciwnik.level * 5
            gracz.increase_xp(xp)
            loot = losuj_loot(przeciwnik.loot)
            print(f"🎁 Zdobyto loot: {loot}")
            return "wygrana", loot

        # Przeciwnik kontratakuje
        obrazenia_wroga = przeciwnik.zadaj_obrazenia()
        gracz.przyjmij_obrazenia(obrazenia_wroga)
        print(f"💥 {przeciwnik.nazwa} zadaje {obrazenia_wroga} obrażeń!")
        print(f"❤️ {gracz.nazwa} ma teraz {int(gracz.hp)} HP")

        if gracz.hp <= 0:
            print(f"\n💀 {gracz.nazwa} został pokonany przez {przeciwnik.nazwa}...")
            return "przegrana", []

def losuj_loot(loot_lista):
    if not loot_lista:
        return []
    return loot_lista  # Możesz dodać losowość tutaj
