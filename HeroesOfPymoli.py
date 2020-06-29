#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Items priced less than 3.00 dollars are significantly less likley to sell than more expensive items. The sellers might be excellent in estimating the value of their items or perhaps the game itself exploits psychological mechanics to entice players to spend more money. Interesting, nonetheless.
# 
# * The highest spenders (on average) are in the age range 35-39 with an average player spending 4.76 dollars, followed by players younger than 10 years old with players spending an average of 4.53 dollars. Perhaps there is a correlation between families with members in each group and average spending per family member.
# 
# * There are more purchases than members for each age group. The age range 20-24 has the highest purchase to player ratio with the total number of purchases being 141 per/100 of the player count. The second highest being players within the range 30-34 with 140 per/100. These two age groups might be the most susceptible to prior marketing and psychological techniques, or they have stronger relationships to the game.

# In[1]:


import pandas as pd
import numpy as np

file_to_load = "Resources/purchase_data.csv"

purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[2]:


player_count = purchase_data.SN.nunique()
player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


item_num = purchase_data["Item ID"].nunique()
avg_price = purchase_data["Price"].mean()
total_purchases = purchase_data["Purchase ID"].count()
net = purchase_data["Price"].sum()
summary = pd.DataFrame({"Number of Items":[item_num],
                       "Average Price":[avg_price],
                       "Total Purchases":[total_purchases],
                       "Revenue":[net]})
summary


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


males = purchase_data[purchase_data['Gender'].isin(['Male'])]
females = purchase_data[purchase_data['Gender'].isin(['Female'])]
others = purchase_data[purchase_data['Gender'].isin(["Other / Non-Disclosed"])]

male = males.SN.nunique()
female = females.SN.nunique()
other = others.SN.nunique()

gender_demo_raw = pd.DataFrame({"Gender":["Male", "Female", "Other / Non-Disclosed"],
                   "Purchase Count":[male, female, other],
                   "Percentage":[round(male/player_count*100, 2), round(female/player_count*100,2), round(other/player_count*100,2)]
                  })

gender_demo = gender_demo_raw.style.format({
    'var1': '{:,.2f}'.format,
    'var2': '{:,.2f}'.format,
    'var3': '{:,.2%}'.format,
})

gender_demo


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


genders = ["Male","Female","Other / Non-Disclosed"]
total_spent = [males["Price"].sum(), females["Price"].sum(), others["Price"].sum()]
avg_spent = [males["Price"].mean(), females["Price"].mean(), others["Price"].mean()]
avg_spent_per_person = [males["Price"].sum()/male, females["Price"].sum()/female, others["Price"].sum()/other]

gender_summary = pd.DataFrame({"Gender":genders,
    "Purchase Count":[males["Purchase ID"].count(), females["Purchase ID"].count(), others["Purchase ID"].count()],
                               "Average Spent":avg_spent,
                               "Total Spent":total_spent,
                               "Average Spent Per Person":avg_spent_per_person})
gender_summary


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[6]:


bins = [0,9,14,19,24,29,34,39,100]
labels = ["<10", "10-14","15-19","20-24","25-29","30-34","35-39","40+"]


purchase_data2 = purchase_data.copy(deep="True")
purchase_data3 = purchase_data2.drop_duplicates(subset="SN",keep="first")
purchase_data3["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)


age_group = purchase_data3.groupby("Age Group")
age = age_group["Age"].count()
age_per = age/player_count*100
age_group_pd = pd.DataFrame({"total":age,"per":age_per})
age_group_pd


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


purchase_data4 = purchase_data.copy(deep="True")
purchase_data4["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=labels)

age_group2 = purchase_data4.groupby("Age Group")

purchase_count2 = age_group2["Purchase ID"].count()
avg_spent2 = age_group2["Price"].mean()
total_spent2 = age_group2["Price"].sum()
avg_spent_per_person2 = total_spent2/age

age_summary = pd.DataFrame({"Purchase Count":purchase_count2,
                               "Average Spent":avg_spent2,
                               "Total Spent":total_spent2,
                               "Average Spent Per Person":avg_spent_per_person2})
age_summary


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[8]:


spenders = purchase_data.groupby("SN")

purchase_count = spenders["SN"].count()
avg_value = spenders["Price"].mean()
total_value = spenders["Price"].sum()

spenders_summary = pd.DataFrame({"Purchase Count":purchase_count,
                                "Average Purchase Price": avg_value,
                                "Total Purchase Value":total_value})


spenders_summary.sort_values(by="Total Purchase Value", ascending=False).head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:


items_df = purchase_data[["Item ID","Item Name", "Price"]].copy()
items = items_df.groupby(["Item ID","Item Name"])

num_sold = items["Item Name"].count()
price = items["Price"].max()
value_sold = items["Price"].sum()

items_summary = pd.DataFrame({"Purchase Count":num_sold,
                            "Item Price":price,
                             "Total Purchase Value":value_sold})
items_df
items_summary.sort_values(by="Purchase Count", ascending=False).head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[10]:


items_summary.sort_values(by="Total Purchase Value", ascending=False).head()
