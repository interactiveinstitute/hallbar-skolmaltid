# 
# Currently generates fiware/ngsiv2-compatible food waste data
# based on real statistics from Helsingborg
# Will use environment variables if found:
#    - NUM_DAYS_HISTORY

import logging, sys, os
from datetime import datetime, timedelta
from threading import Timer
from csv import DictReader
import json
import random
import string
import requests


logger = logging.getLogger('waste_dummy')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

NUM_DAYS_HISTORY = int(os.environ['NUM_DAYS_HISTORY']) if 'NUM_DAYS_HISTORY' in os.environ else 14
WASTE_STATS_FILE = "vramlosa_waste.csv"

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


# Output example:
# {
# 	"id": "waste_1_Lunch_1_2021-10-14",
# 	"type": "FoodWaste",
# 	"dateObserved": {
# 		"type": "DateTime",
# 		"value": "2021-10-14T090302.007008Z",
# 	},
# 	"kitchenWaste": {
# 		"type": "Float",
# 		"value": 5.5,
# 		"metadata": {
# 			"unitCode": {
# 				"type": "Text",
# 				"value" :"kg/person"
# 			}
# 		}
# 	},
# 	"servingWaste": {
# 		"type": "Float",
# 		"value": 6.6,
# 		"metadata": {
# 			"unitCode": {
# 				"type": "Text",
# 				"value" :"kg/person"
# 			}
# 		}
# 	},
# 	"plateWaste": {
# 		"type": "Float",
# 		"value": 7.7,
# 		"metadata": {
# 			"unitCode": {
# 				"type": "Text",
# 				"value" :"kg/person"
# 			}
# 		}
# 	},
# 	"totalWaste": {
# 		"type": "Float",
# 		"value": 8.8,
# 		"metadata": {
# 			"unitCode": {
# 				"type": "Text",
# 				"value" :"kg/person"
# 			}
# 		}
# 	},
# 	"refSchool": {
# 		"type": "Reference",
# 		"value": "vklass_school_1",
# 		"metadata": {}
# 	},
# 	"source": {
# 		"type": "Text",
# 		"value": "http://www.matildafoodtech.com",
# 		"metadata": {}
# 	}
# }
#


def add_waste_for_day(day):
    global waste_data
    
    logger.debug("add waste for day " + day.strftime("%Y-%m-%d"))
    
    for s in schools["schoolidCollection"]:
        day_waste = waste_data[random.randint(0, len(waste_data)-1)]
        json_data = {
            "id": "waste_" + str(s["schoolid"]) + "_" + day.strftime("%Y-%m-%d"),
            "type": "FoodWaste",
            "date": {
                "type": "DateTime",
                "value": day.strftime("%Y-%m-%dT%H%M%S.%fZ"),
                "metadata": {}
            },
            "kitchenWaste": {
                "type": "Float",
                "value": day_waste['kitchenWaste'],
                "metadata": {
                    "unitCode": {
                        "type": "Text",
                        "value" :"kg/person"
                    }
                }
            },
            "servingWaste": {
                "type": "Float",
                "value": day_waste['servingWaste'],
                "metadata": {
                    "unitCode": {
                        "type": "Text",
                        "value" :"kg/person"
                    }
                }
            },
            "plateWaste": {
                "type": "Float",
                "value": day_waste['plateWaste'],
                "metadata": {
                    "unitCode": {
                        "type": "Text",
                        "value" :"kg/person"
                    }
                }
            },
            "totalWaste": {
                "type": "Float",
                "value": day_waste['totalWaste'],
                "metadata": {
                    "unitCode": {
                        "type": "Text",
                        "value" :"kg/person"
                    }
                }
            },
            "refSchool": {
                "type": "Reference",
                "value": "vklass_school_" + str(s["schoolid"]),
                "metadata": {}
            },
            "source": {
                "type": "Text",
                "value": "http://helsingborg.se",
                "metadata": {}
            }
        }
        # if s["schoolid"] == 1:
        #     logger.debug(json_data)
        success = orion_cru_entity(json_data)
        logger.debug("... for school " + str(s["schoolid"]) + ": " + str(success))

def generate_history():
    global last_update
    global waste_data
    logger.debug(f"Reading waste data from {WASTE_STATS_FILE}")
    with open(WASTE_STATS_FILE) as read_obj:
        waste_data = list(DictReader(read_obj, delimiter=","))

    logger.debug(f"Generating {NUM_DAYS_HISTORY} day history ...")
    while last_update.date() < (datetime.today() - timedelta(days=1)).date():
        last_update = last_update + timedelta(days=1)
        if (last_update.isoweekday()):
            add_waste_for_day(last_update)
    logger.debug("\nHistory done.\n")


def generate_continously():
    now = datetime.now()
    if (now.isoweekday()):
        add_waste_for_day(now)
    
    tomorrow = now.replace(day=now.day, hour=1, minute=59, second=0, microsecond=0) + timedelta(days=1)
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