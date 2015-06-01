class Critter(object):
    
    total = 0
    
    def __init__(self,name):
        print 'a new critter has been born'
        self.name = name
        Critter.total += 1
    
    def talk(self):
        print 'Hi Im ' + self.name
        
    def __str__(self):
        return 'Critter Object\nname: ' + self.name + '\n'
    
    @staticmethod
    def status():
        print 'total number: ' + str(Critter.total)
        

crit1 = Critter("p")
Critter.status()
crit2 = Critter("R")
Critter.status()
crit1.talk()
crit2.talk()
print crit1
print crit2
