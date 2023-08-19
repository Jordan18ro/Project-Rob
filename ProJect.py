import mysql.connector
import os 
import csv
from datetime import datetime
import time
import schedule 
from flask import Flask, render_template, request, redirect, url_for


conn = mysql.connector.connect(host="localhost",user="root",password="Adidas@231988",database="proiect")
cursor=conn.cursor()



app = Flask(__name__)

def create_table():
    conn = mysql.connector('user_database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            ID INTEGER PRIMARY KEY,
            Nume TEXT,
            Prenume TEXT,
            Companie TEXT,
            IdManager INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def register_user(nume, prenume, companie, id_manager):
    conn = mysql.connect('user_database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (Nume, Prenume, Companie, IdManager) VALUES (?, ?, ?, ?)', (nume, prenume, companie, id_manager))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        companie = request.form['companie']
        id_manager = request.form['id_manager']
        
        register_user(nume, prenume, companie, id_manager)
        return redirect(url_for('register'))
    return render_template('register.html')




director_intrari = "intrari "
angajati = {
    1:"Mihai Badea",
    2:"Andrei Ciobanu",
    3:"Marius Galca",
    4:"Armand  Santos",
}
   


def procesare_fisier_intrare(director_intrari,Poarta1):
    try:
        with open(f"Poarta1", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                id_angajat = int(row[0])
                ora_validarii = datetime.strptime(row[1])
                sens = row[2]

                if id_angajat in angajati:
                    angajat = angajat(id_angajat, angajati[id_angajat])
                    if sens == "intrare":
                        angajat.intrare(ora_validarii)
                    elif sens == "iesire":
                        angajat.iesire(ora_validarii)
                else:
                    print(f"ID-ul angajatului {id_angajat} nu există în baza de date.")

        print(f"Fișierul {Poarta1} a fost procesat.")
    except FileNotFoundError:
        print(f"Fișierul nu există: {Poarta1}")

def monitorizare_intrari():
    while True:
        fisiere_noi = [fisier for fisier in os.listdir(director_intrari) if fisier.endswith(".csv")]
        for fisier in fisiere_noi:
            procesare_fisier_intrare(fisier)

class Angajatii:
    def __init__(self,ID,nume):
        self.ID = ID
        self.nume = nume
        self.ore_lucrate = 0 
        self.ultima_intrare = None 


def log_hours(employee_name, entry_time, exit_time):
    with open('Poarta2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([employee_name, entry_time, exit_time])

def calculate_daily_hours():
    today = datetime.date.today()
    eight_hours = datetime.timedelta(hours=8)
    
    with open('Poarta2.csv', mode='r') as file:
        reader = csv.reader(file)
        employees = {}
        for row in reader:
            employee_name, entry_time_str, exit_time_str = row
            entry_time = datetime.datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S.%f')
            exit_time = datetime.datetime.strptime(exit_time_str, '%Y-%m-%d %H:%M:%S.%f')
            
            if entry_time.date() == today:
                if employee_name not in employees:
                    employees[employee_name] = datetime.timedelta()
                worked_hours = exit_time - entry_time
                employees[employee_name] += worked_hours
    
    for employee, hours_worked in employees.items():
        if hours_worked < eight_hours:
            print(f"{employee} nu a lucrat suficiente ore ({hours_worked.total_seconds() / 3600} ore)")

def main():
    
    schedule.every().day.at("20:00").do(calculate_daily_hours)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    monitorizare_intrari()
    main()
    create_table()
    app.run(debug=True)
   