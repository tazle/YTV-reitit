import sys
from kalkati import parse_services
from collections import defaultdict
import cPickle
import marshal

services = parse_services(sys.stdin)
print len(services)
