from flask import Blueprint, session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
# db = client.prod
tech = Blueprint('tech', __name__)


@tech.route('/tech', methods=['GET'])
def get_tech():
    country = session['country']
    region = session['region']
    role = session['role'] 
    print(region,len(role),country)
    pipe = [{
        '$lookup':
        {
            'from': "Scraped_Data",
            'localField': "url",
            'foreignField': "url",
            'as': "role_info"
        }
    },
        {'$match': {"role_info.country": country ,
         "role_info.region": region,
         "role_info.title": role}},
        {"$group": {"_id": "$found_list"}}
    ]
    count = client.prod.Scraped_Data.count( {"country": country ,
         "region": region,
         "title": role}) 
    query = client.prod.techs.aggregate(pipeline=pipe)
    embedded_list = [x.get("_id") for x in query]
    tech_list = sum(embedded_list,[])
    out = {"counts" :Counter(tech_list),"numRoles":count }
    return json.dumps(out)
