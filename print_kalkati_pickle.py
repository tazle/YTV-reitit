import sys
import cPickle

services = cPickle.load(sys.stdin)
print len(services)
for service in services:
    if service.line_id.startswith('501'):
        print unicode(service)
