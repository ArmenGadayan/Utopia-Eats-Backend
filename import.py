import pandas as pd
import mysql.connector

from config import databasePass

restaurants = ['Qdoba', "Applebee's", 'Red Lobster', 'Red Robin', "Romano's Macaroni Grill",
'Round Table Pizza', 'Ruby Tuesday', 'Sbarro', 'Sheetz', 'Sonic', 'Starbucks',
'Dairy Queen', "Steak 'N Shake", 'Subway', "TGI Friday's", 'Taco Bell',
'Tim Hortons', "Arby's", 'Whataburger', 'Wawa', "Wendy's",'White Castle',
'Wingstop', 'Yard House', "Checker's Drive-In/Rallys", 'Baskin Robbins',
"Carl's Jr.", 'Del Taco', 'Einstein Bros. Bagels', "Hardee's", 'Bob Evans',
"Jason's Deli", 'Burger King', 'Boston Market',
"BJ's Restaurant & Brewhouse", 'Chick-Fil-A', 'Krispy Kreme',
"Church's Chicken", 'IHOP', "Long John Silver's", 'Bojangles',
'El Pollo Loco', "Friendly's", 'KFC', 'Hooters', '7 Eleven', 'Jamba Juice',
"McDonald's", 'California Pizza Kitchen', "Dunkin' Donuts", "Culver's",
'Bonefish Grill', "Captain D's", "Carrabba's Italian Grill",
'The Capital Grille', 'Jack in the Box', "Auntie Anne's", "Ci Ci's Pizza",
"Denny's", 'Popeyes', "Famous Dave's", "Joe's Crab Shack", 'Krystal',
"McAlister's Deli", "O'Charley's", 'Olive Garden', 'Outback Steakhouse',
'Panda Express', "Papa Murphy's", "PF Chang's", "Zaxby's", 'Quiznos',
"Jersey Mike's Subs", 'Chipotle Mexican Grill', 'Chuck E. Cheese', 'Dominos',
'Firehouse Subs', 'Five Guys', 'LongHorn Steakhouse', "Chili's",
'On the Border', 'Pizza Hut', "Papa John's", "Frisch's Big Boy",
'Golden Corral', 'Panera Bread', 'Perkins', 'Noodles & Company',
"Casey's General Store", "Moe's Southwest Grill", 'In-N-Out Burger',
"Jimmy John's", 'Little Caesars', "Marco's Pizza", "Dickey's Barbeque Pit",
'Potbelly Sandwich Shop']

# Read data from CSV and make some edits
data = pd.read_csv("dataset.csv", usecols=["Food_Category", "Restaurant", "Item_Name", "Calories", "Total_Fat", "Saturated_Fat", "Trans_Fat", "Cholesterol", "Sodium", "Carbohydrates", "Protein", "Sugar", "Dietary_Fiber"])
data.loc[data["Restaurant"] == "Chipotle", "Restaurant"] = "Chipotle Mexican Grill"
data.loc[data["Restaurant"] == "Einstein Bros", "Restaurant"] = "Einstein Bros. Bagels"
data = data[["Food_Category", "Restaurant", "Item_Name", "Calories", "Total_Fat", "Saturated_Fat", "Trans_Fat", "Cholesterol", "Sodium", "Carbohydrates", "Protein", "Sugar", "Dietary_Fiber"]]
data = data.drop_duplicates().dropna()

# Connect to database
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd =databasePass,
  database = "utopian_eats"
)
cursor = dataBase.cursor()
  
# Clear tables
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE api_item")
cursor.execute("TRUNCATE TABLE api_restaurant")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Insert restaurants into restaurants table
sql = "INSERT INTO api_restaurant (restaurant_name) VALUES (%s)"
vals = [(r,) for r in restaurants]
cursor.executemany(sql, vals)

# Insert food items into items table
sql = "INSERT INTO api_item (Food_Category, Item_Name, Calories, Total_Fat, Saturated_Fat, Trans_Fat, Cholesterol, Sodium, Carbohydrates, Protein, Sugar, Dietary_Fiber, restaurant_id)\
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
for i in range(len(data.index)):
    row = data.iloc[i].values.tolist()
    row.append(restaurants.index(row[1])+1)
    row.pop(1)
    cursor.execute(sql, tuple(row))

dataBase.commit()
dataBase.close()