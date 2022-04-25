import csv
import os.path
from os import path
import mongo_api

def insert_msg(email, flight, msg):
    # print("Checking if 'messages.csv' exists...")
    if path.exists('csv\\messages.csv'):
    #     print("Opening 'messages.csv'...")
        csv_file = open('csv\\messages.csv', 'a', newline = '')
    else:
    #     print("File does not exist...\nCreating 'messages.csv'...")
        # print("Opening 'messages.csv'...")
        csv_file = open('csv\\messages.csv', 'w', newline = '')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["email", "flight","message"])

    csv_writer = csv.writer(csv_file)
    if(email!="" and flight!="" and msg!=""):
        csv_writer.writerow([email ,flight,  msg])
        query = {
            'email': email,
            'flight' : flight,
            'msg' : msg,
        }
        mongo_api.Complaint.insert_one(query)
    csv_file.close()