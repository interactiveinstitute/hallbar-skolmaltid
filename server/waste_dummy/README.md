
# Notes

## Overview
This service generates waste data for every weekday, starting by generating a number of days history, configurable in compose file. The data is based around statistics from Helsingborg municipality - see below.

## Helsingborg waste data file
The 'vramlosa_waste.csv' file contains waste data per student for a year, based on a spreadsheet file with statistics provided by Helsingborg, where we
- used data from the school with the most students
- kept the three reported wastes - kökssvinn, serveringssvinnn, tallrikssvinn, totalt svinn
- recalculated to give a per-student value
- removed data for days with no students eating

## Example meals data for one day, one shool
```json
{
    "id": "waste_1_2021-08-16",
    "type": "FoodWaste",
    "date": {
        "type": "DateTime",
        "value": "2021-08-16T11:34:01.00Z",
        "metadata": {}
    },
    "kitchenWaste": {
        "type": "Float",
        "value": "0.0000",
        "metadata": {
            "unitCode": {
                "type": "Text",
                "value": "kg/person"
            }
        }
    },
    "plateWaste": {
        "type": "Float",
        "value": "0.0072",
        "metadata": {
            "unitCode": {
                "type": "Text",
                "value": "kg/person"
            }
        }
    },
    "refSchool": {
        "type": "Reference",
        "value": "vklass_school_1",
        "metadata": {}
    },
    "servingWaste": {
        "type": "Float",
        "value": "0.0091",
        "metadata": {
            "unitCode": {
                "type": "Text",
                "value": "kg/person"
            }
        }
    },
    "source": {
        "type": "Text",
        "value": "http://helsingborg.se",
        "metadata": {}
    },
    "totalWaste": {
        "type": "Float",
        "value": "0.0199",
        "metadata": {
            "unitCode": {
                "type": "Text",
                "value": "kg/person"
            }
        }
    }
}
```
