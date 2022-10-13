import csv
# import numpy as np
# import matplotlib.pyplot as plt
import mysql.connector

cnx = mysql.connector.connect(user='root', database='mothbase2', password='123(sql)')
cursor = cnx.cursor()


def readMyCsv(fileName):
    # with open(fileName, encoding='cp1251') as file:
    with open(fileName) as file:
        reader = csv.reader(file)
        for row in reader:
            vegetation = row[1].split(',')
            spVeg = []
            idVeg = []
            spVeg.append(row[0])
            idVeg.append(row[0])
            for veg in vegetation:
                veg = veg.strip()
                spVeg.append(veg)
                vegId = getIdVeg(veg)
                if vegId:
                    idVeg.append(vegId)
                else:
                    print("not found {}".format(veg))
            print(idVeg)

def getIdVeg(veg):
    query = 'SELECT vegetation_id FROM vegetation WHERE rus_name LIKE %s'
    cursor.execute(query, (veg,))
    vegId = cursor.fetchall()
    if vegId:
        return vegId
    else:
        return None


def main():
    file = "/Users/asya/science/Database/prepared/Processed/vegetation_id_csv_to_proc/vegIdProc.csv"
    # file = "/Users/asya/science/Database/Digital Data conference/1654139556-occur.csv"
    readMyCsv(file)
    # veg = "жимолость"
    # print(getIdVeg(veg))

main()