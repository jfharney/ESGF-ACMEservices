
import sys
import getopt

def main():
    # parse command line options
    print 'in main'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere
        
    
    class MyIterator(object):
        def __init__(self,step):
            self.step = step
        def next(self):
            if self.step == 0:
                raise StopIteration
            self.step -= 1
            return self.step
        def __iter__(self):
            return self
    
    for el in MyIterator(4):
        print el
    

if __name__ == "__main__":
    main()