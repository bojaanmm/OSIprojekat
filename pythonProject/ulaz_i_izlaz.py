import tkinter as tk
import json
import random
import string
from datetime import datetime
from tkinter import messagebox

# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Ulaz i izlaz")
root.geometry("400x300")  # Širina x Visina

# Postavljanje ikone prozora
root.iconphoto(False, tk.PhotoImage(file="parking.png"))

# Promjena boje pozadine prozora na neutralno plavu
root.config(bg="#A9CFE8")

# Funkcija za generisanje nasumičnog jedinstvenog koda
def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Funkcija za učitavanje podataka iz JSON fajla
def load_parking_data():
    try:
        with open("parking_administration.json", "r") as file:
            data = json.load(file)
            # Osiguravanje da svi potrebni ključevi postoje
            if "total_parking_spots" not in data:
                data["total_parking_spots"] = 10
            if "occupied_spots" not in data:
                data["occupied_spots"] = 0
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"total_parking_spots": 10, "occupied_spots": 0}  # Defaultni podaci
        save_parking_data(data)
        return data

# Funkcija za ažuriranje podataka u JSON fajlu
def save_parking_data(data):
    with open("parking_administration.json", "w") as file:
        json.dump(data, file, indent=4)

# Funkcija za ažuriranje prikaza slobodnih mjesta
def update_free_spots():
    data = load_parking_data()
    total_spots = data.get("total_parking_spots", 0)
    occupied_spots = data.get("occupied_spots", 0)
    free_spots = total_spots - occupied_spots
    label_free_spots.config(text=f"Slobodna mjesta: {free_spots}")

# Funkcija za rukovanje unosom registarskih oznaka
def handle_input():
    reg_oznaka = entry.get()
    if reg_oznaka:
        # Učitavanje postojećih podataka
        data = load_parking_data()

        if data["occupied_spots"] >= data["total_parking_spots"]:
            messagebox.showwarning("Upozorenje", "Nema slobodnih mjesta!")
            entry.delete(0, tk.END)
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_code = generate_unique_code()
        parking_record = {"reg_oznaka": reg_oznaka, "vrijeme": current_time, "kod": unique_code}

        # Dodavanje zauzetog mjesta
        data["occupied_spots"] += 1
        save_parking_data(data)

        # Dodavanje novog vozila u parking_data.json
        try:
            with open("parking_data.json", "r") as json_file:
                parked_vehicles = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            parked_vehicles = []

        # Dodavanje nove evidencije u listu
        parked_vehicles.append(parking_record)

        # Spremanje ažurirane liste u fajl
        with open("parking_data.json", "w") as json_file:
            json.dump(parked_vehicles, json_file, indent=4)

        # Kreiranje .txt fajla sa informacijama
        with open(f"parking_ticket_{unique_code}.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write("Račun za parkiranje\n")
            txt_file.write("=====================\n")
            txt_file.write(f"Registarska oznaka: {reg_oznaka}\n")
            txt_file.write(f"Vrijeme: {current_time}\n")
            txt_file.write(f"Jedinstveni kod: {unique_code}\n")
            txt_file.write(f"Status: Nije plaćeno\n")
            txt_file.write("=====================\n")
            txt_file.write("Hvala na korištenju našeg sistema!\n")

        # Prikaz poruke o uspjehu
        messagebox.showinfo("Uspjeh", f"Unos registarskih oznaka '{reg_oznaka}' je uspješno zabilježen!")

        print(f"Unesena registarska oznaka: {reg_oznaka}, Vrijeme: {current_time}, Kod: {unique_code}")
        update_free_spots()
        entry.delete(0, tk.END)

# Funkcija za ažuriranje prikaza cjenovnika
def update_price_list():
    data = load_parking_data()
    price_per_hour = data.get("price_per_hour", 0)
    price_per_day = data.get("price_per_day", 0)
    label_price_list.config(text=f"Cijena po satu: {price_per_hour} KM\nCijena po danu: {price_per_day} KM")

# Dodavanje oznake za prikaz cjenovnika
label_price_list = tk.Label(root, text="", bg="#A9CFE8", justify="center")
label_price_list.pack(pady=10)

# Ažuriranje prikaza cjenovnika
update_price_list()


# Dodavanje labela za unos registarskih oznaka
label = tk.Label(root, text="Unesite registarsku oznaku:", bg="#A9CFE8")
label.pack(pady=10)

# Polje za unos registarskih oznaka
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Dugme za potvrdu
button = tk.Button(root, text="Potvrdi", command=handle_input)
button.pack(pady=10)

# Oznaka za prikaz slobodnih mjesta
label_free_spots = tk.Label(root, text="Slobodna mjesta: 0", bg="#A9CFE8")
label_free_spots.pack(pady=10)

# Učitavanje početnih podataka i ažuriranje prikaza
update_free_spots()

# Pokretanje glavne petlje
root.mainloop()
