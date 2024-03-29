from datetime import datetime
import requests,folium
from .models import Global, Countries, CountriesHistory, India, IndiaHistory
from math import sqrt
from geopy.geocoders import Nominatim
def fetchCovidGlobalData():
    r = requests.get('  https://covid19.mathdro.id/api')
    r = r.json()
    return r


def fetchCovidIndiaData():
    r = requests.get('https://api.covid19india.org/data.json')
    r = r.json()
    return r


def globalData():
    r = fetchCovidGlobalData()
    global_data = r['Global']
    # global_data_date = r['Date']
    # print("global data date:",global_data_date)
    c = r['Countries']
    global_data_date = r['Countries'][1]["Date"]
    print("global data date:", global_data_date)
    global_datanew = None
    countries_data_new = None
    for i in range(len(c)):
        countries_data = r['Countries'][i]
        if Countries.objects.filter(slugId=countries_data['Slug']).exists():
            if Countries.objects.filter(date=countries_data['Date'], slugId=countries_data['Slug']).exists():
                continue
            else:
                CountriesHistory.objects.create(cid=countries_data['ID'],
                                                country=countries_data['Country'],
                                                countryCode=countries_data['CountryCode'],
                                                slugId=countries_data['Slug'],
                                                newConfirmed=int(countries_data['NewConfirmed']),
                                                totalConfirmed=int(countries_data['TotalConfirmed']),
                                                newDeaths=int(countries_data['NewDeaths']),
                                                totalDeaths=int(countries_data['TotalDeaths']),
                                                newRecovered=int(countries_data['NewRecovered']),
                                                totalRecoverd=int(countries_data['TotalRecovered']),
                                                date=countries_data['Date'],
                                                )
                countries_data_new = Countries.objects.get(slugId=countries_data['Slug'])
                countries_data_new.cid = countries_data['ID']
                countries_data_new.newConfirmed = int(countries_data['NewConfirmed'])
                countries_data_new.totalConfirmed = int(countries_data['TotalConfirmed'])
                countries_data_new.newDeaths = int(countries_data['NewDeaths'])
                countries_data_new.totalDeaths = int(countries_data['TotalDeaths'])
                countries_data_new.newRecovered = int(countries_data['NewRecovered'])
                countries_data_new.totalRecoverd = int(countries_data['TotalRecovered'])
                countries_data_new.date = countries_data['Date']
                countries_data_new.save()

        else:
            Countries.objects.create(cid=countries_data['ID'],
                                     country=countries_data['Country'],
                                     countryCode=countries_data['CountryCode'],
                                     slugId=countries_data['Slug'],
                                     newConfirmed=int(countries_data['NewConfirmed']),
                                     totalConfirmed=int(countries_data['TotalConfirmed']),
                                     newDeaths=int(countries_data['NewDeaths']),
                                     totalDeaths=int(countries_data['TotalDeaths']),
                                     newRecovered=int(countries_data['NewRecovered']),
                                     totalRecoverd=int(countries_data['TotalRecovered']),
                                     date=countries_data['Date'],
                                     )

    print(global_data)
    if Global.objects.filter(update_date=global_data_date).exists():
        h = 1
    else:
        Global.objects.create(
                              newConfirmed=int(global_data['NewConfirmed']),
                              totalConfirmed=int(global_data['TotalConfirmed']),
                              newDeaths=int(global_data['NewDeaths']),
                              totalDeaths=int(global_data['TotalDeaths']),
                              newRecovered=int(global_data['NewRecovered']),
                              totalRecoverd=int(global_data['TotalRecovered']),
                              update_date=global_data_date,
                              )


def indiaData():

    r=fetchCovidIndiaData()
    statewise=r['statewise']
    datenew=statewise[0]['lastupdatedtime']
    for i in range(len(statewise)):
        statewise = r['statewise'][i]
        date = statewise['lastupdatedtime']
        date = date.replace('/', '-')
        datesplit = date.split(" ")
        date = datetime.strptime(datesplit[0], '%d-%m-%Y')
        date = date.strftime('%Y-%m-%d ')
        date += datesplit[1]
        indiadata=None

        statechanged = statewise['statecode']
        if statechanged == "UT":
            statechanged = "UK"
        elif statechanged == "LA":
            statechanged = "LD"
        elif statechanged == "TG":
            statechanged = "TS"
        elif statechanged == "OR":
            statechanged = "OD"
        elif statechanged == "UN":
            continue
        if India.objects.filter(state_code=statechanged).exists():
            if not India.objects.filter(last_update_time=date).exists():
                IndiaHistory.objects.create(state_code=statechanged,
                                            state=statewise['state'],
                                            active=statewise['active'],
                                            confirmed=statewise['confirmed'],
                                            new_confirmed=statewise['deltaconfirmed'],
                                            deaths=statewise['deaths'],
                                            new_deaths=statewise['deltadeaths'],
                                            recovered=statewise['deltarecovered'],
                                            new_recovered=statewise['recovered'],
                                            last_update_time=date
                                            )
            # update the data
            india = India.objects.get(state_code=statechanged)
            india.state = statewise['state']
            india.state_code = statechanged
            india.active = statewise['active']
            india.confirmed = statewise['confirmed']
            india.new_confirmed = statewise['deltaconfirmed']
            india.deaths = statewise['deaths']
            india.new_deaths = statewise['deltadeaths']
            india.new_recovered = statewise['deltarecovered']
            india.recovered = statewise['recovered']
            india.last_update_time = date
            india.save()
        else:
            India.objects.create(state=statewise['state'],
                                 state_code=statechanged,
                                 active=statewise['active'],
                                 confirmed=statewise['confirmed'],
                                 deaths=statewise['deaths'],
                                 new_confirmed=statewise['deltaconfirmed'],
                                 new_deaths=statewise['deltadeaths'],
                                 new_recovered=statewise['deltarecovered'],
                                 recovered=statewise['recovered'],
                                 last_update_time=date,
                                 )


def get_global_map():
    # map = folium.Map()  # fetch live location   #context
    country_all = Countries.objects.all()  # context
    geolocators = Nominatim(user_agent='COVID_19_Tracker')  # initialize app folder with nominatim
    for i in country_all:
        pk = i.slugId
        countryloc = geolocators.geocode(pk)
        try:
            lat = countryloc.latitude
            lon = countryloc.longitude
            if lat == None:
                print(pk)

            else:
                print("country_name:", pk, "lat: ", lat, "lon:", lon)
                getcountry=Countries.objects.get(slugId=pk)
                getcountry.lat=countryloc.latitude
                getcountry.lon=countryloc.longitude
                getcountry.save()
        except AttributeError:
            print(pk)


def get_India_map():
    state_all = India.objects.all()  # context
    geolocators = Nominatim(user_agent='COVID_19_Tracker')  # initialize app folder with nominatim
    print(state_all)
    for i in state_all:
        pk = i.state
        stateloc = geolocators.geocode(pk)
        lat=stateloc.latitude
        lon=stateloc.longitude
        if lat == None:
            print(pk)

        else:
            print("after state_name:", pk, "lat: ", lat, "lon:", lon)
            getstate=India.objects.get(state=pk)
            getstate.lat=stateloc.latitude
            getstate.lon=stateloc.longitude
            getstate.save()


