import binascii
import os
from random import randint
from time import sleep
import urllib.request as web
from urllib import parse
import re
from datetime import datetime

startTime = datetime.now()


def writeDict(dict, filename, sep):
    with open(filename, "a") as f:
        for i in dict.keys():
            f.write(i + "  <---> " + sep.join([str(x) for x in dict[i]]) + "\n")


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/36.0.1985.125 Safari/537.36',
    'Host': 'maps.napr.gov.ge',
    'Content-Type': 'text/plain',
    'Connection': 'keep - alive',
    'Content - Length': '484',
    'Origin': 'http://maps.napr.gov.ge',
    'Accept': '* / *',
    'Referer': 'http: // maps.napr.gov.ge /',
    'Accept - Encoding': 'gzip, deflate',
    'Accept - Language': 'en - US, en;q = 0.8, ru;q = 0.6, ka;q = 0.4',
}

with open("cadastr.txt", "r") as ins:
    cad_array = []
    for line in ins:
        cad_array.append(line.strip())

    ins.close()

dict_of_cadastr_with_polygon = {}

for per_cadastrial_code in cad_array:
    cadastr_code = per_cadastrial_code
    payload = {
        'callCount': '1',
        'windowName': 'c0-param0',
        'c0-scriptName': 'JDwrQueryData',
        'c0-methodName': 'findByParam',
        'c0-id': '0',
        'c0-e1': 'string:44.777149397534%2C41.809264644484%2C44.777307647866%2C41.809546035958',
        'c0-e2': 'string:%s' % cadastr_code,
        'c0-e3': 'null:null',
        'c0-e4': 'number:0',
        'c0-param0': 'Object_JSearchParams:{coordinatesString:reference:c0-e1, paramValue:reference:c0-e2, coordinates:reference:c0-e3, paramType:reference:c0-e4}',
        'batchId': '8',
        'instanceId': '0',
        'page': '%2F',
        'scriptSessionId': binascii.hexlify(os.urandom(16))
    }
    proxy_support = web.ProxyHandler({})
    opener = web.build_opener(proxy_support)
    web.install_opener(opener)
    req = web.Request('http://maps.napr.gov.ge/NgmapExt/dwr/call/plaincall/JDwrQueryData.findByParam.dwr',
                      data=parse.urlencode(payload).encode(), headers=headers, method='POST')
    sleep(randint(0, 3))
    resp = web.urlopen(req).read().decode('utf-8')

    try:

        dict_of_cadastr_with_polygon[per_cadastrial_code] = re.findall(r'\"POLYGON((.*?\)))"', resp)[0]
        print(per_cadastrial_code, "Found")

    except IndexError:

        dict_of_cadastr_with_polygon[per_cadastrial_code] = "Not Found Polygon"
        print(per_cadastrial_code, "Not")

writeDict(dict_of_cadastr_with_polygon, 'The_Result.txt', ":")

print("The time I used      = ", datetime.now() - startTime)
