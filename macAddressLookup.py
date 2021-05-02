import json
import re
import sys

import requests


class FindMacAddress:
    def __init__(self):
        pass

    # Iterates over the json and prints the keyword/details asked for
    def iterate_json(self, data, details):
        for k, v in data.items():
            if isinstance(v, dict):
                if str(k).lower() == details:
                    print(k + " : " + str(v))
                else:
                    self.iterate_json(v, details)
                    continue
            else:
                if str(k).lower() == details:
                    print(k + " : " + str(v))
 
    # querying macaddress.io to fetch company name associated with the MAC address
    def mac_address_lookup(self, address):
        # api_key from website after logging in
        api_key = "at_QcfQIrxMNNzoBh9IwO2Pyc4fCQQVI"
        print(f'looking for , {address} ')
        headers = {'X-Authentication-Token': '{key}'.format(key=api_key)}
        url = "https://api.macaddress.io/v1?output=json&search=" + address
        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.content)
            print((data['vendorDetails'])['companyName'] + " is associated with the MAC address : " + address)
            details = input("If you need any other details, please provide the attribute or press exit ")
            if details == "exit":
                sys.exit()
            else:
                self.iterate_json(data, details)
        except requests.exceptions.RequestException as e:
            print("Not able to query for MAC address/parse the response" + e)

    @staticmethod
    def is_mac_address_valid(address):
        regex = ("^([0-9a-fA-F]{4}\\." +
                 "[0-9a-fA-F]{4}\\." +
                 "[0-9a-fA-F]{4})|" +
                 "^([0-9A-Fa-f]{2}[:-])" +
                 "{5}([0-9A-Fa-f]{2})$")

        pattern = re.compile(regex)

        if re.search(pattern, address):
            # return true if the address format is proper
            return True
        else:
            return False


if __name__ == '__main__':
    # to make sure only one command line argument is provided
    if len(sys.argv) == 2:
        mac_lookup = FindMacAddress()
        mac_address = sys.argv[1]
        # check whether the input mac address is in proper format or not
        is_mac_valid = mac_lookup.is_mac_address_valid(mac_address)
        # if valid mac address format, then call for address lookup
        if is_mac_valid:
            mac_lookup.mac_address_lookup(address=mac_address)
        else:
            print("Invalid MAC address format, Please verify your input")
    else:
        print("MAC Address cannot be NULL, Please provide the MAC address")
