import sys
from storage import marshal
from kalkati import parse_services

services = parse_services(sys.stdin)
marshal(sys.stdout, services)

