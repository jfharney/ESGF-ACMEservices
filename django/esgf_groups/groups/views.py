from django.http import HttpResponse
# Create your views here.


import json


import ConfigParser
config = ConfigParser.ConfigParser()
config.read('ACMEservices.cfg')

import ast
isConnectedToDB = ast.literal_eval(config.get("db_options","isConnectedToDB"))
print 'isConnectedToDB: ' + str(isConnectedToDB)


dbname = 'esgcet'
dbuser = 'dbsuper'
dbpassword = 'esg4ever'

prefix = config.get("db_options","prefix")
esgini_location = config.get("db_options","esgini_location")
esgini_location2 = config.get("db_options","esgini_location2")



def get_user_id(username): 
	conn=psycopg2.connect("dbname='esgcet' user='dbsuper' password='esg4ever'")
	cur = conn.cursor()
		
	user_id = ''
	try: 
		query = "select * from esgf_security.user where username='" + username + "';"
		#print 'query: ' + query
		cur.execute("select * from esgf_security.user where username='" + username + "';")
		rows = cur.fetchall()
		#print 'getting user_id from username: ' +  username
		user_id = str(rows[0][0])
		#print 'user_id: ' + user_id
	except:
		print 'I cannot select ' + user_id + ' from esgf_security'
		return HttpResponse('username: ' + username + ' not found')
	
	return user_id

def get_group_id_list_set(user_id):
	group_id_list_set = []		
	try:
		query = "SELECT group_id from esgf_security.permission where user_id='" + user_id + "';"
		#print 'query: ' + query
		cur.execute("SELECT group_id from esgf_security.permission where user_id='" + user_id + "';")
		rows = cur.fetchall()
		group_id_list = []
		for row in rows:
				
			group_id_list.append(row[0])
				
		group_id_list_set = list(set(group_id_list))
			#print 'type: ' + str(type(group_id_list_set))	
	except:		
		print 'exception in permission table'
		
	return group_id_list_set


 user_id | group_id | role_id | approved 
---------+----------+---------+----------
       2 |        3 |       6 | t
       2 |        7 |       4 | t
       2 |        7 |       6 | t


def get_group_name_list_set(group_id_list_set):
	group_name_list_set = []

	try:
		temp_list = []
		for group_id in group_id_list_set:
			query = "SELECT name from esgf_security.group where id='" + str(group_id) + "';"
			#print 'query: ' + query
			cur.execute(query)
			rows = cur.fetchall()
			for row in rows:
				group_name = rows[0]
				print '   type: ' + str(type(group_name))
				#group_name_list_set.append(group_name)
				temp_list.append(str(group_name[0]))

				
		group_name_list_set = list(set(temp_list))

	except:
		print 'exception in group table'
		
	return group_name_list_set
	

def groups(request,username):


	if isConnectedToDB:
		
		import psycopg2
		print 'in esg.ccs.ornl.gov groups'

		groups_response = []
	
		try:
			print 'in try'
		
			conn=psycopg2.connect("dbname='" + dbname + "' user='" + dbuser + "' password='" + dbpassword + "'")
			cur = conn.cursor()
		
			user_id = get_user_id(username)

			print 'user_id: ' + user_id	
		
			group_id_list_set = get_group_id_list_set(user_id)
		
			group_name_list_set = get_group_name_list_set(group_id_list_set)
		
			groups_response = group_name_list_set
		
		except:
			print 'in  except'
		

 		data = {'groups' : groups_response}
 	 	data_string = json.dumps(data,sort_keys=False,indent=2)	
	
		return HttpResponse(data_string + '\n')

	else:
		
		
		groups_response = []
		groups_response.append('ACME')
		groups_response.append('CSSEF')
		data = {'groups' : groups_response}
		
 	 	data_string = json.dumps(data,sort_keys=False,indent=2)	
		return HttpResponse(data_string + '\n')


def roles(request,username):
	if isConnectedToDB:
		print 'connected'
	
	
	else:
		print 'is not connected'
		
		
		#get the username
		
		
		return HttpResponse('roles' + '\n')


import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise




def make_publish_directory(request):
	
	#load the json object
	import json 
	
	print str(request.body)
	
	json_data = json.loads(request.body)
	
	#directory_format = /data/acme/projects/%(project)s/%(data_type)s/%(experiment)s/%(versionnum)s/%(realm)s/%(regridding)s/%(range)s
	project = None
	data_type = None
	experiment = None
	versionnum = None
	realm = None
	regridding = None
	range = None

	for key in json_data:
		print 'key: ' + key
		
		if key == 'project':
			project = json_data[key]
		
		if key == 'data_type':
			data_type = json_data[key]
			
		if key == 'experiment':
			experiment = json_data[key]
		
		if key == 'versionnum':
			versionnum = json_data[key]
		
		if key == 'realm':
			realm = json_data[key]
		
		if key == 'regridding':
			regridding = json_data[key]
		
		if key == 'range':
			range = json_data[key]
	
	print 'project: ' + str(project) + ' ' + str(project == None)
	print 'data_type: ' + str(data_type) + ' ' + str(data_type == None)
	print 'experiment: ' + str(experiment) + ' ' + str(experiment == None)
	print 'versionnum: ' + str(versionnum) + ' ' + str(versionnum == None)
	print 'realm: ' + str(realm) + ' ' + str(realm == None)
	print 'regridding: ' + str(regridding) + ' ' + str(regridding == None)
	print 'range: ' + str(range) + ' ' + str(range == None)
	
	print 'falkse? ' + str((project == None) or (data_type == None) or (experiment == None) or (versionnum == None) or (realm == None) or (regridding == None) or (range == None))
			
	if (project == None) or (data_type == None) or (experiment == None) or (versionnum == None) or (realm == None) or (regridding == None) or (range == None):
		return "error"
	else:
		return make_publish_directory_helper(project,data_type,experiment,versionnum,realm,regridding,range)



def make_publish_directory_helper(project,data_type,experiment,versionnum,realm,regridding,range):
	
	#make the directory /data/acme/projects/ACME/
	
	path = prefix + '/' + project + '/' + experiment + '/' + versionnum + '/' + realm + '/' + regridding + '/' + range
	
	mkdir_p(path)
	
	return "success"
		
#for GET:
#curl -X GET http://localhost:8081/groups/publish/8xo
#for POST:
#echo '{"dataset" : test}' | curl -d @- 'http://localhost:8081/groups/publish/8xo' -H "Accept:application/json" -H "Context-Type:application/json"
def publish(request,username):
	
	print 'in publish'
	
	
	
	if request.method == 'POST':
	
		print 'in POST'
		
		#make the directory (if it doesnt exist) from the facets
		#otherwise return an error message
		if make_publish_directory(request) == "success":
			
			#append to the esg.ini file
			txt = open(esgini_location)
			
			print txt.read()
			with open(esgini_location) as f:
				lines = f.readlines()
			
			
       			print 'len: ' + str(len(lines))
    		
			return HttpResponse('success\n')
		else:
			
			
			
			
			return HttpResponse('error\n')
		
		
		
		
	
		
	elif request.method == 'GET':
		
		print 'in GET'
	
	
	
	return HttpResponse('publish\n')


#Both reads and writes basic facets

#for GET:
#curl -X GET http://localhost:8081/groups/base_facets/jfharney
#for POST:
#echo '{"realm": "lndice"}' | curl -d @- 'http://localhost:8081/groups/base_facets/jfharney?project=ACME' -H "Accept:application/json" -H "Context-Type:application/json"
#output:
#
#  
#
def base_facets(request,username):
	
	if request.method == 'POST':
	
		print 'in POST'
		
		project = ''
		if not request.GET.get('project') == None:
			
			project = str(request.GET.get('project')).strip()
			
		else:
			project = 'ACME'
		
		import json
		
		
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
		
		
		write_facet_values(project,facet_arr,facet_values_arr)
		
		return HttpResponse("In POST\n")
	
	else:
		
	
		#should read from the query parameters
		project = ''
		if not request.GET.get('project') == None:
			
			project = str(request.GET.get('project')).strip()
			
		else:
			project = 'ACME'
		
		
		import ConfigParser
		config = ConfigParser.ConfigParser()
		config.read(esgini_location)
		
		categories_value = config.get("project:" + project,"categories")
		
		
		categories_list = categories_value.split("\n")
		#print str(categories_list)
		
		categories = []
		for category_values in categories_list:
			if "|" in category_values:
				category_list = category_values.split("|")
				category = category_list[0].strip()
				
				category_options = category + '_options'
				category_options = category_options.strip()
				
				options = config.get("project:" + project,category_options)
				
				if category == 'project':
					print 'project processing different'
					obj = { "project" : project }
					categories.append(obj)
					
				elif category == 'experiment':
					print 'extra experiment processing here'
					
					exp_options = options.split('\n')
					print str(exp_options)
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
					print 'category: ' + category + ' options: ' + options
					
					obj = { category : options }
					categories.append(obj)
				#categories.append(category)
		
				
		import json
		categories_json = json.dumps(categories,sort_keys=False,indent=2)
	    
		print str(categories_json)		
		
		
		
		
	 	return HttpResponse(categories_json)
 		
 		
 		
#writes to esg.ini file given project, array of facet names and their associated values
def write_facet_values(project,facet_arr,facet_values_arr):
	
	print 'project: ' + project + ' facet_arr: ' + str(facet_arr) + ' facet_values_arr: ' + str(facet_values_arr)
	
	#for key in facet_json:
	#	print 'key: ' + key + ' facet_json: ' + facet_json[key]
	
	from ConfigParser import SafeConfigParser
	import sys
	
	parser = SafeConfigParser()
	parser.read(esgini_location)
	
	
	project_header = "project:" + project
	
	if type(facet_values_arr)==type(list()):
		print 'list'
	else:
		print 'not list'
	
	for i in range(0,len(facet_arr)):
		print 'i: ' + str(i)
		#grab the options line header
		options_line = str(facet_arr[i]+"_options")
		
		#if the facet_option doesnt exist then skip (for now)
		try:
			print 'options line: ' + options_line + ' options line values: ' + str(parser.get(project_header, options_line) )
			
			
			
			
			#check to see if the option exists already
			#if so, then skip
			#if not facet_values_arr[i].strip() in parser.get(project_header, options_line):
				#print 'doesnt already exist'
				#create new string for values of the options line
			
			new_facet_values = parser.get(project_header, options_line)
			facet_values = facet_values_arr[i]
			for j in range(0,len(facet_values)):
			
				if not facet_values[j].strip() in new_facet_values:
					new_facet_values = new_facet_values + ',' + facet_values[j].strip()
				else:
					print 'already exists'
			
			print 'new_facet_values: ' + new_facet_values
			#set the values 
			parser.set(project_header, options_line, new_facet_values)
	
			#else:
			#	print 'already exists'
		
			
			
		except: 
			print 'error'
			pass
		
	
	#write changes out
	f = open(esgini_location, 'w') 
	
	
	
	parser.write(f)
	
	
	f.close()
		










'''
		parser.add_section('bug_tracker22')
		parser.set('bug_tracker22', 'url', 'http://localhost:8080/bugs')
		parser.set('bug_tracker22', 'username', 'dhellmann')
		parser.set('bug_tracker22', 'password', 'secret')
'''


'''
	txt = open(esgini_location)
	lines = []
	with open(esgini_location) as f:
		lines = f.readlines()
			
 	print 'len: ' + str(len(lines))			
 	
 	project = 'ACME'
 	
 	projectFlag = False
 	buffer = []
 	for line in lines:
 		#print 'line: ' + line
 		
 		#first identify the 
 		if "[project:" + project + "]" in line:
 		
 			#print 'begin project'
 			projectFlag = True
 		
 		if "[project:" in line and str(project + "]") not in line:
 			#print 'end project'
 			projectFlag = False
 		
 		if projectFlag:
 			buffer.append(line)
 	
 	
 	#get the categories here
 	categoriesFlag = False
 	categories = []
 	for bufferline in buffer:
 		
 	 	#print 'firstchar: ' + bufferline[0] + ' ... line: ' + str(bufferline)
 	 	
 	 	
 	 	print str(bufferline[0] == '\t') + ' ' + str(bufferline[0] == ' ') + ' ' + str(categoriesFlag == True) + ' ' + str((bufferline[0] == '\t' or bufferline[0] == ' ') and (categoriesFlag == True))
 	 	 	
 	 	if (bufferline[0] == '\t' or bufferline[0] == ' ') and (categoriesFlag == True):
 	 		#print 'firstchar indicates category'
 	 		if "|" in bufferline:
 	 			category = bufferline.split('|')[0]
 	 			print 'appending ' + category
 	 			categories.append(category.strip())
 	 	else:
 	 		
 	 		categoriesFlag = False
 	 		
 	 		print 'firstchar indicates done category'
 	 
 	 	
 	 	if "categories =" in bufferline: 
 	 	 	print 'found categories ='
 	 	 	categoriesFlag = True
 	 	
 	
 	print 'categories: ' + str(categories)
 	
 	category_opts_arr = []
 	
 	#add project to the arr
 	obj = { 'project' : 'ACME'}
 	category_opts_arr.append(obj)
 	inExperimentFlag = False
 	for bufferline in buffer:
 		#print 'bufferline: ' + bufferline
 		
 		for category in categories:
 			print "\t" + str(category + "_options")  + ' ' +  str(str(category + "_options") in bufferline)
 			if str(category + "_options") in bufferline and not bufferline[0] == "#":
 				print 'category: ' + category + ' is in bufferline, extract the values '
 				
 				if (bufferline[0] == '\t' or bufferline[0] == ' ') and (inExperimentFlag == True):
 					print 'found another property'
 					inExperimentFlag = True
 				elif (not (bufferline[0] == '\t' or bufferline[0] == ' ')) and (inExperimentFlag == True):
 					inExperimentFlag = True
 				if category == "experiment":
 					print 'handle experiment different'
 					inExperimentFlag = True
 					
 					
 				else:
 				 	bufferline_opts = bufferline.split("=")
 				 	print 'extracting and appending: ' + str(bufferline_opts[1]).strip()
 				 	obj = { category : str(bufferline_opts[1]).strip() }
 				 	category_opts_arr.append(obj)
 				 	print 'new arr: ' + str(category_opts_arr)
 	
 	
 	print 'categories options: ' + str(category_opts_arr) + ' ' + str(len(category_opts_arr))
 '''
	