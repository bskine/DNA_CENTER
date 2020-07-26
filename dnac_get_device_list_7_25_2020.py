from pprint import pprint
import requests
import json
from requests.auth import HTTPBasicAuth
from dna_creds import DNAC_IP, DNAC_PORT, USERNAME, PASSWORD

def get_auth_token():
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token' 
    # Make the POST Request
    resp = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD)) 
    # Retrieve the Token from the returned JSON
    token = resp.json()['Token']
    # Create a return statement to send the token back for later use
    return token


def get_device_list():
    token = get_auth_token()
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    header = {'x-auth-token': token, 'content-type' : 'application/json'}
    response = requests.get(url, headers=header)
    device_list = response.json()
    return device_list


def print_out():
    clean = []
    data = get_device_list()
    foo = data['response']
    print('\n')
    print('{:<25}{:^25}{:<25}{:<25}{:<25}'.format('hostname',
                                                  'mgmt IP',
                                                  'Platform',
                                                  'IOS',
                                                  'SN#'))
    print(('-'*125))
    for x in foo:
        for k,v in x.items():
            if v is None:
                x[k] = '**********'
            if v == 'None':
                x[k] = '*!*!*!*!*!'
        clean.append(x)
    for i in clean:
        print('{:<25}{:^25}{:<25}{:<25}{:<25}'.format(i['hostname'],
                                                      i['managementIpAddress'],
                                                      i['platformId'], 
                                                      i['softwareVersion'], 
                                                      i['serialNumber']))
        print(('-'*125))

if __name__ == "__main__":
    print_out()
    

