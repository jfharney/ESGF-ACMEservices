from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View

import json
import ConfigParser
import traceback
import logging

acme_services_config = ConfigParser.ConfigParser()
acme_services_config.read('ACMEservices.cfg')

logger = logging.getLogger("db")
logger.setLevel(logging.DEBUG)

# create the logging file handler
db_log_file = acme_services_config.get("loggers","db_log_file")
fh = logging.FileHandler(db_log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)


#gets group information
class GroupView(View):
    
    dbname = acme_services_config.get("db_options","dbname")
    dbuser = acme_services_config.get("db_options","dbuser")
    dbpassword = acme_services_config.get("db_options","dbpassword")
    isConnectedToDB = acme_services_config.get("db_options","isConnectedToDB")
    
    
    def get(self, request, username):
        
        self.isConnectedToDB = acme_services_config.get("db_options","isConnectedToDB")
        logger.debug('isConnected: ' + str(self.isConnectedToDB))
        
        
        
        if self.isConnectedToDB == "True":
            try:
                print 'in true'
                import psycopg2
                conn=psycopg2.connect("dbname='" + dbname + "' user='" + dbuser + "' password='" + dbpassword + "'")
                cur = conn.cursor()
                
            except:
                print 'in connected to DB except'
                tb = traceback.format_exc()
                print tb
                pass
            return HttpResponse("Connected\n")
        
        else:
            
            return HttpResponse("Not Connected\n")
        
        '''
        if isConnectedToDB == "True":
        
            try:
            
                import psycopg2
                
                conn=psycopg2.connect("dbname='" + dbname + "' user='" + dbuser + "' password='" + dbpassword + "'")
                cur = conn.cursor()
                
                
                user_id = get_user_id(username)

                print 'user_id: ' + user_id    
            
                group_id_list_set = get_group_id_list_set(user_id)
            
                group_name_list_set = get_group_name_list_set(group_id_list_set)
            
                groups_response = group_name_list_set
                
            
                return HttpResponse("Connected\n")
            
            except:
                print 'in connected to DB except'
                tb = traceback.format_exc()
                print tb
                return HttpResponse("Not Connected\n")
        
        else:
            groups_response = []
            if populate_groups == "True":
                groups_response.append('ACME')
                groups_response.append('CSSEF')
            data = {'groups' : groups_response}
        
            data_string = notConnectedResponse()
            return HttpResponse(data_string + '\n')
    
        '''


'''
def notConnectedResponse():
    
    groups_response = []
    if populate_groups == "True":
        groups_response.append('ACME')
        groups_response.append('CSSEF')
    data = {'groups' : groups_response}

    data_string = json.dumps(data,sort_keys=False,indent=2)    

    return data_string
'''
