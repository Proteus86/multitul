__author__ = 'balakin'
# -*- coding: utf-8 -*-
import urllib.error
import urllib.request, hashlib,urllib.parse
import json
import requests
import xml.etree.cElementTree as ElementTree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)
class XmlDictConfig(dict):

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                else:
                    aDict = {element[0].tag: XmlListConfig(element)}
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
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
        result=requests.post(base_request,data=resultparam,headers=headers,verify=False)
        tree = ElementTree.fromstring(result.content)
        return   XmlDictConfig(tree)

    except requests.exceptions.ConnectTimeout:
        ups= 'The request timed out while trying to connect to the remote server.'
        return ups
#-----------------------------------------------------------------------------------------