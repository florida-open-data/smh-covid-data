# smh-covid-data

Sarasota Memorial Hospital Covid-19 Data
Located in Sarasota County, Florida USA

### Status

[![Fetch latest data](https://github.com/florida-open-data/smh-covid-data/actions/workflows/scheduled.yml/badge.svg)](https://github.com/florida-open-data/smh-covid-data/actions/workflows/scheduled.yml)


### About
This is an unofficial repository of historical data downloaded from
Sarasota Memorial Hospital Covid-19 information page.
https://www.smh.com/Home/News-Events/Release/coronavirus-daily-news-update


The SMH website was downloaded and saved for historical reference and study.
The original HTML pages are available under the data/ directory.
Python programs were used to transform values into CSV and JSON format.
The other derivative file formats are: text, csv, json.

This historial data is provided as an information resource only.
This is an effort to share community data.
No warranty is made regarding this data.
However, every effort was made to preserve accuracy and completeness of the data.

https://twitter.com/data_florida
@data_florida


### Schema

JSON data schema for COVID-19 patient data

data field name | data field description
--------------- | ---------------------
covid_icu_today |  COVID Patent count in ICU today
covid_icu_yesterday | COVID Patent count in ICU yesterday
cumm_patient_discharged_today |  Cummulative patients discharged today
cumm_patient_discharged_yesterday |   Cummulative patients discharged yesterday
cumm_patient_today |   Cummulative patients as of today
cumm_patient_yesterday |  Cummulative patients as of yesterday
info_date | Date of information; example: "2021-07-15T00:00"
percent_unvaccinated | Percent of covid patients not vaccinated
positivity_rate |  Positivity rate today
positivity_rate_last_week |  Positivity rate last week
since_date | Data origin specified on site; example:  "Reflects patients tested through SMH systems since March 2 2020"
total_beds |  Total beds capacity
total_icu_beds |  Total ICU beds capacity
total_icu_today |  ICU count today
total_icu_yesterday |  ICU count yesterday
total_patient |  Total patient (need to clarify)
total_patient_today |  Total patient count today
total_patient_yesterday |   Total patient count yesterday
total_test_negative |  Total covid test negative (no duplicate patients)
total_test_positive |  Total covid test positive (no duplicate patients)



#### Example schema data:
```
{
   "covid_icu_today" : 45,
   "covid_icu_yesterday" : 44,
   "cumm_patient_discharged_today" : 3914,
   "cumm_patient_discharged_yesterday" : 3862,
   "cumm_patient_today" : 3290,
   "cumm_patient_yesterday" : 3266,
   "info_date" : "2021-08-12T00:00:00",
   "percent_unvaccinated" : 90,
   "positivity_rate" : 18.7,
   "positivity_rate_last_week" : 13.8,
   "since_date" : "Reflects patients tested through SMH systems since March 2 2020",
   "total_beds" : 839,
   "total_icu_beds" : 90,
   "total_icu_today" : 69,
   "total_icu_yesterday" : 73,
   "total_patient" : 782,
   "total_patient_today" : 205,
   "total_patient_yesterday" : 211,
   "total_test_negative" : 96260,
   "total_test_positive" : 5262
}
```


### JSON Data

Complete JSON output available at: 
https://github.com/florida-open-data/smh-covid-data/blob/main/smh_data.json

Raw JSON for web services:
https://raw.githubusercontent.com/florida-open-data/smh-covid-data/main/smh_data.json

### CSV Data

Complete CSV output available at: 
https://github.com/florida-open-data/smh-covid-data/blob/main/smh_data.csv

Raw CSV for web services:
https://raw.githubusercontent.com/florida-open-data/smh-covid-data/main/smh_data.csv

