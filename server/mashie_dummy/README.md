
# Notes

## Overview
This service generates meals data for every weekday, starting by generating a number of days history, configurable in compose file. The data model adheres as closely as it can to the work around the OpenMeal format. The data comes from one months' data downloaded from Mashie - see below.

## Mashie data file
The 'mashie_one_months_meals.json' file contains meals data for a full month downloaded through the mashie api, with the manual addition of
- filling in the weekends so that every day of the month has data (for use in any other month)
- the parentheses for nutrient energy are removed because of being fiware/ngsi non-compliant
- the 'lang' attribute was filled in with the correct 'sv' value
- possibleAllergens list was mostly empty, so some data was filled in (see [livsmedelsverket](https://www.livsmedelsverket.se/livsmedel-och-innehall/text-pa-forpackning-markning/allergimarkning)/[EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32003L0089))

## Example meals data for one day, one shool
```json
{
	"id": "mashie_meal_1_Lunch_1_2021-10-14",
	"type": "OpenMeal",
	"date": {
		"type": "DateTime",
		"value": "2021-10-14T090302.007008Z",
		"metadata": {}
	},
	"lang": {
		"type": "Text",
		"value": "sv"
	},
	"name": {
		"type": "Text",
		"value": "Lunch 1"
	},
	"courses": {
		"type": "Course",
		"value": [{
			"name": "Fiskpanett, kall s?s med dill, kokt potatis",
			"ingredientsLabel": "Dill fryst, Paprikapulver, MF Majonn?s l?tt fett 35 % ?GGfri, Salt, Torskfiskett, MSC, f?rstekt, GR?DDfil, FilMJ?LK 3%  EKO, Potatis skalad, Svartpeppar mald",
			"possibleAllergens": ["fisk", "mjölkprodukter"],
			"preferences": [],
			"nutrients": [{
				"name": "Energi",
				"amount": 2079.46,
				"unit": "kJ"
			}, {
				"name": "Energi",
				"amount": 498.58,
				"unit": "kcal"
			}, {
				"name": "Fett",
				"amount": 21.21,
				"unit": "g"
			}, {
				"name": "varav m?ttade fettsyror",
				"amount": 3.61,
				"unit": "g"
			}, {
				"name": "Enkelom?ttade fettsyror",
				"amount": 1.97,
				"unit": "g"
			}, {
				"name": "Flerom?ttade fettsyror",
				"amount": 4.25,
				"unit": "g"
			}, {
				"name": "Kolhydrater",
				"amount": 53.85,
				"unit": "g"
			}, {
				"name": "Protein",
				"amount": 22.08,
				"unit": "g"
			}, {
				"name": "Fibrer",
				"amount": 1.78,
				"unit": "g"
			}, {
				"name": "Salt",
				"amount": 1.92,
				"unit": "g"
			}, {
				"name": "Vitamin D",
				"amount": 0.02,
				"unit": "?g"
			}, {
				"name": "Vitamin C",
				"amount": 15.58,
				"unit": "mg"
			}, {
				"name": "J?rn",
				"amount": 1.3,
				"unit": "mg"
			}, {
				"name": "Kalcium",
				"amount": 69.1,
				"unit": "mg"
			}, {
				"name": "Natrium",
				"amount": 640.78,
				"unit": "mg"
			}],
			"co2Equivalents": 0.35
		}]
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
