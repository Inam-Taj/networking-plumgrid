# Copyright 2016 PLUMgrid Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_serialization import jsonutils
import requests


class RESTClient(object):
    """
        This class makes REST calls to API Neutron in order to perform:
        - CRUD on Transit Domains (TD)
        - CRUD on Physical Attachment Points (PAP)
    """

    # Static Values
    port_keystone = "5000"
    port_neutron = "9696"
    base_url = "http://localhost:"
    transit_domain_url = "/v2.0/transit-domains"
    pap_url = "/v2.0/physical-attachment-points"

    # Global Access Token to be used to make REST calls to Neutron
    global accessToken

    # OpenStack Credentials to access KeyStone/Neutron APIs
    username = "admin"
    password = "pass"

    # Constructor
    def __init__(self):

        # Get Access Token in order to start making REST calls
        self.accessToken = self.getAccessToken()

    def getAccessToken(self):
        """
            Function that returns Access Token from Keystone that
            is required to make REST calls to Neutron
            ARGUMENTS: none
            RETURN TYPE: String
        """

        # Set up URL to access
        url = self.base_url + self.port_keystone + "/v2.0/tokens"

        # Set up Custom Headers for Request
        headers = {'accept': 'application/json', 'content-type':
                   'application/json'}

        # Set up parameters to send Authorization Details
        data = {"auth": {"passwordCredentials": {"username": self.username,
                         "password": self.password},
                         "tenantName": "admin"}}

        # Convert it into JSON
        dataInJson = jsonutils.dumps(data)

        # Send POST request and get RESPONSE
        response = requests.post(url, headers=headers, data=dataInJson)

        # Convert response in JSON
        jsonResp = response.json()

        # Extract Access Token from JSON Response
        self.accessToken = jsonResp['access']['token']['id']

        # Return Access Token
        return self.accessToken

    def createTransitDomain(self, tdName):
        """
            REST Function to create a Transit Domain
            and return the created Transit Domain
            ARGUMENTS:
                tdName = name of transit domain
            RETURN TYPE: JSON
        """

        # Set up URL to be accessed
        url = self.base_url + self.port_neutron + self.transit_domain_url

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Set up parameters to send Transit Domain Name
        data = {"transit_domain": {"name": tdName}}

        # Convert it into JSON
        dataInJson = jsonutils.dumps(data)

        # Send POST request to create Transit Domain and get RESPONSE
        response = requests.post(url, headers=headers, data=dataInJson)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def showTransitDomain(self, tdId):
        """
            Function to return a specific Transit Domain
            ARGUMENTS:
                tdId = ID of Transit Domain (tenant_id of TD)
            RETURN TYPE: JSON
        """

        # Set up URL for a specific Transit Domain to be accessed
        url = self.base_url + self.port_neutron \
            + self.transit_domain_url + "/" + tdId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send GET request and get RESPONSE
        response = requests.get(url, headers=headers)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def listTransitDomain(self):
        """
            REST Function to list all (existing) Transit Domain
            ARGUMENTS: NONE
            RETURN TYPE: JSON
        """

        # Set up URL to be accessed
        url = self.base_url + self.port_neutron + self.transit_domain_url

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send GET request to List all TDs and get response in JSON
        response = requests.get(url, headers=headers)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def updateTransitDomain(self, tdId, tdName):
        """
            Function to update Transit Domain with given new parameters
            ARGUMENTS:
                tdId = ID of Transit Domain (tenant_id of TD) to find TD by ID
                tdName = New name of Transit Domain which is to be updated
            RETURN TYPE: JSON
        """

        # Set up URL to specific access Transit Domain
        url = self.base_url + self.port_neutron \
            + self.transit_domain_url + "/" + tdId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Set up parameters to send Transit Domain Name
        data = {"transit_domain": {"name": tdName}}

        # Convert it into JSON
        dataInJson = jsonutils.dumps(data)

        # Send PUT request to update Transit Domain Details
        response = requests.put(url, headers=headers, data=dataInJson)

        # NOTE: response returns 200 in normal cases
        # so get body.text which is String; converts it to JSON
        jsonResp = jsonutils.loads(response.text)

        # return JSON Response
        return jsonResp

    def deleteTransitDomain(self, **kwargs):
        """
            Function to delete Transit Domain with given ID of Transit Domain
            ARGUMENTS which kwargs MAY have:
                tdId = ID of Transit Domain (not tenant_id) to find TD by ID
                tdName = Name of Transit Domain
            RETURN TYPE: boolean [True, False]
        """

        tdId = None

        # if tdName is given, then resolve its UUID
        if 'tdName' in kwargs:
            tdId = self.__getTransitDomainByName(kwargs['tdName'])

            # if UUID of Transit Domain is not found
            if(tdId is None):
                return False
        else:
            tdId = kwargs['tdId']

        # Set up URL to specific access Transit Domain
        url = self.base_url + self.port_neutron \
            + self.transit_domain_url + "/" + tdId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send PUT request to delete Transit Domain Details
        response = requests.delete(url, headers=headers)

        # if server deleted transit domain successfully then return true
        if(response.status_code == 204):
            return True
        else:
            return False

    def __getTransitDomainByName(self, tdName):
        """
            Function that resolves Transit Domain's Name to
            respective UUID. It returns None if UUID isn't resovled
        """
        allTDs = self.listTransitDomain()
        foundTD = None

        for value in allTDs['transit_domains']:
            if(value['name'] == tdName):
                foundTD = value['id']

        return foundTD

    def createPap(self, **kwargs):
        """
            REST Function to create return (created) PAP
            ARGUMENTS **kwargs will have:
                name = name of Physical Attachment Point
                interfaces = LIST of interfaces that includes
                hostnames and respective interface_names
                transit_domain_id = UUID of Transit Domain
                hash_mode = String: L2 / L3 / L2+L3 / L3+L4
                lacp = String: True / False
            RETURN TYPE: JSON
        """

        # Set up URL to be accessed
        url = self.base_url + self.port_neutron + self.pap_url

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        data = {"physical_attachment_point": kwargs}

        # Convert it into JSON
        dataInJson = jsonutils.dumps(data)

        # Send POST request to create PAP and get RESPONSE
        response = requests.post(url, headers=headers, data=dataInJson)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def showPap(self, papId):
        """
            Function to return a specific PAP
            ARGUMENTS:
                papId = ID of Physical Attachment Point
            RETURN TYPE: JSON
        """

        # Set up URL for a specific Transit Domain to be accessed
        url = self.base_url + self.port_neutron \
            + self.pap_url + "/" + papId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send GET request and get RESPONSE
        response = requests.get(url, headers=headers)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def listPap(self):
        """
            REST Function to list all (existing) PAPs
            ARGUMENTS: NONE
            RETURN TYPE: JSON
        """

        # Set up URL to be accessed
        url = self.base_url + self.port_neutron + self.pap_url

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send GET request to List all TDs and get response in JSON
        response = requests.get(url, headers=headers)

        # Convert response in JSON
        jsonResp = response.json()

        # Return JSON of response
        return jsonResp

    def updatePap(self, papId, **kwargs):
        """
            Function to update PAP with given new parameters
            ARGUMENTS
                id = UUID of Physical Attachment Point
                **kwargs will have:
                name = name of Physical Attachment Point
                add_interfaces = LIST of new interfaces to Add
                remove_interfaces = LIST of interfaces to Remove
                hash_mode = String: L2 / L3 / L2+L3 / L3+L4
                lacp = String: True / False

            RETURN TYPE: JSON
        """

        # Set up URL to specific access to PAP
        url = self.base_url + self.port_neutron \
            + self.pap_url + "/" + papId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Set up parameters to send PAP request according to variables
        data = {"physical_attachment_point": kwargs}

        # Convert it into JSON
        dataInJson = jsonutils.dumps(data)

        # Send PUT request to update Transit Domain Details
        response = requests.put(url, headers=headers, data=dataInJson)

        # NOTE: response returns 200 in normal cases
        # so get body.text which is String; converts it to JSON
        jsonResp = jsonutils.loads(response.text)

        # return JSON Response
        return jsonResp

    def deletePap(self, papId):
        """
            Function to delete PAP with given UUID
            ARGUMENTS:
                papId = ID of Physical Attachment Point to find it
            RETURN TYPE: boolean [True, False]
        """

        # Set up URL to specific access Transit Domain
        url = self.base_url + self.port_neutron \
            + self.pap_url + "/" + papId

        # Set up Custom Headers for Request
        headers = {'X-Auth-Token': self.accessToken,
                   'accept': 'application/json',
                   'content-type': 'application/json'}

        # Send PUT request to delete Transit Domain Details
        response = requests.delete(url, headers=headers)

        # if server deleted transit domain successfully then return true
        if(response.status_code == 204):
            return True
        else:
            return False
