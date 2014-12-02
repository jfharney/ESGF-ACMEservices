from django.http import HttpResponse
# Create your views here.


import json

print 'loading view'

isConnectedToDB = False

dbname = 'esgcet'
dbuser = 'dbsuper'
dbpassword = 'esg4ever'


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
	