# MIR4 Summon
Simulation of MIR4 gacha summoning system.

#### ➡️ **Selenium Framework** was used to scrape item names and summon rates from MIR4 website.


### ➡️ Setup 
```pip install -r requirements.txt```

```python -m main```


### ❕MIR4 Summon Simulator
This application simulates the gacha system of the game MIR4, using item names and summon chances from the official MIR4 website.

Data is scraped using Selenium and serialized into a JSON file, which can be deserialized to Python objects.


### ❕ Main Menu
- `Summoning Menu` Enter the summoning menu if the data is successfully deserialized. A new menu will be displayed with different types of summons
- `Update Summoning Data` Update the data.json file with the most recent data from the official MIR4 website
- `Display Summoning Data` Print the summoning data on screen, displaying categories, item names and summon rates

<img src="https://raw.githubusercontent.com/xbandrade/mir4-summon/master/img/menu.png" width=30% height=30%>

When choosing the `Skill Tome` summon, an extra menu will be displayed with all available player classes.

Before showing the summon results, the number of summons will also be asked.


<img src="https://raw.githubusercontent.com/xbandrade/mir4-summon/master/img/tome.png" width=40% height=40%>



