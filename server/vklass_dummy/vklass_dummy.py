# 
# Runs a flask server for emulating vklass endpoints, generating dummy
# data for the current day upon call.
# Currently built to be called every day, where if it's after a certain
# time in the morning, absence is added.
# UPDATE 210413: Now also generates history on first call, NOTE that
# it calls orion itself for this - not returned to draco/nifi.
# Will use environment variables if found:
#    - MAX_PERCENT_DAILY_ADDED_ABSENCES
#    - MORNING_UPDATE_HOUR
#    - LATE_MORNING_UPDATE_HOUR
#    - NUM_DAYS_HISTORY
# Otherwise, these can be changed dynamically through a config endpoint

import logging, sys, os
from datetime import datetime, timedelta
import json
import random
import copy
import requests
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
MAX_PERCENT_DAILY_ADDED_ABSENCES = int(os.environ['MAX_PERCENT_DAILY_ADDED_ABSENCES']) if 'MAX_PERCENT_DAILY_ADDED_ABSENCES' in os.environ else 20
morning_update_hour      = int(os.environ['MORNING_UPDATE_HOUR']) if 'MORNING_UPDATE_HOUR' in os.environ else 8
late_morning_update_hour = int(os.environ['LATE_MORNING_UPDATE_HOUR']) if 'LATE_MORNING_UPDATE_HOUR' in os.environ else 8
NUM_DAYS_HISTORY = int(os.environ['NUM_DAYS_HISTORY']) if 'NUM_DAYS_HISTORY' in os.environ else 14
uid_to_schoolid = {
    "8de0d630-209d-41d6-bef2-87e3a2fd24c3": 1,
    "piw7egza-4b44-hbgw-ipxw-nqmnvkuyr77c": 2,
    "idd6rswo-xva3-jjvd-6w77-vcf0k0se0lr2": 3,
    "5tc1hrjr-e22p-yvhl-9vsb-5o0edwrpzmaj": 4,
    "sxsy9ep3-6mrk-wnxw-0nvn-uhir126pi5ll": 5
}
schools = { # correct vklass format
    "schoolidCollection":[
        {
            "schoolid":1,
            "schoolname":"Gripenskolan F-9",
            "schooltype":0,
            "studentcount":800,
            "personalcount":40
        },
        {
            "schoolid":2,
            "schoolname":"FS Paletten",
            "schooltype":0,
            "studentcount":40,
            "personalcount":4
        },
        {
            "schoolid":3,
            "schoolname":"FS Blåklockan",
            "schooltype":0,
            "studentcount":50,
            "personalcount":5
        },
        {
            "schoolid":4,
            "schoolname":"FS Humlan",
            "schooltype":0,
            "studentcount":45,
            "personalcount":4
        },
        {
            "schoolid":5,
            "schoolname":"FS Vargtass",
            "schooltype":0,
            "studentcount":30,
            "personalcount":3
        }
    ]
}
todaysAbsence = {} # absenceidCollection in correct vklass format
studentCount = {}
for s in schools["schoolidCollection"]:
    todaysAbsence[s["schoolid"]] = {'absenceidCollection':[]}
    studentCount[s["schoolid"]] = s["studentcount"]

last_update = datetime.now() - timedelta(days=(NUM_DAYS_HISTORY+1))
# names from Swedish baby name top list 2019:
first_names = ["Lucas", "Liam", "William", "Elias", "Noah", "Hugo", "Oliver", "Oscar", "Adam", "Matteo", "Walter", "Alexander", "Leo", "Nils", "Alfred", "Ludvig", "Adrian", "Theo", "Leon", "Elliot", "Arvid", "Vincent", "Theodor", "Filip", "Axel", "Harry", "Frans", "Charlie", "Mohamed", "Gabriel", "Isak", "August", "Loui", "Benjamin", "Sam", "Josef", "Ebbe", "Melvin", "Love", "Olle", "Albin", "Henry", "Edvin", "Elton", "Emil", "Malte", "Vidar", "Gustav", "Jack", "Frank", "Viggo", "Noel", "Sixten", "Viktor", "Melker", "Jacob", "Casper", "Erik", "Tage", "Aron", "Loke", "Otto", "Wilmer", "Colin", "Milo", "Sigge", "Alvin", "Carl", "Milton", "Wilhelm", "Anton", "Ivar", "Kian", "Julian", "Max", "Elis", "Levi", "Nicholas", "Elvin", "Felix", "Vilgot", "Ali", "Omar", "Hjalmar", "Ture", "Samuel", "David", "Kevin", "Joel", "Vide", "Amir", "Ville", "Dante", "John", "Daniel", "Algot", "Folke", "Alve", "Ibrahim", "Thor",\
"Alice", "Olivia", "Astrid", "Maja", "Vera", "Ebba", "Ella", "Wilma", "Alma", "Lilly", "Elsa", "Agnes", "Freja", "Saga", "Ellie", "Clara", "Signe", "Alva", "Alicia", "Selma", "Ester", "Stella", "Julia", "Ines", "Leah", "Ellen", "Molly", "Iris", "Sara", "Luna", "Isabelle", "Nora", "Nova", "Hedda", "Mila", "Nellie", "Sofia", "Lova", "Juni", "Elvira", "Linnéa", "Emilia", "Sigrid", "Celine", "Elise", "Edith", "Emma", "Lykke", "Liv", "Lo", "Thea", "Mejas", "Livia", "Tuva", "Isabella", "Sally", "Majken", "Maria", "Leia", "Hailey", "Tyra", "Elin", "Amelia", "Lovisa", "Märta", "Rut", "Ida", "Ingrid", "Bianca", "Hanna", "Ronja", "Jasmine", "Stina", "Svea", "Cleo", "Melissa", "Hilma", "Filippa", "Hedvig", "Julie", "Tilde", "Lovis", "Siri", "Felicia", "Cornelia", "Elina", "Elsie", "Joline", "Hilda", "Mira", "Moa", "Melina", "Bonnie", "Mariam", "Matilda", "Wilda", "Bella", "Millie", "My", "Amanda"]
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

def remove_absence_before_day(day_time):
    global todaysAbsence
    past_midnight_str = day_time.strftime("%Y-%m-%dT00:00:00")
    for sid in todaysAbsence.keys():
        todaysAbsence[sid]['absenceidCollection'] = [a for a in todaysAbsence[sid]['absenceidCollection'] if not (a['enddate'] < past_midnight_str)]
        logger.debug("   school " + str(sid) + ": " + str(len(todaysAbsence[sid]['absenceidCollection'])) + " absences left from previous day")

def add_absences_for_day(day_time, portion_now, ):
    global todaysAbsence
    global MAX_PERCENT_DAILY_ADDED_ABSENCES
    for sid in todaysAbsence.keys():
        logger.debug("adding absences for school " + str(sid) + " rand(" + str(portion_now) + " * " + str(MAX_PERCENT_DAILY_ADDED_ABSENCES/100) + " * " + str(studentCount[sid]) + ")")
        for ix in range(random.randint(0, int(portion_now*(MAX_PERCENT_DAILY_ADDED_ABSENCES/100)*studentCount[sid]))):
            absence = {}
            absence["absenceid"]        = str(random.randrange(100000, 100000000))
            absence["usersocialnumber"] = str(random.randrange(100000, 1000000)) + "-" + str(random.randrange(1000, 10000))
            absence["userfirstname"] = first_names[random.randrange(len(first_names))]
            absence["userlastname"]  =  last_names[random.randrange(len(last_names))]
            absence["created"] = str(day_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])
            absence["updated"] = absence["created"]
            length_rand = random.random()
            if length_rand < 0.03:
                # 1 week
                absence["startdate"] = day_time.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
                absence["enddate"]   = (day_time + timedelta(days=6)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")
                logger.debug("add absence #" + str(ix) + ": 7 days")
            elif length_rand < 0.10:
                # 3 days
                absence["startdate"] = day_time.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
                absence["enddate"]   = (day_time + timedelta(days=2)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")
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
                absence["startdate"] = day_time.replace(hour=start_hour,   minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
                absence["enddate"]   = day_time.replace(hour=start_hour+num_hours, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
                logger.debug("add absence #" + str(ix) + ": " + str(num_hours) + " hour")
            todaysAbsence[sid]['absenceidCollection'].append(absence)

def update_vklass_absences_today():
    global last_update
    global morning_update_hour
    global late_morning_update_hour
    morning_update      = datetime.now().replace(hour=morning_update_hour,      minute=0, second=0)
    late_morning_update = datetime.now().replace(hour=late_morning_update_hour, minute=0, second=0)
    if last_update < morning_update:
        logger.debug("BEFORE MORNING UPDATE! Cleanup ...")
        remove_absence_before_day(datetime.now())
    if last_update < morning_update and datetime.now() >= morning_update:
        logger.debug("MORNING UPDATE!")
        add_absences_for_day(datetime.now(), 0.9)
        last_update = datetime.now()
    if last_update < late_morning_update and datetime.now() >= late_morning_update:
        logger.debug("LATE MORNING UPDATE!")
        add_absences_for_day(datetime.now(), 0.1)
        last_update = datetime.now()

# NOTE: This calls orion directly - so make sure there's no inconsistency between draco calls to orion and this
def generate_vklass_absence_history():
    global last_update
    logger.debug(f"Generating {NUM_DAYS_HISTORY} day history ...")
    while last_update.date() < (datetime.today() - timedelta(days=1)).date():
        last_update = last_update + timedelta(days=1)
        print("Generating history for", last_update)
        remove_absence_before_day(last_update)
        add_absences_for_day(last_update, 1.0)
        for s in schools["schoolidCollection"]:
            abs_list = copy.deepcopy(todaysAbsence[s["schoolid"]]['absenceidCollection'])
            for a in abs_list:
                a.pop('absenceid', None)
                a.pop('created', None)
                a.pop('updated', None)
                a["socialNumber"] = a.pop("usersocialnumber")
                a["givenName"] = a.pop("userfirstname")
                a["familyName"] = a.pop("userlastname")
                a["dateStart"] = a.pop("startdate")
                a["dateEnd"] = a.pop("enddate")
            json_data = {
                "id": "vklass_absence_" + str(s["schoolid"]) + "_" + last_update.strftime("%Y-%m-%d"),
                "type": "SchoolAttendanceObserved",
                "absent": {
                    "type": "studentAbsence",
                    "value": abs_list,
                    "metadata": {}
                },
                "dateObserved": {
                    "type": "DateTime",
                    "value": last_update.strftime("%Y-%m-%dT%H%M%S.%fZ"),
                    "metadata": {}
                },
                "enrolled": {
                    "type": "Integer",
                    "value": s["studentcount"],
                    "metadata": {}
                },
                "refSchool": {
                    "type": "Reference",
                    "value": "vklass_school_" + str(s["schoolid"]),
                    "metadata": {}
                },
                "source": {
                    "type": "Text",
                    "value": "http://www.vklass.se",
                    "metadata": {}
                }
            }
            success = orion_cru_entity(json_data)

def orion_cru_entity(data_dict, entity_id=None, verb="POST"):
    success = True
    fiware_url = "http://orion:1026/v2/entities/"
    if entity_id:
        # existing entity - patch attributes
        fiware_url = fiware_url + "/" + entity_id + "/attrs"
    # print(verb + " : " + fiware_url + "\n" + str(data_dict))
    response = None
    try:
        response = requests.request(verb, fiware_url,
            data = json.dumps(data_dict),
            headers = {"Content-type": "application/json", "fiware-service":"timeseries", "fiware-servicepath":"/"}
        )
    except Exception as e:
        success = False
        print(f"Problem making orion call\n  {verb} : {fiware_url}\n  {str(data_dict)}\nError: {str(e)}")

    # Ignore some responses as ok - 201 Created, 204 No Content, 409 Conflict (already exists)
    if (response and (response.status_code not in [201, 204, 409])):
        print(f"Problem making orion call:\n  Data: {data_dict}\n  Response: {response.status_code}: {response.content}")
    return success

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
                    <li>MAX_PERCENT_DAILY_ADDED_ABSENCES</li>\
                    <li>morning_update_hour</li>\
                    <li>late_morning_update_hour</li>\
                </ul>\
                <li>example: /admin/config?MAX_PERCENT_DAILY_ADDED_ABSENCES=50&morning_update_hour=9&late_morning_update_hour=11</li>\
            </ul>\
            <li><a href='/admin/reset_update_time'>/admin/reset_update_time</a></li>\
        </ul>"

@app.route('/export_vklass_net/absence')
def export_vklass_net_absence():
    global uid_to_schoolid
    global todaysAbsence
    global last_update
    xp = flask_request.headers.get('x-password')
    uid = flask_request.args.get('UID')
    logger.debug("xp: " + str(xp) + ", uid: " + str(uid) + ", sid: " + str(uid_to_schoolid[uid]))
    if last_update.date() < (datetime.today() - timedelta(days=1)).date():
        generate_vklass_absence_history()
    update_vklass_absences_today()
    return todaysAbsence[uid_to_schoolid[uid]], 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/export_vklass_net/schoolinfo')
def export_vklass_net_schoolinfo():
    global schools
    uid = flask_request.args.get('UID') # not currently used
    logger.debug(str(schools))
    return schools, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/admin/config')
def admin_config():
    global MAX_PERCENT_DAILY_ADDED_ABSENCES
    global morning_update_hour
    global late_morning_update_hour
    m_abs = flask_request.args.get('MAX_PERCENT_DAILY_ADDED_ABSENCES')
    if m_abs is not None:
        MAX_PERCENT_DAILY_ADDED_ABSENCES = int(m_abs)
        logger.debug("MAX_PERCENT_DAILY_ADDED_ABSENCES updated to " + m_abs)
    u_hr = flask_request.args.get('morning_update_hour')
    if u_hr is not None:
        morning_update_hour = int(u_hr)
        logger.debug("morning_update_hour updated to " + u_hr)
    u_late_hr = flask_request.args.get('late_morning_update_hour')
    if u_late_hr is not None:
        late_morning_update_hour = int(u_late_hr)
        logger.debug("late_morning_update_hour updated to " + u_late_hr)
    return redirect("/", code=302)

# @app.route('/admin/reset_update_time')
# def admin_reset():
#     global last_update
#     last_update = datetime.now() - timedelta(days=1)
#     logger.debug("update time reset")
#     return redirect("/", code=302)


# ----------------------------------------


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=12345, host='0.0.0.0')
