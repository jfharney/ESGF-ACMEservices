from django.http import HttpResponse
# Create your views here.

print 'loading view'

def groups(request,username):

	import psycopg2
	print 'in esg.ccs.ornl.gov groups'

	groups_response = []
        try:
		
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

		print 'user_id: ' + user_id
		


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
		


		#print 'group_id_list_set: ' + str(group_id_list_set) + ' type: ' + str(type(group_id_list_set)) + ' length: ' + str(len(group_id_list_set))		
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

		groups_response = group_name_list_set

	except:
		print 'I am unable to connect to the database'

	import json

 	data = {'groups' : groups_response}
    	data_string = json.dumps(data,sort_keys=False,indent=2)	

	return HttpResponse(data_string + '\n')


