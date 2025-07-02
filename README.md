# 🧙‍♂️ RPG Survival Game

Tekstowa gra RPG w klimacie realistycznego fantasy z elementami survivalu. Gracz eksploruje świat, walczy z potworami, rozwija postać, wykonuje zadania i dąży do osiągnięcia najwyższego poziomu.

## 🎮 Funkcje gry

- 🌍 Otwarty świat z lochami, ruinami i dziką przyrodą
- ⚔️ System walki turowej z przeciwnikami
- 🌱 Sadzenie roślin i tworzenie mikstur
- 📦 Ekwipunek i ulepszanie przedmiotów
- 🧠 Rozwój umiejętności i zdobywanie doświadczenia
- 🧑‍🤝‍🧑 Interakcje z NPC i handel
- 🧩 Zadania fabularne i poboczne
- 💾 System zapisu i wczytywania gry

## W grze już możesz:
- Zarządzać graczem (statystyki, poziom, exp, leczenie, obrażenia, nazwa)
- Zarządzać ekwipunkiem (dodawanie, usuwanie, wyświetlanie, zapisywanie)
- Zarządzać przedmiotami (wczytywanie z pliku, pobieranie po ID)
- Walczyć z przeciwnikami (obrażenia, loot, sprawdzanie życia)
- Ładować przeciwników z pliku

## 🗂️ Struktura projektu

```
rpg_game/
│
├── main.py                  # Główna pętla gry
├── config.py                # Stałe, ustawienia gry
├── requirements.txt         # Lista bibliotek (jeśli używasz zewnętrznych)
├── README.md                # Opis projektu
├── .gitignore               # Pliki ignorowane przez Git
│
├── data/                    # Dane gry (np. mapy, dialogi, przedmioty)
│   ├── items.json
│   ├── enemies.json
│   ├── quests.json
│   └── locations.json
│
├── core/                    # Logika gry
│   ├── player.py            # Klasa gracza
│   ├── enemy.py             # Klasa przeciwników
│   ├── combat.py            # System walki
│   ├── inventory.py         # Ekwipunek i przedmioty
│   ├── skills.py            # Umiejętności i rozwój
│   ├── quests.py            # Zadania i ich logika
│   ├── world.py             # Mapa i eksploracja
│   └── dialogue.py          # System rozmów z NPC
│
├── utils/                   # Pomocnicze funkcje
│   ├── file_manager.py      # Wczytywanie/zapisywanie danych
│   └── helpers.py           # Różne narzędzia (np. losowość, formatowanie)
│
└── saves/                   # Zapisane stany gry
    └── save1.json

```

## 🚀 Jak uruchomić grę

1. Zainstaluj Pythona (3.10+)
2. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/9arks9/rpg_new.git
   cd rpg_new
   ```

3. Uruchom grę:

   ```bash
   python main.py
   ```

## 📌 Wymagania

- Python 3.10 lub nowszy
- Brak zewnętrznych bibliotek (na razie)

## 📅 Status projektu

🔧 W fazie wczesnego rozwoju. Planowane funkcje: system klas postaci, crafting, więcej lokacji i zadań.

## 📜 Licencja

Projekt tworzony hobbystycznie. Możesz używać i modyfikować na własny użytek.

---

Stworzono z pasji do kodu i gier. ✨
```

readme stworzony przy uzyciu ai
