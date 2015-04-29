
import urllib2 


def useFileHttp(request,user_id):
      path = request.GET.get('path')
    #print "http://" + serviceHost + ":" + servicePort + "/sws/files?uid=" + user_id + '&path=' + path + '&list=retrieve'
      data = urllib2.urlopen("http://" + serviceHost + ":" + servicePort + "/sws/files?uid=" + user_id + '&path=' + path + '&list=retrieve').read()
      
      #print 'data from url call: ' + data
      jsonObj = json.loads(data)
      respArr = []
      
      #print 'jsonObj: ' + str(jsonObj)
      t = 'files' in jsonObj
      #print 't--->' + str(t)
      
      res = ''
      
      files = {}
      if t:
          files = jsonObj['files']
          
          res += '['
      
          if files:
              #print 'files.length: ' + str(len(files))
              counter = 0
              for file in files:
                  counter = counter + 1
                  #print 'sending path: ' + path
                  obj = createDynatreeJSONObjStr(file,path)
                  
                  res += obj
                  if counter < len(files):
                      res += ' , '
                  
              res += ']'
              
      else:
          res += '[{'
          
          res += '"title" : ' + '"' + path + '|' + jsonObj['name'] + '",'     
        
          if jsonObj['type'] == 5:
            
            res += '"isFolder" : ' + 'true,'
            res += '"isLazy" : ' + 'true,'       
                         
          else: 
            res += '"isFolder" : ' + 'false,'
            res += '"isLazy" : ' + 'false,'
            
          res += '"path" : "' + path + '|' + jsonObj['name'] + '",'
          res += '"nid" : "' + str(jsonObj['nid']) + '"'    
          res += '}]'
      
      
      return res
      
      #print '\n\nstr res: ' + res
    
     

def createDynatreeJSONObjStrFile():
    
    return "hello"
 
def createDynatreeJSONObjStr(file,path):
    
    #res += '{ "title": "Node 1", "key": "k1", "isLazy": true },'
     
    res = '{' 
      
    #print 'file str: ' + str(file)
    dynatreeJSONObj = {}
              
    if path == '|':
                  
        #dynatreeJSONObj['title'] = "|" + file['name']
        res += '"title" : ' + '"|' + file['name'] + '",'     
        if file['type'] == 5:
            res += '"isFolder" : ' + 'true,'
            res += '"isLazy" : ' + 'true,'
            #dynatreeJSONObj['isFolder'] = 'true'
            #dynatreeJSONObj['isLazy'] = 'true'
        else:
            res += '"isFolder" : ' + 'false,'
            res += '"isLazy" : ' + 'false",'
            #dynatreeJSONObj['isFolder'] = 'false'
            #dynatreeJSONObj['isLazy'] = 'false'
        
        res += '"path" : "|' + file['name'] + '",'
        res += '"nid" : "' + str(file['nid']) + '"'
        dynatreeJSONObj['path'] = '|' + file['name']
        dynatreeJSONObj['nid'] = file['nid']
              
    else:
                  
        dynatreeJSONObj['title'] = path + '|' + file['name']
        res += '"title" : ' + '"' + path + '|' + file['name'] + '",'     
        
        if file['type'] == 5:
            
            res += '"isFolder" : ' + 'true,'
            res += '"isLazy" : ' + 'true,'          
            dynatreeJSONObj['isFolder'] = 'true'
            dynatreeJSONObj['isLazy'] = 'true'
                         
        else: 
            res += '"isFolder" : ' + 'false,'
            res += '"isLazy" : ' + 'false,'
            dynatreeJSONObj['isFolder'] = 'false'
            dynatreeJSONObj['isLazy'] = 'false'
            
        res += '"path" : "' + path + '|' + file['name'] + '",'
        res += '"nid" : "' + str(file['nid']) + '"'    
        dynatreeJSONObj['path'] = path + '|' + file['name'];
        dynatreeJSONObj['nid'] = file['nid'];  
      
    
    res += '}'
    return res 
