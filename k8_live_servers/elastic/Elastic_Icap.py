from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_elastic.elastic.ES import ES
from osbot_elastic.elastic.Index import Index


class Elastic_Icap:

    def __init__(self):
        self.index_id = 'gw-icap-servers'

    def add(self, data, id_key=None):
        return self.index().add(data, id_key=id_key, refresh=True)

    @cache_on_self
    def es(self):
        return ES().setup()

    @cache_on_self
    def index(self):
        index = Index(es=self.es(), index_id=self.index_id)
        index.create()                                              # make sure it exists
        return index

    @index_by
    @group_by
    def data(self, **kwargs):
        return self.index().data(**kwargs)


