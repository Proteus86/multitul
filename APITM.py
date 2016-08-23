__author__ = 'balakin'
# -*- coding: utf-8 -*-
import urllib.error
import urllib.request, hashlib, socket ,urllib.parse
import json
import re
import sys
import requests
import xml.etree.cElementTree as ElementTree
import certifi
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)
class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


'''
#---------------------------------------------------------------------------------------
def GET(ip,port,request,key=''):
    base_request = 'https://'+ip+':'+port+'/common_api/1.0/'+request
    try:

        req = urllib.request.Request(base_request)
        signature = hashlib.md5(key.encode('UTF-8')).hexdigest()
        req.add_header('Signature', signature)
        result = urllib.request.urlopen(req)
        decoded = json.loads(result.read().decode())
        print (decoded)
    except urllib.error.URLError:
        print ('urlopen error [WinError 10060] Попытка установить соединение была безуспешной,'
           ' \т.к. от другого компьютера за '
           '\требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного '
           '\отклика уже подключенного компьютера')
'''
#--------------------------------------------------------------------------
'''
Гет Апи работает проверил
'''
def GETparamAPI(ip, port, request, param='', key=''):
    base_request = 'https://' + ip + ':' + port + '/common_api/1.0/' + request + '?'

    result = ''
    if param != '':
        for item in param:
            result = result + item + '=' + urllib.parse.quote_plus(param[item]) + '&'
        resultparam = str(result[0:-1])
    else:
        resultparam= ''
    try:
        signature = hashlib.md5((resultparam+key).encode('UTF-8')).hexdigest()
        r=requests.get(base_request+resultparam,headers={'Signature':signature}, verify=False)
        decoded = json.loads(r.text)
        return  decoded

    except requests.exceptions.ConnectTimeout:
        ups= 'The request timed out while trying to connect to the remote server.'
        return ups
#-----------------------------------------------------------------------------------------
'''
ПОСТ Апи с разделением JSON или СЛОВАРЬ (по умолчанию словарь) работает проверил
'''
#--------------------------------------------------------------------------
def POSTparamAPI(ip,port,request,param='',key='',_json=False):
    base_request = 'https://'+ip+':'+port+'/common_api/1.0/'+request
    result=''
    req = urllib.request.Request(base_request,method='POST')
    if _json:
        signature = hashlib.md5((param+key).encode('UTF-8')).hexdigest()
        headers = {'Signature':signature, 'Content-Type':'application/json'}

    else:

        for item in param:
            result = result + item+'='+urllib.parse.quote_plus(param[item])+'&'
        param = str(result[0:-1])
        signature = hashlib.md5((param+key).encode('UTF-8')).hexdigest()
        headers = {'Signature':signature, 'Content-Type':'application/x-www-form-urlencoded'}


    try:
            result=requests.post(base_request,data=param, headers=headers, verify=False, timeout=20)
            #print(result)#   .encode('UTF-8'))
            decoded = json.loads(result.text)
            return decoded

    except requests.exceptions.ConnectTimeout:
        ups= 'The request timed out while trying to connect to the remote server.'
        return ups
#-----------------------------------------------------------------------------------------
'''
Гет ТАпи работает проверил
'''
def GETparamTAPI(ip,port,request,param='',fields='',key=''):
    base_request = 'https://'+ip+':'+port+'/tm_tapi/1.0/'+request+'?'
    result=''
    resultparam=''
    if param != '':
        for item in param:
            result = result + item+'='+urllib.parse.quote_plus(param[item])+'&'
        if fields =='':
            resultparam = str(result[0:-1])
        else:
            resultparam=result+'fields='+fields
    else:
        resultparam= ''
    try:
        signature = hashlib.md5((resultparam+key).encode('UTF-8')).hexdigest()
        base_request = base_request+resultparam+'&signature='+signature
        result=requests.get(base_request,headers={'Signature':signature}, verify=False)
        decoded = result.text
        tree = ElementTree.fromstring(result.content)
        return   XmlDictConfig(tree)

    except requests.exceptions.ConnectTimeout:
        ups= 'The request timed out while trying to connect to the remote server.'
        return ups
#-----------------------------------------------------------------------------------------
'''
ПОСТ ТАпи работает проверил
'''
def POSTparamTAPI(ip,port,request,param='',key=''):
    base_request = 'https://'+ip+':'+port+'/tm_tapi/1.0/'+request
    result=''
    resultparam=''
    if param != '':
        for item in param:
            result = result + item+'='+urllib.parse.quote_plus(param[item])+'&'
        resultparam = str(result[0:-1])
    else:
        resultparam= ''
    try:
        signature = hashlib.md5((resultparam+key).encode('UTF-8')).hexdigest()
        base_request = base_request
        headers = { 'Content-Type':'application/x-www-form-urlencoded'}
        resultparam=resultparam+'&signature='+signature
        #result=requests.post(base_request,data=resultparam,headers,verify=False)
        result=requests.post(base_request,data=resultparam,headers=headers,verify=False)

        decoded = result.text
        tree = ElementTree.fromstring(result.content)
        return   XmlDictConfig(tree)

    except requests.exceptions.ConnectTimeout:
        ups= 'The request timed out while trying to connect to the remote server.'
        return ups
#-----------------------------------------------------------------------------------------