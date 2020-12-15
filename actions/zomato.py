import requests
import json

headers = {'user-key': 'be12c6d609272b0e58f5c2e7cff52b2a',
           'Accept': 'application/json'}##########ADD KEY HERE########################################################

def getLocationDetailsbyName(location_name):
    data = {'query': location_name}
    url = 'https://developers.zomato.com/api/v2.1/locations'
    data = requests.get(url, headers=headers, params=data)
    data = json.loads(data.text)
    if(len(data["location_suggestions"])>0):
        entity_type = data["location_suggestions"][0]["entity_type"]
        entity_id = data["location_suggestions"][0]["entity_id"]
        title = data["location_suggestions"][0]["title"]
        city_id=data["location_suggestions"][0]["city_id"]
        country_id=data["location_suggestions"][0]["country_id"]
        details={"restaurants_available":"yes","entity_type":entity_type,"entity_id":entity_id,"title":title,"city_id":city_id,"country_id":country_id}
        longitude=data["location_suggestions"][0]["longitude"]
        latitude=data["location_suggestions"][0]["latitude"]
        return city_id,entity_id,entity_type
    else:
        return {"restaurants_available":"no"}

def getCuisineId(cuisine_name,city_id):
    data = {'city_id': city_id}
    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    # print("data: ",data)
    cuisines=data["cuisines"]
    cuisineID=None
    for cuisine in cuisines:
            if(cuisine_name.lower() == cuisine["cuisine"]["cuisine_name"].lower()):
                return cuisine["cuisine"]["cuisine_id"]
                      
    return cuisineID

def search(name,cname):

    city_id,entity_id,entity_type=getLocationDetailsbyName(name)
    if city_id==None:
        return 0
    cuisineID=getCuisineId(cname,city_id)
    if cuisineID!=None:
        return searchRestaurants(entity_id,entity_type,cuisineID)
    else:
        return 1



def searchRestaurants(entity_id, entity_type, cuisine_id):
    url = 'https://developers.zomato.com/api/v2.1/search'
    data = {"entity_id": entity_id, "entity_type": entity_type,
            "cuisines": cuisine_id, "count": "10", "order": "asc"}
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    l=[]
    if data!=None:
        for i in range(4):
            l.append(data['restaurants'][i])
        restaurant=[]
        for i in l:
            x=i['restaurant']
            restaurant.append([x['name'],x['url'],(x['location'])['address']])
    else:
        return 2

    return restaurant


