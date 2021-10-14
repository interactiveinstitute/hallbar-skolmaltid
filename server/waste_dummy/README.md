
# Notes

## Overview
This service generates waste data for every weekday, starting by generating a number of days history, configurable in compose file. The data is based around statistics from Helsingborg municipality - see below.

## Helsingborg waste data file
The 'vramlosa_waste.csv' file contains waste data per student for a full month based on a spreadsheet file with statistics provided by Helsingborg, where we
- used data from the school with the most students
- kept the three reported wastes - kökssvinn, serveringssvinnn, tallrikssvinn, totalt svinn
- recalculated to give a per-student value
- removed data for days with no students eating

## Example meals data for one day, one shool
```json
{
	"id": "waste_1_Lunch_1_2021-10-14",
	"type": "FoodWaste",
	"dateObserved": {
		"type": "DateTime",
		"value": "2021-10-14T090302.007008Z",
	},
	"kitchenWaste": {
		"type": "Float",
		"value": 5.5,
		"metadata": {
			"unitCode": {
				"type": "Text",
				"value" :"kg/person"
			}
		}
	},
	"servingWaste": {
		"type": "Float",
		"value": 6.6,
		"metadata": {
			"unitCode": {
				"type": "Text",
				"value" :"kg/person"
			}
		}
	},
	"plateWaste": {
		"type": "Float",
		"value": 7.7,
		"metadata": {
			"unitCode": {
				"type": "Text",
				"value" :"kg/person"
			}
		}
	},
	"totalWaste": {
		"type": "Float",
		"value": 8.8,
		"metadata": {
			"unitCode": {
				"type": "Text",
				"value" :"kg/person"
			}
		}
	},
	"refSchool": {
		"type": "Reference",
		"value": "vklass_school_1",
		"metadata": {}
	},
	"source": {
		"type": "Text",
		"value": "http://www.matildafoodtech.com",
		"metadata": {}
	}
}
```
