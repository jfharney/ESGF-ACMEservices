from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View

import json
import ConfigParser
import traceback

acme_services_config = ConfigParser.ConfigParser()
acme_services_config.read('ACMEservices.cfg')

esgini_location = acme_services_config.get("esg_ini_options","esgini_location")
esgini = ConfigParser.ConfigParser()
esgini.read(esgini_location)

import logging
logger = logging.getLogger("publication")
logger.setLevel(logging.DEBUG)

# create the logging file handler
publication_log_file = acme_services_config.get("loggers","publication_log_file")
fh = logging.FileHandler(publication_log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add handler to logger object
logger.addHandler(fh)


# Create your views here.

class FacetsView(View):
    
    #import ConfigParser
    esgini_location = acme_services_config.get("esg_ini_options","esgini_location")
    project = "ACME"
    
    
    #given 
    def get(self, request, username):
        
        facet_config = ConfigParser.ConfigParser()
        facet_config.read(self.esgini_location)
    
        categories_value = facet_config.get("project:" + self.project,"categories")
    
        #logger.debug(str(categories_value)) 

        categories_list = categories_value.split("\n")
        
        #logger.debug(str(categories_list))
        
        #categories = self.getOutput(self,facet_config,self.project,categories_list)
    
        categories = {}
        
        
        for category_values in categories_list:
            logger.debug('category_values: ' + category_values)
            
            #test if the pipe | is in the category value (denoting a valid cateogry)
            if "|" in category_values:
                #logger.debug('\tvalid category')
                
                category_list = category_values.split("|")
                category = category_list[0].strip()
                category_options = (category + '_options').strip()
                logger.debug('category_options: ' + category_options) 
                
                 
                #need to handle project and experiment differently
                #project because that is defined earlier in the document
                #experiment because that is defined with multi-level descriptions
                if category == 'project':
                    project_arr = []
                    print 'str: ' + str(project_arr)
                    project_arr.append(str(self.project))
                    categories['project'] = project_arr
                 
                elif category == 'experiment':
                    
                    options = facet_config.get("project:" + self.project,category_options)
                    
                    exp_options = options.split('\n')
                    exp_option_names = []
                    for exp_option in exp_options:
                        if "|" in exp_option:
                            exp_option_arr = exp_option.split("|")
                            exp_option_name = exp_option_arr[1]
                            exp_option_names.append(exp_option_name.strip())
                    
                    exp_option_str = ",".join(exp_option_names)        
                    #obj = { "experiment" : exp_option_str }
                    categories['experiment'] = exp_option_names#exp_option_str
                
                else:
                    
                    options = facet_config.get("project:" + self.project,category_options)
                    print 'category: ' + category + ' options: ' + options
                    
                    categories[category] = options.split(',')
                  
                
        categories_json = json.dumps(categories,sort_keys=False,indent=2)
        
        
        return HttpResponse(categories_json)
    
    
    #POST: "Replaces" facet options
    #for POST:
    #
    #curl example:
    #curl -i -H "Accept: application/json" -X POST -d "experiment=ACME | B1850C5e1_ne30 | experiment ne30 C6" http://localhost:8000/acme_services/publishing/facets/jfharney
    #
    def post(self, request, username):
        
        from django.http import QueryDict
        post_body = QueryDict(str(request.body))
        
        
        project_header = "project:" + self.project
        
        facet_arr = []
        facet_values_arr = []
        
        from ConfigParser import SafeConfigParser
        import sys
    
        parser = SafeConfigParser()
        parser.read(self.esgini_location)
    
        #get listing of facets
        
        
        for key in post_body:
            
            facet = key
            
            #have to use getlist because some values may be arrays
            facet_values = post_body.getlist(key)
                    
            print 'facet: ' + facet
            
            options_line = str(facet+"_options")
            #print 'options line: ' + options_line + ' options line values: ' + str(parser.get(project_header, options_line) )
                
            old_facet_values = parser.get(project_header, options_line)
            print 'old_facet_values: ' + str(old_facet_values)           
            
            
            if facet == 'experiment':
                print 'have to handle experiment differently'
                
                try:
                
                    old_facet_values_list = old_facet_values.split('\n')
                    print 'old_facet_values: ' + str(old_facet_values_list)
                    new_facet_values_list = convertUnicode(facet_values)
                    print 'new_facet_values: ' + str(new_facet_values_list)
                    
                    #add lists together (eliminate duplicates)
                    appended_list = new_facet_values_list#trimList(list(set(old_facet_values_list+new_facet_values_list)))
                    print 'appended list: ' + str(appended_list)
                    
                    parser.set(project_header, options_line, ('\n').join(appended_list))
                    print parser.get(project_header, facet + '_options')
                    
                    #write changes out
                    f = open(esgini_location, 'w') 
                    parser.write(f)
                    f.close()
                    
                    
                    
                except:
                    print 'in except for options line'
                    tb = traceback.format_exc()
                    print tb
                    pass
                    
            else:
                
                try:
                    
                    #convert to list
                    old_facet_values_list = old_facet_values.split(',')
                    
                        
                    print 'old_facet_values: ' + str(old_facet_values_list)
                    new_facet_values_list = convertUnicode(facet_values)
                    print 'new_facet_values: ' + str(new_facet_values_list)
                    
                    #add lists together (eliminate duplicates)
                    appended_list = new_facet_values_list#list(set(old_facet_values_list+new_facet_values_list))
                    print 'appended list: ' + str(appended_list)
                    
                    parser.set(project_header, options_line, (',').join(appended_list))
        
                    print parser.get(project_header, 'data_type_options')
                    
                    #write changes out
                    f = open(esgini_location, 'w') 
                    parser.write(f)
                    f.close()
                    
                    
                except:
                    print 'in except for options line'
                    tb = traceback.format_exc()
                    print tb
                    pass
                
            
            
    
    
        
        
        return HttpResponse("End post\n")
    
    
    #PUT: "Appends" facet options
    #curl -i -H "Accept: application/json" -X PUT -d "experiment=ACME | B1851C5e1_ne30 | experiment ne30 C5" http://localhost:8000/acme_services/publishing/facets/jfharney 
    #
    def put(self, request, username):
        
        
        
        from django.http import QueryDict
        put_body = QueryDict(str(request.body))
        
        
        project_header = "project:" + self.project
        
        facet_arr = []
        facet_values_arr = []
        
        from ConfigParser import SafeConfigParser
        import sys
    
        parser = SafeConfigParser()
        parser.read(self.esgini_location)
    
        #get listing of facets
        
        
        for key in put_body:
            
            facet = key
            
            #have to use getlist because some values may be arrays
            facet_values = put_body.getlist(key)
                    
            logger.debug( 'facet: ' + facet )
            
            options_line = str(facet+"_options")
            #print 'options line: ' + options_line + ' options line values: ' + str(parser.get(project_header, options_line) )
                
            old_facet_values = parser.get(project_header, options_line)
            logger.debug( 'old_facet_values: ' + str(old_facet_values) )      
            
            
            if facet == 'experiment':
                
                try:
                
                    old_facet_values_list = old_facet_values.split('\n')
                    logger.debug( 'old_facet_values: ' + str(old_facet_values_list) )
                    new_facet_values_list = convertUnicode(facet_values)
                    logger.debug( 'new_facet_values: ' + str(new_facet_values_list) )
                    
                    #add lists together (eliminate duplicates)
                    appended_list = trimList(list(set(old_facet_values_list+new_facet_values_list)))
                    logger.debug( 'appended list: ' + str(appended_list) )
                    
                    parser.set(project_header, options_line, ('\n').join(appended_list))
                    logger.debug( parser.get(project_header, facet + '_options') )
                    
                    #write changes out
                    f = open(esgini_location, 'w') 
                    parser.write(f)
                    f.close()
                    
                    
                    
                except:
                    
                    tb = traceback.format_exc()
                    logger.debug( tb )
                    pass
                    
            else:
                
                
                
                
                try:
                    
                    #convert to list
                    old_facet_values_list = old_facet_values.split(',')
                    
                        
                    logger.debug( 'old_facet_values: ' + str(old_facet_values_list) )
                    new_facet_values_list = convertUnicode(facet_values)
                    logger.debug( 'new_facet_values: ' + str(new_facet_values_list) )
                    
                    #add lists together (eliminate duplicates)
                    appended_list = list(set(old_facet_values_list+new_facet_values_list))
                    logger.debug( 'appended list: ' + str(appended_list) )
                    
                    parser.set(project_header, options_line, (',').join(appended_list))
        
                    logger.debug( parser.get(project_header, 'data_type_options') )
                    
                    #write changes out
                    f = open(esgini_location, 'w') 
                    parser.write(f)
                    f.close()
                    
                    
                except:
                    tb = traceback.format_exc()
                    logger.debug( tb )
                    pass
                
            
            
        
        return HttpResponse("End put\n")
    
    
    
    def delete(self, request, username):
        
        
        
        return HttpResponse("End delete\n")
    



def convertUnicode(list):
    print 'in convert Unicode'
    new_list = []
    for element in list:
        print 'element: ' + element
        new_list.append(element.encode('utf8'))
    return new_list
                
def trimList(list):
    
    for item in list:
        if item == '':
            list.remove(item)
    return list

def getOutput(self,facet_config,project,categories_list):
        
    return ''


'''  
def getOutput(facet_config,project,categories_list):
    
    
    
    categories = []
    for category_values in categories_list:
        logger.debug('category_values: ' + category_values)
        
        #test if the pipe | is in the category value (denoting a valid cateogry)
        if "|" in category_values:
            logger.debug('\tvalid category')
            
            category_list = category_values.split("|")
            category = category_list[0].strip()
            logger.debug('category: ' + category) 
            category_options = (category + '_options').strip()
            options = facet_config.get("project:" + project,category_options)
                
            
        
    return ''
'''