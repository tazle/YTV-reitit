import sys
from storage import marshal
from kalkati import parse_services
import json

if len(sys.argv) > 1:
    combination_groups = json.load(open(sys.argv[1], 'rb'))
else:
    combination_groups = []

services = parse_services(sys.stdin, combination_groups)
marshal(sys.stdout, services)

