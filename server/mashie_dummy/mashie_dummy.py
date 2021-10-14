# 
# Currently generates fiware/ngsiv2-compatible versions of Mashie's
# OpenMeal data every day (and at startup historical). Since
# Will use environment variables if found:
#    - NUM_DAYS_HISTORY

import logging, sys, os
from datetime import datetime, timedelta
from threading import Timer
import json
import string
import requests


logger = logging.getLogger('mashie_dummy')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

NUM_DAYS_HISTORY = int(os.environ['NUM_DAYS_HISTORY']) if 'NUM_DAYS_HISTORY' in os.environ else 14
MASHIE_MEAL_FILE = "mashie_one_months_meals.json"

last_update = datetime.now() - timedelta(days=(NUM_DAYS_HISTORY+1))

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


# https://rc.mashie.com/api/open-meal/v3/meals... output example:
# {
#     "meals": [
#         {
#             "name": "Lunch 1",
#             "date": "2021-09-01",
#             "lang": null,
#             "courses": [
#                 {
#                     "name": "Köttfärslåda med potatis och curry",
#                     "ingredientsLabel": "Nötfärs 10 %, GratängOST 28%, Ketchup tomat, Potatis strimlad, Lök rå tärnad , Salt, Ostcreme stark 15%, Curry, MellanMJÖLK 1,5% 10L  EKO",
#                     "possibleAllergens": [],
#                     "preferences": [],
#                     "nutrients": [
#                         {
#                             "name": "Energi (kJ)",
#                             "amount": 1424.52,
#                             "unit": "kJ"
#                         },
#                         {
#                             "name": "Energi (kcal)",
#                             "amount": 340.77,
#                             "unit": "kcal"
#                         },
#                         {
#                             "name": "Fett",
#                             "amount": 11.96,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "varav mättade fettsyror",
#                             "amount": 6.55,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Enkelomättade fettsyror",
#                             "amount": 3.98,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Fleromättade fettsyror",
#                             "amount": 0.52,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Kolhydrater",
#                             "amount": 39.07,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Protein",
#                             "amount": 18.47,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Fibrer",
#                             "amount": 2.09,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Salt",
#                             "amount": 1.85,
#                             "unit": "g"
#                         },
#                         {
#                             "name": "Vitamin D",
#                             "amount": 0.20,
#                             "unit": "µg"
#                         },
#                         {
#                             "name": "Vitamin C",
#                             "amount": 20.55,
#                             "unit": "mg"
#                         },
#                         {
#                             "name": "Järn",
#                             "amount": 2.41,
#                             "unit": "mg"
#                         },
#                         {
#                             "name": "Kalcium",
#                             "amount": 145.0,
#                             "unit": "mg"
#                         },
#                         {
#                             "name": "Natrium",
#                             "amount": 756.25,
#                             "unit": "mg"
#                         }
#                     ],
#                     "co2Equivalents": 1.55
#                 }
#             ]
#         },
#         ...


def add_meals_for_day(day):
    global mashie_meals
    
    mashie_meals_date = datetime.strptime(mashie_meals[0]['date'], "%Y-%m-%d").replace(day=day.day)
    logger.debug("add meals for day " + day.strftime("%Y-%m-%d") + " by using " + mashie_meals_date.strftime("%Y-%m-%d"))
    # same meal for all schools for now
    day_meal = None
    for meal in mashie_meals:
        if (meal['date'] == mashie_meals_date.strftime("%Y-%m-%d")):
            day_meal = meal
            break
    
    for s in schools["schoolidCollection"]:
        json_data = {
            "id": "mashie_meal_" + str(s["schoolid"]) + "_" + day_meal['name'].strip().replace(" ", "_") + "_" + day.strftime("%Y-%m-%d"),
            "type": "OpenMeal",
            "date": {
                "type": "DateTime",
                "value": day.strftime("%Y-%m-%dT%H%M%S.%fZ"),
                "metadata": {}
            },
            "lang": {
                "type": "Text",
                "value": (day_meal['lang'] if day_meal['lang'] != None else "")
            },
            "name": {
                "type": "Text",
                "value": (day_meal['name'] if day_meal['name'] != None else "")
            },
            "courses": {
                "type": "Course",
                "value": day_meal['courses']
            },
            "refSchool": {
                "type": "Reference",
                "value": "vklass_school_" + str(s["schoolid"]),
                "metadata": {}
            },
            "source": {
                "type": "Text",
                "value": "http://www.matildafoodtech.com",
                "metadata": {}
            }
        }
        # if s["schoolid"] == 1:
        #     logger.debug(json_data)
        success = orion_cru_entity(json_data)
        logger.debug("... for school " + str(s["schoolid"]) + ": " + str(success))

def generate_history():
    global last_update
    global mashie_meals
    logger.debug(f"Reading maashie meals from {MASHIE_MEAL_FILE}")
    with open(MASHIE_MEAL_FILE) as json_file:
        json_obj = json.load(json_file)
        mashie_meals = json_obj['meals']
        json_file.close()

    logger.debug(f"Generating {NUM_DAYS_HISTORY} day history ...")
    while last_update.date() < (datetime.today() - timedelta(days=1)).date():
        last_update = last_update + timedelta(days=1)
        if (last_update.isoweekday()):
            add_meals_for_day(last_update)
    logger.debug("\nHistory done.\n")


def generate_continously():
    now = datetime.now()
    if (now.isoweekday()):
        add_meals_for_day(now)
    
    tomorrow = now.replace(day=now.day, hour=0, minute=59, second=0, microsecond=0) + timedelta(days=1)
    delta_dt = tomorrow-now
    delta_secs = delta_dt.total_seconds()
    t = Timer(delta_secs, generate_continously)
    t.start()


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


if __name__ == "__main__":
    generate_history()
    generate_continously()