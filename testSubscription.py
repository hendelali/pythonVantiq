__author__ = 'Hendel Ali'
__email__ = "hvalverde@vantiq.com"

import asyncio
from datetime import datetime
from gc import callbacks
from typing import Union
import pytest
from vantiqsdk import Vantiq, VantiqResources

_server_url: Union[str, None] = None
_access_token: Union[str, None] = None
_username: Union[str, None] = None
_password: Union[str, None] = None


def pytest_sessionstart():
    global _server_url
    global _access_token
    global _username
    global _password
    _server_url = "https://internal.vantiq.com/"
    _access_token = "7F6zxka1tqeXix6q_zoqtfefVYVPnToPt2mQ8lBZKBM="
    _username = "hvalverde@vantiq.com"
    _password = "**********" #not using credetials in this app only tokens

TEST_TOPIC = '/omniverse/test'
TEST_RELIABLE_TOPIC = '/omniverse/test'
TEST_TYPE = 'cities'

class TestTopicFromAPI:
    def _setup(self):
        """This method replaces/augments the usual __init__(self).  __init__(self) is not supported by pytest.
    Its primary purpose here is to 'declare' (via assignment) the instance variables.
    """
        self._acquired_doc = None
        self._doc_is_from = None
        self.callback_count = 0
        self.callbacks = []


    async def subscriber_callback(what: str, details: dict) -> None:
        print('Subscriber got a callback')
        if what == 'message':
            print(details['body']['value']['state'])
        #self.callback_count += 1
        #callbacks.append(what)
        #if message_checker:
        #    message_checker(what, details)
            
    
    async def check_subscription_ops(self, client: Vantiq, prestart_transport: bool):
        if prestart_transport:
            await client.start_subscriber_transport()

        # Now, we should see that our callback was called after a little while.
        self.last_message = None

        vr = await client.subscribe(VantiqResources.TOPICS, TEST_RELIABLE_TOPIC, None, self.subscriber_callback)
        #self.dump_result('Subscribe to reliable', vr)
        assert vr.is_success
        while self.last_message is None:
            await asyncio.sleep(0.1)

        last = self.last_message
     
    @staticmethod
    def check_test_conditions():
        if _server_url is None or _access_token is None or (_username is None and _password is None):
            pytest.skip('Need access to Vantiq server.')
            
    @pytest.mark.timeout(10)
    @pytest.mark.asyncio
    
    async def test_subscriptions(self):
        self._setup
        self.check_test_conditions()
        async with Vantiq(_server_url, '1') as client:
            await client.set_access_token(_access_token)
            await client.connect()
            await self.check_subscription_ops(self,client, True)        
        
        
test = TestTopicFromAPI
pytest_sessionstart()
asyncio.run(test.test_subscriptions(test))