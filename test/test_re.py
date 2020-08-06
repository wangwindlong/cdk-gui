import re

string = "originOrgId: 'WDCN02431',"
print(re.findall(re.compile(r"originOrgId: ['](.*?)[']", re.S), string)[0])

