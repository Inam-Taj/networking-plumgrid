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

from plumgrid_tempest_plugin import config
from plumgrid_tempest_plugin.services import rest_client as rs
import random
from tempest.api.network import base
from tempest import test

CONF = config.CONF


class TestPhysicalAttachmentPoint(base.BaseNetworkTest):
    """
        This class contains Test Cases for Physical
        Attachment Point that are specified in the
        Document: "Physical Attachment Point Tempest Test Plan"
    """
    hostname = "devstack-RiG"
    interface = "eth1"

    @test.idempotent_id('2fb95a42-482d-45cd-93fd-9e161a709874')
    def test_create_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        interfaces = [{'hostname': self.hostname,
                       'interface': self.interface}]

        # create Pap
        newPap = restC.createPap(name=tempPapName, interfaces=interfaces,
                                 hash_mode="L2", lacp="True")

        # Verifying Pap Creation with it's name
        self.assertEqual(tempPapName,
                         newPap['physical_attachment_point']['name'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('5d4b2eb6-5ce6-44c3-afb3-b0fb75a15c7c')
    def test_show_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        interfaces = [{'hostname': self.hostname,
                       'interface': self.interface}]

        # create Pap
        newPap = restC.createPap(name=tempPapName, interfaces=interfaces,
                                 hash_mode="L2", lacp="True")

        # show PAP
        tempPap = restC.showPap(newPap['physical_attachment_point']['id'])

        # compare PAP Ids to verify correctness
        self.assertEqual(newPap['physical_attachment_point']['id'],
                         tempPap['physical_attachment_point']['id'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('3ba5892a-5fb1-49fc-b113-1e3b47712a37')
    def test_update_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        newPapName = "updated_Pap_Name_" + str(random.randint(100, 10000))

        interfaces = [{'hostname': self.hostname,
                       'interface': self.interface}]

        newPap = restC.createPap(name=newPapName,
                                 interfaces=interfaces,
                                 hash_mode="L2", lacp="True")

        updatedPap = restC.updatePap(newPap['physical_attachment_point']['id'],
                                     name=newPapName, hash_mode="L2",
                                     lacp="False")

        # compare Pap Name to verify correctness of updation
        self.assertEqual(newPapName,
                         updatedPap['physical_attachment_point']['name'])

        # compare hash_mode to verify correctness of updation
        self.assertEqual("L2",
                         updatedPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness of updation
        self.assertEqual(False,
                         updatedPap['physical_attachment_point']['lacp'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('3f817924-7ca0-41a3-bf30-ce00079a90d6')
    def test_delete_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        interfaces = [{'hostname': self.hostname,
                       'interface': self.interface}]

        # create Pap
        newPap = restC.createPap(name=tempPapName, interfaces=interfaces,
                                 hash_mode="L2", lacp="True")

        result = restC.deletePap(newPap['physical_attachment_point']['id'])

        # compare results of deletion
        self.assertEqual(True, result)

    @test.idempotent_id('0634b1f7-8332-4f10-8079-42b274c7e156')
    def test_create_pap_no_parameters(self):
        """
            Functionality:
            - create physical attachment point without
            providing any input values
        """

        restC = rs.RESTClient()
        noIntfs = False

        # create Pap
        newPap = restC.createPap()

        # check if returned interfaces field is empty
        if not newPap['physical_attachment_point']['interfaces']:
            noIntfs = True

        # compare empty interfaces to verify correctness
        self.assertEqual(True, noIntfs)

        # compare hash_mode to verify correctness
        self.assertEqual("L2",
                         newPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness
        self.assertEqual(False,
                         newPap['physical_attachment_point']['lacp'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('fb1e3803-2872-439a-bb4a-e3de50d3ed91')
    def test_create_pap_name(self):
        """
            Functionality:
            - create physical attachment point but only
            provide the name parameter as input
        """
        restC = rs.RESTClient()
        noIntfs = False

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        # create Pap
        newPap = restC.createPap(name=tempPapName)

        # check if returned interfaces field is empty
        if not newPap['physical_attachment_point']['interfaces']:
            noIntfs = True

        # Verifying Pap Creation with it's name
        self.assertEqual(tempPapName,
                         newPap['physical_attachment_point']['name'])

        # compare empty interfaces to verify correctness
        self.assertEqual(True, noIntfs)

        # compare hash_mode to verify correctness
        self.assertEqual("L2",
                         newPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness
        self.assertEqual(False,
                         newPap['physical_attachment_point']['lacp'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('60bbb470-ac16-47ed-ae04-61a343d97146')
    def test_create_pap_lacp(self):
        """
            Functionality:
            - create physical attachment point but only
            provide the lacp parameter as input
        """
        restC = rs.RESTClient()
        noIntfs = False

        # create Pap
        newPap = restC.createPap(lacp=True)

        # check if returned interfaces field is empty
        if not newPap['physical_attachment_point']['interfaces']:
            noIntfs = True

        # compare lacp to verify correctness
        self.assertEqual(True,
                         newPap['physical_attachment_point']['lacp'])

        # compare empty interfaces to verify correctness
        self.assertEqual(True, noIntfs)

        # compare hash_mode to verify correctness
        self.assertEqual("L2",
                         newPap['physical_attachment_point']['hash_mode'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('697354b0-6636-4e5e-92e9-562a6d2e407e')
    def test_create_pap_hash_mode(self):
        """
            Functionality:
            - create physical attachment point but only
            provide the hash_mode parameter as input
        """
        restC = rs.RESTClient()
        noIntfs = False

        # create Pap
        newPap = restC.createPap(hash_mode="L2")

        # check if returned interfaces field is empty
        if not newPap['physical_attachment_point']['interfaces']:
            noIntfs = True

        # compare hash_mode to verify correctness
        self.assertEqual("L2",
                         newPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness
        self.assertEqual(False,
                         newPap['physical_attachment_point']['lacp'])

        # compare empty interfaces to verify correctness
        self.assertEqual(True, noIntfs)

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('58954f98-b9f0-4415-83b4-30be114378a2')
    def test_create_pap_interfaces_empty(self):
        """
            Functionality:
            - create physical attachment point but only provide
            empty list of interfaces parameter as input
        """
        restC = rs.RESTClient()
        noIntfs = False

        # create Pap
        newPap = restC.createPap()

        # check if returned interfaces field is empty
        if not newPap['physical_attachment_point']['interfaces']:
            noIntfs = True

        # compare empty interfaces to verify correctness
        self.assertEqual(True, noIntfs)

        # compare hash_mode to verify correctness
        self.assertEqual("L2",
                         newPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness
        self.assertEqual(False,
                         newPap['physical_attachment_point']['lacp'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('929c8540-597e-49c2-b645-1b5d3f7ea88a')
    def test_create_pap_interfaces_dict(self):
        """
            Functionality:
            - create physical attachment point but only provide
            dict of interfaces parameter as input
        """
        restC = rs.RESTClient()
        interfaces = {'hostname': self.hostname, 'interface': self.interface}

        # create Pap
        newPap = restC.createPap(interfaces=interfaces)

        # compare hash_mode to verify correctness
        self.assertEqual("InvalidInterfaceFormat",
                         newPap['NeutronError']['type'])

    @test.idempotent_id('673b0dc9-4ebe-4148-9a43-43f84f673903')
    def test_create_pap_interfaces_no_host(self):
        """
            Functionality:
            - create PAP with list of interfaces
            - one of the interfaces should be missing hostname

        """
        restC = rs.RESTClient()
        interfaces = [{'interface': self.interface}]

        # create Pap
        newPap = restC.createPap(interfaces=interfaces)

        # compare hash_mode to verify correctness
        self.assertEqual("InvalidInterfaceFormat",
                         newPap['NeutronError']['type'])

    @test.idempotent_id('f1fce688-4cb5-4327-b3b7-96c7abc066aa')
    def test_create_pap_interfaces_no_interface_name(self):
        """
            Functionality:
            - create PAP with list of interfaces
            - one of the interfaces should be missing interface

        """
        restC = rs.RESTClient()
        interfaces = [{'hostname': self.hostname}]

        # create Pap
        newPap = restC.createPap(interfaces=interfaces)

        # compare hash_mode to verify correctness
        self.assertEqual("InvalidInterfaceFormat",
                         newPap['NeutronError']['type'])
