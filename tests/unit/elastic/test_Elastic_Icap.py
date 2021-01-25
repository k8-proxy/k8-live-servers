from pprint import pprint
from unittest import TestCase

from k8_live_servers.elastic.Elastic_Icap import Elastic_Icap


class test_Elastic_Icap(TestCase):

    def setUp(self) -> None:
        self.elastic_icap = Elastic_Icap()
        print()

    def test_add(self):
        test_id   = 'test_add'
        test_data = {'an_id': test_id , 'some':'data'}
        result_add = self.elastic_icap.add(test_data, 'an_id')
        assert result_add['forced_refresh'] is True
        assert result_add['result'        ] == 'created'

        assert self.elastic_icap.data(index_by="an_id").get('test_add') == test_data

        result_delete = self.elastic_icap.index().delete(test_id, refresh=True)
        assert result_delete['forced_refresh'] is True
        assert result_delete['result'       ] == 'deleted'

        assert self.elastic_icap.data(index_by="an_id").get('test_add') is None


    def test_es(self):
        es = self.elastic_icap.es()
        assert es.info().get('tagline') == 'You Know, for Search'

    def test_index(self):
        index = self.elastic_icap.index()
        assert index.info().get('settings').get('index').get('provided_name') == 'gw-icap-servers'