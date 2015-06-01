from django.test import TestCase


# Create your tests here.
class dbTests(TestCase):
    
        
    def test_isConnectedToDB(self):
        
        import ConfigParser
        acme_services_config = ConfigParser.ConfigParser()
        acme_services_config.read('ACMEservices.cfg')
        
        dbname = acme_services_config.get("db_options","dbname")
        dbuser = acme_services_config.get("db_options","dbuser")
        dbpassword = acme_services_config.get("db_options","dbpassword")
        isConnectedToDB = acme_services_config.get("db_options","isConnectedToDB")
        
        a = 1
        b = 1
        
        #test to see if 
        
        self.assertEqual(a,b)