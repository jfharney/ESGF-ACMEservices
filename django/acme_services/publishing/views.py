# Create your views here.
from django.http import HttpResponse
# Create your views here.


import json



import ConfigParser
acme_services_config = ConfigParser.ConfigParser()
acme_services_config.read('ACMEservices.cfg')


#for GET:
#curl -X POST http://localhost:8081/acme_services/publishing/publish_data/jfharney
#for POST:
#echo '{"realm": "lndice"}' | curl -d @- 'http://localhost:8081/groups/base_facets/jfharney?project=ACME' -H "Accept:application/json" -H "Context-Type:application/json"

def publish_data(request,username):
    
    
    
    return HttpResponse('Published')




#Both reads and writes basic facets

#for GET:
#curl -X GET http://localhost:8081/acme_services/publishing/base_facets/jfharney
#for POST:
#echo '{"realm": "lndice"}' | curl -d @- 'http://localhost:8081/groups/base_facets/jfharney?project=ACME' -H "Accept:application/json" -H "Context-Type:application/json"
#output:
#
#  
#
def base_facets(request,username):
    
    
    if request.method == 'POST':
    
        print 'in POST'
        
        
        
        
        base_facets_put(request)
        
        return HttpResponse("In POST\n")
    
    else:
        
        
        #should read from the query parameters
        project = ''
        if not request.GET.get('project') == None:
            
            project = str(request.GET.get('project')).strip()
            
        else:
            project = 'ACME'
        
        #assemble the categories (i.e. facets) into an object to be returned
        categories_json = base_facets_get(project)       
        
        
        return HttpResponse(categories_json)

def base_facets_put(request):
    import json
        
    project = ''
    if not request.GET.get('project') == None:
        
        project = str(request.GET.get('project')).strip()
        
    else:
        project = 'ACME'
        
    print 'request.body: ' + str(request.body)
    
    json_data = json.loads(request.body)
    
    facet_arr = []
    facet_values_arr = []
    
    
    for key in json_data:
        print 'key: ' + key + ' value: ' + str(json_data[key])
        facet = key
        facet_values = json_data[key]
        
        facet_arr.append(facet)
        facet_values_arr.append(facet_values)
    
    
    #write_facet_values(project,facet_arr,facet_values_arr)
    

def base_facets_get(project):
    
    
    #import ConfigParser
    esgini_location = acme_services_config.get("esg_ini_options","esgini_location")
    config = ConfigParser.ConfigParser()
    config.read(esgini_location)
    
    categories_value = config.get("project:" + project,"categories")
    
    #grab a listing of the categories associated with the project
    categories_list = categories_value.split("\n")
    
    categories = getOutput(config,project,categories_list,2)
    
    import json
    categories_json = json.dumps(categories,sort_keys=False,indent=2)
    
    return categories_json


'''
output type 1 gives this format

{
    "project": "ACME", 
    "data_type": "climo,h,h0,dd", 
    "experiment": "B1850C5_ne30gx1_tuning,B1850C5e1_ne30", 
    "realm": "atm,ice,lnd,ocn,all,ATM,lndice", 
    "versionnum": "v0_1,v01,HIGHRES,pre-v0", 
    "regridding": "bilinear,downscaled,native,fv257x512", 
    "range": "all_dir,all,2-9,10-19,20-29,30-39,30-50,40-49,ALL"
}
output type 2 gives this format

{
  "realm": [
    "atm", 
    "ice", 
    "lnd", 
    "ocn", 
    "all", 
    "ATM", 
    "lndice"
  ], 
  "data_type": [
    "climo", 
    "h", 
    "h0", 
    "dd"
  ], 
  "versionnum": [
    "v0_1", 
    "v01", 
    "HIGHRES", 
    "pre-v0"
  ], 
  "project": [
    "ACME"
  ], 
  "range": [
    "all_dir", 
    "all", 
    "2-9", 
    "10-19", 
    "20-29", 
    "30-39", 
    "30-50", 
    "40-49", 
    "ALL"
  ], 
  "experiment": [
    "B1850C5_ne30gx1_tuning", 
    "B1850C5e1_ne30"
  ], 
  "regridding": [
    "bilinear", 
    "downscaled", 
    "native", 
    "fv257x512"
  ]
}

output type 3 gives this format
[
  {
    "project": "ACME"
  }, 
  {
    "data_type": "climo,h,h0,dd"
  }, 
  {
    "experiment": "B1850C5_ne30gx1_tuning,B1850C5e1_ne30"
  }, 
  {
    "realm": "atm,ice,lnd,ocn,all,ATM,lndice"
  }, 
  {
    "versionnum": "v0_1,v01,HIGHRES,pre-v0"
  }, 
  {
    "regridding": "bilinear,downscaled,native,fv257x512"
  }, 
  {
    "range": "all_dir,all,2-9,10-19,20-29,30-39,30-50,40-49,ALL"
  }
]
'''
'''

'''
def getOutput(config,project,categories_list,type):
    
    if type == 3:
        #get the list of category values in that project
        categories = []
        for category_values in categories_list:
            
            #test if the pipe | is in the category value (denoting a valid cateogry)
            if "|" in category_values:
                category_list = category_values.split("|")
                category = category_list[0].strip()
                
                category_options = (category + '_options').strip()
                #category_options = category_options.strip()
                
                options = config.get("project:" + project,category_options)
                
                #need to handle project and experiment differently
                #project because that is defined earlier in the document
                #experiment because that is defined with multi-level descriptions
                if category == 'project':
                    obj = { "project" : project }
                    categories.append(obj)
                    
                elif category == 'experiment':
                    
                    exp_options = options.split('\n')
                    exp_option_names = []
                    for exp_option in exp_options:
                        if "|" in exp_option:
                            exp_option_arr = exp_option.split("|")
                            exp_option_name = exp_option_arr[1]
                            exp_option_names.append(exp_option_name.strip())
                    
                    exp_option_str = ",".join(exp_option_names)        
                    obj = { "experiment" : exp_option_str }
                    categories.append(obj)
                    
                else:
                    obj = { category : options }
                    categories.append(obj)
        return categories
    
    elif type == 2:
        #get the list of category values in that project
        categories = {}
        for category_values in categories_list:
        
        #test if the pipe | is in the category value (denoting a valid cateogry)
            if "|" in category_values:
                category_list = category_values.split("|")
                category = category_list[0].strip()
                
                category_options = (category + '_options').strip()
                #category_options = category_options.strip()
                
                options = config.get("project:" + project,category_options)
                
                #need to handle project and experiment differently
                #project because that is defined earlier in the document
                #experiment because that is defined with multi-level descriptions
                if category == 'project':
                    #obj = { "project" : project }
                    project_arr = []
                    project_arr.append(project)
                    categories['project'] = project_arr
                    
                elif category == 'experiment':
                    
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
                    print 'category: ' + category + ' options: ' + options
                    
                    categories[category] = options.split(',')
                    #obj = { category : options }
                    #categories.append(obj)
        return categories         
             
    elif type == 1:
        #get the list of category values in that project
        categories = {}
        for category_values in categories_list:
        
        #test if the pipe | is in the category value (denoting a valid cateogry)
            if "|" in category_values:
                category_list = category_values.split("|")
                category = category_list[0].strip()
                
                category_options = (category + '_options').strip()
                #category_options = category_options.strip()
                
                options = config.get("project:" + project,category_options)
                
                #need to handle project and experiment differently
                #project because that is defined earlier in the document
                #experiment because that is defined with multi-level descriptions
                if category == 'project':
                    #obj = { "project" : project }
                    categories['project'] = project
                    
                elif category == 'experiment':
                    
                    exp_options = options.split('\n')
                    exp_option_names = []
                    for exp_option in exp_options:
                        if "|" in exp_option:
                            exp_option_arr = exp_option.split("|")
                            exp_option_name = exp_option_arr[1]
                            exp_option_names.append(exp_option_name.strip())
                    
                    exp_option_str = ",".join(exp_option_names)        
                    #obj = { "experiment" : exp_option_str }
                    categories['experiment'] = exp_option_str
                    
                else:
                    print 'category: ' + category + ' options: ' + options
                    categories[category] = options
                    #obj = { category : options }
                    #categories.append(obj)
        return categories         
             

    
    
         