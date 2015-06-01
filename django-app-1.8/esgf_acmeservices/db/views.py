from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View

import json


import ConfigParser
acme_services_config = ConfigParser.ConfigParser()
acme_services_config.read('ACMEservices.cfg')

#db configuration params
dbname = acme_services_config.get("db_options","dbname")
dbuser = acme_services_config.get("db_options","dbuser")
dbpassword = acme_services_config.get("db_options","dbpassword")
isConnectedToDB = acme_services_config.get("db_options","isConnectedToDB")

#testing params
populate_groups = acme_services_config.get("test_options","populate_groups")


import logging
db_logger = logging.getLogger("db")
db_logger.setLevel(logging.INFO)

# create the logging file handler
# add handler to logger object
fh = logging.FileHandler("publication.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
db_logger.addHandler(fh)

db_logger.info("DB Program started") 

#gets group information
class GroupView(View):
    
    def get(self, request, username):
        
        print 'isConnected: ' + str(isConnectedToDB)
        
        if isConnectedToDB == "True":
        
            try:
            
                import psycopg2
                
                conn=psycopg2.connect("dbname='" + dbname + "' user='" + dbuser + "' password='" + dbpassword + "'")
                cur = conn.cursor()
                
                '''
                user_id = get_user_id(username)

                print 'user_id: ' + user_id    
            
                group_id_list_set = get_group_id_list_set(user_id)
            
                group_name_list_set = get_group_name_list_set(group_id_list_set)
            
                groups_response = group_name_list_set
                '''
            
                return HttpResponse("Connected\n")
            
            except:
                print 'in connected to DB except'
            
                return HttpResponse("Not Connected\n")
        
        else:
            groups_response = []
            if populate_groups == "True":
                groups_response.append('ACME')
                groups_response.append('CSSEF')
            data = {'groups' : groups_response}
        
            data_string = notConnectedResponse()
            return HttpResponse(data_string + '\n')
    
    




def notConnectedResponse():
    
    groups_response = []
    if populate_groups == "True":
        groups_response.append('ACME')
        groups_response.append('CSSEF')
    data = {'groups' : groups_response}

    data_string = json.dumps(data,sort_keys=False,indent=2)    

    return data_string

