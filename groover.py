# Version 1.0

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import json
import re

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Asetuksia ei löytynyt, luodaan uusi tiedosto.")
        return {"timingVariation": 5,
                "swingAmount": 0.1,
                "handedness": "right",
                "handStrenght": 10,
                "velocityVariation": 10,
                "maxVelocity": 115,
                "minVelocity": 90,
                "useHandednessFeature": False
                }

def loadPreset(preset_name):
            
            try:
                with open('preset.json', 'r') as f:
                    data = json.load(f)
                    return data["presets"][preset_name]
            except (FileNotFoundError, KeyError):
                print("Asetuksia ei löytynyt")
                return {"timingVariation": 5,
                        "swingAmount": 0.1,
                        "handedness": "right",
                        "handStrenght": 10,
                        "velocityVariation": 10,
                        "maxVelocity": 115,
                        "minVelocity": 90,
                        "useHandednessFeature": False
                        }

def update_ui(settings):
    minVelocity_scale.set(settings["minVelocity"])
    maxVelocity_scale.set(settings["maxVelocity"])
    velocityVariation_scale.set(settings["velocityVariation"])
    timingVariation_scale.set(settings["timingVariation"])
    swingAmount_scale.set(settings["swingAmount"])
    handedness_var.set(settings["handedness"])
    handStrenght_scale.set(settings["handStrenght"])
    use_handedness_feature.set(settings["useHandednessFeature"])

def saveSettingsAndRunScript(settings, root):
    # Lue asetukset käyttöliittymästä
    try:
        timingVariation = int(timingVariation_scale.get())
        swingAmount = float(swingAmount_scale.get())
        handedness = str(handedness_var.get())
        handStrenght = int(handStrenght_scale.get())
        velocityVariation = int(velocityVariation_scale.get())
        maxVelocity = int(maxVelocity_scale.get())
        minVelocity = int(minVelocity_scale.get())
        useHandednessFeature = use_handedness_feature.get()
    except ValueError:
        print("Väärin meni")
        return
    
    # Tallenna asetukset JSON-tiedostoon
    with open('settings.json', 'w') as f:
        json.dump({"timingVariation": timingVariation,
                   "swingAmount": swingAmount,
                   "handedness": handedness,
                   "handStrenght": handStrenght,
                   "velocityVariation": velocityVariation,
                   "maxVelocity": maxVelocity,
                   "minVelocity": minVelocity,
                   "useHandednessFeature": useHandednessFeature
                   }, f)
        
    # Luodaan päivitetty sanakirja:
    newSettings = {
        "timingVariation": int(timingVariation_scale.get()),
        "swingAmount": float(swingAmount_scale.get()),
        "handedness": str(handedness_var.get()),
        "handStrenght": int(handStrenght_scale.get()),
        "velocityVariation": int(velocityVariation_scale.get()),
        "maxVelocity": int(maxVelocity_scale.get()),
        "minVelocity": int(minVelocity_scale.get()),
        "useHandednessFeature": use_handedness_feature.get()
    }

    # Tallennetaan ominaisuudet Lua skriptiin
    try:
        with open('groover.lua', 'r') as f:
            # Tallennetaan olemassa oleva skripti
            existing_lua_code = f.read()

        # Käydään settings Sanakirja läpi
        for setting, value in newSettings.items():
            
            # Lisätään heittomerkit handedness muuttujan arvolle
            if setting == "handedness":
                existing_lua_code = re.sub(rf"local {setting} = .*$", f"local {setting} = \"{value}\"", existing_lua_code, flags=re.MULTILINE)
                print(f"Muutettu: {setting} {value}")
            else:
                existing_lua_code = re.sub(rf"local {setting} = .*$", f"local {setting} = {value}", existing_lua_code, flags=re.MULTILINE)
                print(f"Muutettu: {setting} {value}")

        # Kirjoitetaan Koodi tiedostoon
        with open('groover.lua', 'w') as f:
            f.write(existing_lua_code)

    except FileNotFoundError:
        print("Tiedostoa 'groover.lua' ei löydy tai siihen ei ole lukuoikeuksia.")
    except PermissionError:
        print("Sinulla ei ole oikeuksia kirjoittaa tiedostoon 'groover.lua'.")
    except Exception as e:
        print(f"Asetuksien tallennus epäonnistui: {e}")
        tk.messagebox.showerror("Virhe", "Asetuksien tallennus epäonnistui. Tarkista asetukset ja yritä uudelleen.")

# Lataa asennukset ennen käyttöliittymän luontia
settings = load_settings()

root = tk.Tk()
root.title("Groover 1.1")

#Käyttöliittymä elementit
separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

# Alasvetovalikko preseteille
preset_label = tk.Label(root, text="Preset:", font=("Arial", 11))
preset_label.pack(pady=(20, 0))
preset_var = tk.StringVar(root)
preset_options = ["Kick", "Snare", "Hihat/Ride", "Toms", "Crash"]
preset_var.set("Valitse preset...")
preset_dropdown = ttk.Combobox(root, textvariable=preset_var, values=preset_options, state='enabled')
# Määritetään funktio, joka kutsutaan, kun valinta muuttuu
preset_dropdown.bind('<<ComboboxSelected>>', lambda event: update_ui(loadPreset(preset_var.get())))
preset_dropdown.pack(pady=(0, 20))

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

minVelocity_label = tk.Label(root, text="Min Velocity:", font=("Arial", 11))
minVelocity_label.pack(pady=(20, 0))
minVelocity_scale = tk.Scale(root, from_=0, to=127, orient=tk.HORIZONTAL, resolution=1)
minVelocity_scale.set(settings["minVelocity"])
minVelocity_scale.pack(fill="x", expand=True, padx=50 )

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

maxVelocity_label = tk.Label(root, text="Max Velocity:", font=("Arial", 11))
maxVelocity_label.pack(pady=(20, 0))
maxVelocity_scale = tk.Scale(root, from_=0, to=127, orient=tk.HORIZONTAL, resolution=1)
maxVelocity_scale.set(settings["maxVelocity"])
maxVelocity_scale.pack(fill="x", expand=True, padx=50 )

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

velocityVariation_label = tk.Label(root, text="Velocity Variation:", font=("Arial", 11))
velocityVariation_label.pack(pady=(20, 0))
velocityVariation_scale = tk.Scale(root, from_=0, to=127, orient=tk.HORIZONTAL, resolution=1)
velocityVariation_scale.set(settings["velocityVariation"])
velocityVariation_scale.pack(fill="x", expand=True, padx=50 )

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

timingVariation_label = tk.Label(root, text="Timing Variation:", font=("Arial", 11))
timingVariation_label.pack(pady=(20, 0))
timingVariation_scale = tk.Scale(root, from_=0, to=127, orient=tk.HORIZONTAL, resolution=1)
timingVariation_scale.set(settings["timingVariation"])
timingVariation_scale.pack(fill="x", expand=True, padx=50 )

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

swingAmount_label = tk.Label(root, text="Swing Amount:", font=("Arial", 11))
swingAmount_label.pack(pady=(20, 0))
swingAmount_scale = tk.Scale(root, from_=0.0, to=1.0, orient=tk.HORIZONTAL, resolution=0.1)
swingAmount_scale.set(settings["swingAmount"])
swingAmount_scale.pack(fill="x", expand=True, padx=50 )

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

use_handedness_feature = tk.BooleanVar()

checkbutton = tk.Checkbutton(root, text="Katisyys on/off", variable=use_handedness_feature, 
                             onvalue=True, offvalue=False, 
                             command=lambda: toggle_feature(), font=("Arial", 11))
checkbutton.pack(pady=(20, 0))

def toggle_feature():
    global settings
    #print(settings)
    settings["useHandednessFeature"] = use_handedness_feature.get()
    #print(settings)
    # Päivitetään Alasvetovalikon Tila
    #handedness_dropdown.state(["readonly"] if use_handedness_feature.get() else ["disabled"])
    current_state = handedness_dropdown.state()
    if settings["useHandednessFeature"] == True:
        new_state = "readonly"
    else:
        new_state = "disabled"

     # Tulostetaan muutokset
    #print(f"Muutetaan valikon tila '{current_state}' -> '{new_state}'")

    handedness_dropdown.config(state=new_state)

    # Tulostetaan uusi tila vielä kerran varmistukseksi
    #print(f"Uusi valikon tila: {handedness_dropdown.state()}")

def update_handedness(*args):
    global settings
    settings["handedness"] = handedness_var.get()
    #print(f"Kätisyys päivitetty: {settings['handedness']}")


# Alasvetovalikko kätisyydelle
handedness_label = tk.Label(root, text="Katisyys:", font=("Arial", 11))
handedness_label.pack(pady=(20, 0))
handedness_var = tk.StringVar(root)
handedness_var.trace_add("write", update_handedness)
handedness_options = ["right", "left"]
handedness_dropdown = ttk.Combobox(root, textvariable=handedness_var, values=handedness_options, state='disabled')
handedness_dropdown.pack(pady=(0, 20))

if "handedness" in settings:
    handedness_var.set(settings["handedness"])

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

handStrenght_label = tk.Label(root, text="Hand Strenght:", font=("Arial", 11))
handStrenght_label.pack(pady=(20, 0))
handStrenght_scale = tk.Scale(root, from_=0, to=127, orient=tk.HORIZONTAL)
handStrenght_scale.set(settings["handStrenght"])
handStrenght_scale.pack(fill="x", expand=True, padx=50)

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill="x", padx=20)

# Nappula, joka kutsuu saveSettingsAndRunScript-funktion
save_button = tk.Button(root, text="Tallenna", font=("Arial", 11), command=lambda: saveSettingsAndRunScript(settings, root))
save_button.pack(pady=20)

# Aseta geometria ja näytä ikkuna
root.geometry("400x900")
root.mainloop()