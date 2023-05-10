import csv
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

"""
------------------------ OPENING THE FILE AND CAPTURING/CLEANING THE DATA ----------------------------------
"""

#Opens up the original call slip data CSV file and a new CSV file to deposit the cleaned up data
raw_slip_data = open("CBHCallSlipData_ArchivalCollections.csv","r")

slip_data_reader = csv.reader(raw_slip_data)

cleaned_slip_data_write = open("Cleaned_CallSlipData.csv", "w", newline='')

slip_data_writer = csv.writer(cleaned_slip_data_write)

#Iterates through the rows in the original CSV file and adds only columns 1-7 to the new CSV file (cleaning it up to remove empty columns at the end)
for row in slip_data_reader:
    if row[0] != "":
        slip_data_writer.writerow(row[0:7])

cleaned_slip_data_write.close()
raw_slip_data.close()


#Opens the newly cleaned call slip data to read it and creates a Dictionary Reader object with the data
#This object is a collection of dictionaries, each one representing a line in the orginial CSV
#The keys are the column headers, while the values are the values in each field of that row
cleaned_slip_data = open("Cleaned_CallSlipData.csv", "r")

slip_data = csv.DictReader(cleaned_slip_data)



"""
------------------------ CALCULATING TOTAL COLLECTION USE ----------------------------------
"""

#Creates empty dictionary and variable to track collection use and appointment dates/days
total_collection_use = {}
appointment_dates = {}
appointment_days = {}
appointment_collections = {}
total_rows = 0

#Iterates through each row of data and counts the frequency of collection titles, as well as appointment dates and days
for row in slip_data:
    total_rows += 1
    title = row["Collection Title"].upper()

    date = row["Appointment Date"]


    if title in total_collection_use:
        total_collection_use[title][0] += 1
    else:
        total_collection_use[title] = [1,0,0,0]

    date_list = date.split("/")
    year = int(date_list[2])

    if year == 2021:
        total_collection_use[title][1] += 1
    elif year == 2022:
        total_collection_use[title][2] += 1
    elif year == 2023:
        total_collection_use[title][3] += 1
    

    if date in appointment_dates:
        appointment_dates[date] += 1
    else:
        appointment_dates[date] =1

    date_object = datetime.strptime(date, '%m/%d/%Y').date()
    weekday = date_object.weekday()

    if weekday in appointment_days:
        appointment_days[weekday] += 1
    else:
        appointment_days[weekday] =1

    if date in appointment_collections:
        if title not in appointment_collections[date]:
            appointment_collections[date].append(title)
    else:
        appointment_collections[date] = [title]

for date in appointment_collections:
    appointment_collections[date] = len(appointment_collections[date])

total_collections = len(total_collection_use)
print("Total Collections Used:",total_collections)
print()

#Creates a new dictionary that includes the data from the total collection use dictionary, but sorted by value
collection_use_sort = sorted(total_collection_use.items(), key=lambda x:x[1], reverse=True)
sorted_collection_use = dict(collection_use_sort)

appointment_dates_sort = sorted(appointment_dates.items(), key=lambda x:x[1], reverse=True)
sorted_appointment_dates = dict(appointment_dates_sort)

#Writes to a CSV file to store total collection use

with open("total_collection_use.csv","w",newline="") as csvout:
    write_csv = csv.writer(csvout)
    write_csv.writerow(["Collection Name","Total Requests","2021 Requests","2022 Requests","2023 Requests"])
    for entry in sorted_collection_use:
        name = entry
        total = sorted_collection_use[entry][0]
        year_21 = sorted_collection_use[entry][1]
        year_22 = sorted_collection_use[entry][2]
        year_23 = sorted_collection_use[entry][3]
        write_csv.writerow([name,total,year_21,year_22,year_23])

#Creates a dictionary to hold the top ten appointment dates
top_appointment_dates = {}
counter3 = 0

for date in sorted_appointment_dates:
    if counter3 <10:
        top_appointment_dates[date] = sorted_appointment_dates[date]
        counter3 +=1



appointment_days_sort = sorted(appointment_days.items(), key=lambda x:x[1], reverse=True)
sorted_appointment_days = dict(appointment_days_sort)

#Writes to a CSV file to store total appointment date data by boxes requested
with open("appointment_dates_boxes.csv","w",newline="") as csvout:
    write_csv = csv.writer(csvout)
    write_csv.writerow(["Date","Total Boxes Requested"])
    for date in appointment_dates:
        write_csv.writerow([date,appointment_dates[date]])

#Writes to a CSV file to store total appointment date data by collections requested
with open("appointment_dates_collections.csv","w",newline="") as csvout:
    write_csv = csv.writer(csvout)
    write_csv.writerow(["Date","Total Collections Requested"])
    for date in appointment_collections:
        write_csv.writerow([date,appointment_collections[date]])
    

#Creating a dictionary to store day of the week stats with actual day of the week as key
sorted_days = {}

for day in sorted_appointment_days:
    if day == 0:
        sorted_days["Monday"] = sorted_appointment_days[day]
    elif day == 1:
        sorted_days["Tuesday"] = sorted_appointment_days[day]
    elif day == 2:
        sorted_days["Wednesday"] = sorted_appointment_days[day]
    elif day == 3:
        sorted_days["Thursday"] = sorted_appointment_days[day]
    elif day == 4:
        sorted_days["Friday"] = sorted_appointment_days[day]
    elif day == 5:
        sorted_days["Saturday"] = sorted_appointment_days[day]
    else:
        sorted_days["Sunday"] = sorted_appointment_days[day]
  

#Writes to a CSV file to store total appointment days of the week data
with open("appointment_days_week.csv","w",newline="") as csvout:
    write_csv = csv.writer(csvout)
    write_csv.writerow(["Day","Total"])
    for day in sorted_days:
        write_csv.writerow([day,sorted_days[day]])

#Creates a dictionary to hold the top ten collections
top_collections = {}
counter = 0
other_collections = 0

for collection in sorted_collection_use:
    if counter <10:
        top_collections[collection] = sorted_collection_use[collection]
        counter +=1
    else:
        other_collections += sorted_collection_use[collection][0]

top_collections["Other"] = other_collections

print("Total Boxes Requested:", total_rows)
print()
print("Boxes Requested on a Given Day:")
print(sorted_days)
print()
print("Top Appointment Dates (by Box Requests):")
print(top_appointment_dates)
print(len(appointment_collections))
print()
print("Top Total Collections:")
print(top_collections)
print()

cleaned_slip_data.close()
"""
------------------------ CALCULATING ADJUSTED COLLECTION USE ----------------------------------
"""
cleaned_slip_data = open("Cleaned_CallSlipData.csv", "r")

slip_data = csv.DictReader(cleaned_slip_data)
#This will calculate how many disctinct days the collection was used.
#This shows the collections that are requested the most per appointment, versus boxes requested.

adjusted_collection_use = {}

for row in slip_data:
    title = row["Collection Title"].upper()

    if title in adjusted_collection_use:
        date = adjusted_collection_use[title][1]
        if row["Appointment Date"] != date:
            adjusted_collection_use[title][0] += 1
            adjusted_collection_use[title][1] = row["Appointment Date"]
    else:
        collection_info = [1,row["Appointment Date"]]
        adjusted_collection_use[title] = collection_info


adjusted_use_sort = sorted(adjusted_collection_use.items(), key=lambda x:x[1], reverse=True)
sorted_adjusted_collection_use = dict(adjusted_use_sort)

for entry in sorted_adjusted_collection_use:
    sorted_adjusted_collection_use[entry] = sorted_adjusted_collection_use[entry][0]
    
#Writes to a CSV file to store adjusted collection use
with open("adjusted_collection_use.csv","w",newline="") as csvout:
    write_csv = csv.writer(csvout)
    write_csv.writerow(["Collection Title","Total Collections Requested"])
    for entry2 in sorted_adjusted_collection_use:
        write_csv.writerow([entry2,sorted_adjusted_collection_use[entry2]])

#Creates a dictionary to hold the top ten collections
top_adjusted_collections = {}
counter2 = 0

for collection in sorted_adjusted_collection_use:
    if counter2 <10:
        top_adjusted_collections[collection] = sorted_adjusted_collection_use[collection]
        counter2 +=1

cleaned_slip_data.close()

print("Top Adjusted Collections:")
print(top_adjusted_collections)














  

