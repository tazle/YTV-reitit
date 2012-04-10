import sys
import cPickle

services = cPickle.load(sys.stdin)
print len(services)
for service in services:
    if service.line_id.startswith('63'):
        print unicode(service).encode('utf-8')
