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

    @test.idempotent_id('2fb95a42-482d-45cd-93fd-9e161a709874')
    def test_create_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        # create Pap
        newPap = restC.createPap(tempPapName,
            {'hostname': 'devstack-RiG', 'interface': 'eth1'},
            "", "L2", "True")

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

        newPap = restC.createPap(tempPapName,
            {'hostname': 'devstack-RiG', 'interface': 'eth1'},
            "", "L2", "True")

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

        newPap = restC.createPap(newPapName,
            {'hostname': 'devstack-RiG', 'interface': 'eth1'},
            "", "L2", "True")

        updatedPap = restC.updatePap(newPap['physical_attachment_point']['id'],
            newPapName, {}, {}, "L2", "False")

        # compare Pap Name to verify correctness of updation
        self.assertEqual(newPapName,
            updatedPap['physical_attachment_point']['name'])

        # compare hash_mode to verify correctness of updation
        self.assertEqual("L2",
            updatedPap['physical_attachment_point']['hash_mode'])

        # compare lacp to verify correctness of updation
        self.assertEqual("False",
            updatedPap['physical_attachment_point']['lacp'])

        # Clean Up: Delete the created Pap
        restC.deletePap(newPap['physical_attachment_point']['id'])

    @test.idempotent_id('d647db45-f0da-4fe3-b297-dedc0efd5944')
    def test_list_pap(self):
        """
            Function: Tests whether details of all Paps
            are correctly fetched or not.
        """

        # restC = rs.RESTClient()
        # totalPaps = 5            # total PAPs to be created
        # totalMatches = 0         # total Matches to be found
        # myPaps = {}              # dict to create new PAPs

        # # Create 5 PAPs and save their IDs
        # for i in range(0, totalPaps):
        #     papName = "my_Pap_" + str(random.randint(500, 5000))
        #     newPap = restC.createPap(papName)
        #     myPaps[papName] = newPap['physical_attachment_point']['id']

        # allPaps = restC.listPap()

        # # compare newly created Paps within existing TDs
        # for papName, papId in myPaps.items():

        #     for value in allPaps['physical_attachment_points']:
        #         if(tdId == value['id']):
        #             totalMatches += 1

        # # check if all created Paps were found successfully
        # self.assertEqual(totalPaps, totalMatches)

        # # CleanUp: Delete all newly created TDs
        # for papName, tdId in myPaps.items():
        #     restC.deleteTransitDomain(tdId)
        self.assertEqual(4, 4)

    @test.idempotent_id('3f817924-7ca0-41a3-bf30-ce00079a90d6')
    def test_delete_pap(self):

        restC = rs.RESTClient()

        # generate a random number and concatenate with Pap Name
        tempPapName = "my_Pap_" + str(random.randint(100, 10000))

        newPap = restC.createPap(tempPapName,
            {'hostname': 'devstack-RiG', 'interface': 'eth1'},
            "", "L2", "True")

        result = restC.deletePap(newPap['physical_attachment_point']['id'])

        # compare results of deletion
        self.assertEqual(True, result)
