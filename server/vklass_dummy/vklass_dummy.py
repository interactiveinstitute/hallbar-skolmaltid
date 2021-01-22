# 
# Runs a flask server for emulating vklass endpoints, generating dummy
# data for the current day upon call.
# Currently built to be called every day, where if it's after a certain
# time in the morning, absence is added
# Will use environment variables if found:
#    - MAX_DAILY_ADDED_ABSENCES
#    - MORNING_UPDATE_HOUR
#    - LATE_MORNING_UPDATE_HOUR
# Otherwise, these can be changed dynamically through a config endpoint

import logging, sys, os
import time
from datetime import datetime, timedelta
import urllib.request as request
import json
import random
# ----------------------------------------
from flask import Flask
from flask import request as flask_request, redirect
# ----------------------------------------


logger = logging.getLogger('vklass_dummy')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
max_daily_added_absences = int(os.environ['MAX_DAILY_ADDED_ABSENCES']) if 'MAX_DAILY_ADDED_ABSENCES' in os.environ else 50
morning_update_hour      = int(os.environ['MORNING_UPDATE_HOUR']) if 'MORNING_UPDATE_HOUR' in os.environ else 8
late_morning_update_hour = int(os.environ['LATE_MORNING_UPDATE_HOUR']) if 'LATE_MORNING_UPDATE_HOUR' in os.environ else 8
schools = {
    "schoolidCollection":[
        {
            "schoolid":1,
            "schoolname":"Söderskolan",
            "schooltype":0,
            "studentcount":500,
            "personalcount":50
        },
        {
            "schoolid":2,
            "schoolname":"Västerskolan",
            "schooltype":0,
            "studentcount":1000,
            "personalcount":100
        }
    ]
}
todaysAbsence = {'absenceidCollection':[]}
last_call = datetime.now() - timedelta(days=1)
# names from Swedish baby name top list 2019:
first_names = ["Lucas", "Liam", "William", "Elias", "Noah", "Hugo", "Oliver", "Oscar", "Adam", "Matteo", "Walter", "Alexander", "Leo", "Nils", "Alfred", "Ludvig", "Adrian", "Theo", "Leon", "Elliot", "Arvid", "Vincent", "Theodor", "Filip", "Axel", "Harry", "Frans", "Charlie", "Mohamed", "Gabriel", "Isak", "August", "Loui", "Benjamin", "Sam", "Josef", "Ebbe", "Melvin", "Love", "Olle", "Albin", "Henry", "Edvin", "Elton", "Emil", "Malte", "Vidar", "Gustav", "Jack", "Frank", "Viggo", "Noel", "Sixten", "Viktor", "Melker", "Jacob", "Casper", "Erik", "Tage", "Aron", "Loke", "Otto", "Wilmer", "Colin", "Milo", "Sigge", "Alvin", "Carl", "Milton", "Wilhelm", "Anton", "Ivar", "Kian", "Julian", "Max", "Elis", "Levi", "Nicholas", "Elvin", "Felix", "Vilgot", "Ali", "Omar", "Hjalmar", "Ture", "Samuel", "David", "Kevin", "Joel", "Vide", "Amir", "Ville", "Dante", "John", "Daniel", "Algot", "Folke", "Alve", "Ibrahim", "Thor",\
"Alice", "Olivia", "Astrid", "Maja", "Vera", "Ebba", "Ella", "Wilma", "Alma", "Lilly", "Elsa", "Agnes", "Freja", "Saga", "Ellie", "Clara", "Signe", "Alva", "Alicia", "20 Selma", "Ester", "Stella", "Julia", "Ines", "Leah", "Ellen", "Molly", "Iris", "Sara", "Luna", "Isabelle", "Nora", "Nova", "Hedda", "Mila", "Nellie", "Sofia", "Lova", "Juni", "Elvira", "Linnéa", "Emilia", "Sigrid", "Celine", "Elise", "Edith", "Emma", "Lykke", "Liv", "Lo", "Thea", "Mejas", "Livia", "Tuva", "Isabella", "Sally", "Majken", "Maria", "Leia", "Hailey", "Tyra", "Elin", "Amelia", "Lovisa", "Märta", "Rut", "Ida", "Ingrid", "Bianca", "Hanna", "Ronja", "Jasmine", "Stina", "Svea", "Cleo", "Melissa", "Hilma", "Filippa", "Hedvig", "Julie", "Tilde", "Lovis", "Siri", "Felicia", "Cornelia", "Elina", "Elsie", "Joline", "Hilda", "Mira", "Moa", "Melina", "Bonnie", "Mariam", "Matilda", "Wilda", "Bella", "Millie", "My", "Amanda"]
last_names = ["Andersson", "Johansson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Persson", "Svensson", "Gustafsson", "Pettersson", "Jonsson", "Jansson", "Hansson", "Bengtsson", "Jönsson", "Lindberg", "Jakobsson", "Magnusson", "Olofsson", "Lindström", "Lindqvist", "Lindgren", "Axelsson", "Berg", "Bergström", "Lundberg", "Lind", "Lundgren", "Lundqvist", "Mattsson", "Berglund", "Fredriksson", "Sandberg", "Henriksson", "Forsberg", "Sjöberg", "Wallin", "Ali", "Engström", "Mohamed", "Eklund", "Danielsson", "Lundin", "Håkansson", "Björk", "Bergman", "Gunnarsson", "Holm", "Wikström", "Samuelsson", "Isaksson", "Fransson", "Bergqvist", "Nyström", "Holmberg", "Arvidsson", "Löfgren", "Söderberg", "Nyberg", "Blomqvist", "Claesson", "Nordström", "Mårtensson", "Lundström", "Ahmed", "Viklund", "Björklund", "Eliasson", "Pålsson", "Hassan", "Berggren", "Sandström", "Lund", "Nordin", "Ström", "Åberg", "Hermansson", "Ekström", "Falk", "Holmgren", "Dahlberg", "Hellström", "Hedlund", "Sundberg", "Sjögren", "Ek", "Blom", "Abrahamsson", "Martinsson", "Öberg", "Andreasson", "Strömberg", "Månsson", "Åkesson", "Hansen", "Norberg", "Lindholm", "Dahl", "Jonasson"]


# ----------------------------------------


# https://export.vklass.net/output.ashx output example:
# {
#     "absenceidCollection": [
#         {
#             "absenceid": 14626867,
#             "usersocialnumber": "121003-TF01",
#             "userfirstname": "Nova",
#             "userlastname": "Demoelev",
#             "startdate": "2020-03-02T00:00:00",
#             "enddate": "2020-03-27T23:59:00",
#             "absenceid": 14626867,
#             "created": "2020-02-17T14:48:30.243",
#             "updated": "2020-02-17T14:48:30.243"
#         },
#         ...
#         }
#     ]
# }

def remove_absence_before_today():
    global todaysAbsence
    past_midnight_str = datetime.now().strftime("%Y-%m-%dT00:00:00")
    todaysAbsence['absenceidCollection'] = [a for a in todaysAbsence['absenceidCollection'] if not (a['enddate'] < past_midnight_str)]
    logger.debug("   " + str(len(todaysAbsence['absenceidCollection'])) + " absences left from previous day")

def add_absences_today(portion_now, ):
    global todaysAbsence
    global max_daily_added_absences
    for ix in range(random.randint(0, int(portion_now*max_daily_added_absences))):
        absence = {}
        absence["absenceid"]        = str(random.randrange(100000, 100000000))
        absence["usersocialnumber"] = str(random.randrange(100000, 1000000)) + "-" + str(random.randrange(1000, 10000))
        absence["userfirstname"] = first_names[random.randrange(len(first_names))]
        absence["userlastname"]  =  last_names[random.randrange(len(last_names))]
        absence["created"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])
        absence["updated"] = absence["created"]
        length_rand = random.random()
        if length_rand < 0.03:
            # 1 week
            absence["startdate"] = datetime.now().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            absence["enddate"]   = (datetime.now() + timedelta(days=6)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")
            logger.debug("add absence #" + str(ix) + ": 7 days")
        elif length_rand < 0.10:
            # 3 days
            absence["startdate"] = datetime.now().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            absence["enddate"]   = (datetime.now() + timedelta(days=2)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")
            logger.debug("add absence #" + str(ix) + ": 3 days")
        else:
            # few hours
            hours_rand = random.random()
            if hours_rand < 0.07:
                num_hours = 4
            elif hours_rand < 0.21:
                num_hours = 3
            elif hours_rand < 0.49:
                num_hours = 2
            else:
                num_hours = 1
            start_hour = random.randint(8, 16-num_hours)
            absence["startdate"] = datetime.now().replace(hour=start_hour,   minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            absence["enddate"]   = datetime.now().replace(hour=start_hour+num_hours, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            logger.debug("add absence #" + str(ix) + ": " + str(num_hours) + " hour")
        
        todaysAbsence['absenceidCollection'].append(absence)

def update_vklass_absences_today():
    global todaysAbsence
    global last_call
    global morning_update_hour
    global late_morning_update_hour
    morning_update      = datetime.now().replace(hour=morning_update_hour,      minute=0, second=0)
    late_morning_update = datetime.now().replace(hour=late_morning_update_hour, minute=0, second=0)
    if last_call < morning_update:
        logger.debug("BEFORE MORNING UPDATE! Cleanup ...")
        remove_absence_before_today()
    if last_call < morning_update and datetime.now() >= morning_update:
        logger.debug("MORNING UPDATE!")
        add_absences_today(0.9)
        last_call = datetime.now()
    if last_call < late_morning_update and datetime.now() >= late_morning_update:
        logger.debug("LATE MORNING UPDATE!")
        add_absences_today(0.1)
        last_call = datetime.now()

# ----------------------------------------


@app.route('/')
def index():
    return "<h1>Vklass emulator</h1>\
        <p>\
        Emulator to generate dummy vklass absence json answers.\
        </p>\
        <h2>Available endpoints:</h2>\
        <ul>\
            <li><a href='/export_vklass_net/absence'>/export_vklass_net/absence</a></li>\
            <li>/admin/config</li>\
            <ul>\
                <li>params:</li>\
                <ul>\
                    <li>max_daily_added_absences</li>\
                    <li>morning_update_hour</li>\
                    <li>late_morning_update_hour</li>\
                </ul>\
                <li>example: /admin/config?max_daily_added_absences=50&morning_update_hour=9&late_morning_update_hour=11</li>\
            </ul>\
            <li><a href='/admin/reset_update_time'>/admin/reset_update_time</a></li>\
        </ul>"

@app.route('/export_vklass_net/absence')
def export_vklass_net_absence():
    global todaysAbsence
    xp = flask_request.headers.get('x-password')
    uid = flask_request.args.get('UID')
    logger.debug("xp: " + str(xp) + ", uid: " + str(uid))
    update_vklass_absences_today()
    return todaysAbsence, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/export_vklass_net/schoolinfo')
def export_vklass_net_schoolinfo():
    global schools
    uid = flask_request.args.get('UID')
    logger.debug(str(schools))
    return schools, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/admin/config')
def admin_config():
    global max_daily_added_absences
    global morning_update_hour
    global late_morning_update_hour
    m_abs = flask_request.args.get('max_daily_added_absences')
    if m_abs is not None:
        max_daily_added_absences = int(m_abs)
        logger.debug("max_daily_added_absences updated to " + m_abs)
    u_hr = flask_request.args.get('morning_update_hour')
    if u_hr is not None:
        morning_update_hour = int(u_hr)
        logger.debug("morning_update_hour updated to " + u_hr)
    u_late_hr = flask_request.args.get('late_morning_update_hour')
    if u_late_hr is not None:
        late_morning_update_hour = int(u_late_hr)
        logger.debug("late_morning_update_hour updated to " + u_late_hr)
    return redirect("/", code=302)

@app.route('/admin/reset_update_time')
def admin_reset():
    global last_call
    last_call = datetime.now() - timedelta(days=1)
    logger.debug("update time reset")
    return redirect("/", code=302)


# ----------------------------------------


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=12345, host='0.0.0.0')
