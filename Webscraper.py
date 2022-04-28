# Webscraper to get the list of enemy names on tibia.fandom.com
import requests
from bs4 import BeautifulSoup
import time
from Creature_data import Creature

# TODO: Make this function return the list of creature names
def list_of_creatures_names():
  tick = time.perf_counter()

  URL = "https://tibia.fandom.com/wiki/List_of_Creatures"

  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="mw-content-text")

  html_enemy_names = results.find_all("tr")

  enemy_names_list = []

  for html_enemy in html_enemy_names:
    for td in html_enemy.find_all('td'):
      actual_enemy_name = td.get_text()
      actual_enemy_name.strip()
      enemy_names_list.append(actual_enemy_name)
      break # Break since we are taking first object only (Name) and then returning

  print(len(enemy_names_list))

  tock = time.perf_counter()

  elapsed_time = tock - tick
  print(elapsed_time)


def get_creature_data(creature_name):
  URL = f"https://tibia.fandom.com/wiki/{creature_name}"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(class_="portable-infobox")
  enemy_attributes = results.findAll("div", "pi-item")

  creature_attributes_list = []

  ################ GET ALL DATA EXCEPT RESISTANCE & LOOT FOR CREATURE ################
  for attribute in enemy_attributes:
    creature_attribute = attribute.get_text()
    creature_attribute = creature_attribute.strip()
    creature_attributes_list.append(creature_attribute)

  not_needed_attributes = ["Classification", "Spawn Type", "Class", "Walks Around", "Version", "Status", "Charm Points"]
  final_creature_dict = {}

  for x in creature_attributes_list:
    if("\n" in x):
      data = x.split("\n")
      if(data[1] == '✓'):
        data[1] = "Yes"
      elif(data[1] == '✗'):
        data[1] = "No"
      elif(data[0] in not_needed_attributes):
        creature_attributes_list.remove(x)
        continue
      final_creature_dict[data[0]] = data[1] # Adding new {key : value} pair to dict 
      #print(f"Creature data:  {data[0]} - {data[1]}")
    else:
      #print(f"removing {x} since it didnt have backslash n")
      creature_attributes_list.remove(x)

  # Clean max dmg numbers
  if('?' in final_creature_dict.get("Est. Max Dmg")):
    max_dmg = final_creature_dict.get("Est. Max Dmg").split('?')
    final_creature_dict["Est. Max Dmg"] = max_dmg[0]
  elif(len(final_creature_dict.get("Est. Max Dmg")) > 6):
    final_creature_dict["Est. Max Dmg"] = final_creature_dict.get("Est. Max Dmg").split(" ")[0]
  ################ CREATE CREATURE OBJECT ################
  new_creature = Creature(
    creature_name,
    final_creature_dict.get("Health"),
    final_creature_dict.get("Experience"),
    final_creature_dict.get("Speed"),
    final_creature_dict.get("Armor"),
    final_creature_dict.get("Est. Max Dmg"),
    final_creature_dict.get("Summon"),
    final_creature_dict.get("Convince"),
    final_creature_dict.get("Illusionable"),
    final_creature_dict.get("Pushable"),
    final_creature_dict.get("Pushes"),
    final_creature_dict.get("Kills to Unlock"),
    final_creature_dict.get("Sense Invis"),
    None, None, None, None, None, None, None, None
  )

  ################ GET RESISTANCE FOR CREATURE ################
  results = soup.find("div", {"id": "creature-resistance-d"}) # Find div by id
  for resistance in results:
    data = resistance.get_text()
    data = data.strip()
    data = data.split(" ")
    # Clean prysical resistance numbers
    if(len(data) > 1):
      test_data_1 = data[1].split("%")
      test_data_1[0] += "%"
    if(data[0] == "Physical"): new_creature.dmgfromphysical = test_data_1[0]
    elif(data[0] == "Death"): new_creature.dmgfromdeath = test_data_1[0]
    elif(data[0] == "Holy"): new_creature.dmgfromholy = test_data_1[0]
    elif(data[0] == "Ice"): new_creature.dmgfromice = test_data_1[0]
    elif(data[0] == "Fire"): new_creature.dmgfromfire = test_data_1[0]
    elif(data[0] == "Energy"): new_creature.dmgfromenergy = test_data_1[0]
    elif(data[0] == "Earth"): new_creature.dmgfromearth = test_data_1[0]
    else: continue #print("This is what went wrong with the data: ", data)

  ################ GET LOOT LIST FROM CREATURE ################
  results = soup.find("div", {"id": "loot_perc_loot"}) # Find div by id
  loot_list = []
  loot_list = results.get_text().split("\n")
  new_creature.listofloot = loot_list
  #print("loot_list:", loot_list)

  print(vars(new_creature))

## HERE WE TEST RUN THE CODE
get_creature_data("Amazon")