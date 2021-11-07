from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
from datetime import datetime
import time
import json


def create_elastic_conn():
    for x in range(20):
        # čekání na yellow status
        try:
            es = Elasticsearch(hosts=[{"host": "host.docker.internal", "port": 9200}])
            if es.cluster.health(wait_for_status='yellow'):
                return es
        except ElasticConnectionError:
            print("Waiting for elasticsearch connection")
            time.sleep(5)
        else:
            print("Elasticsearch failed to start")
            exit()


def insert_into_elastic(contract_id, contract_metadata, contract_text):
    es = create_elastic_conn()
    contract_metadata = json.loads(contract_metadata)
    doc = {
        'casZverejneni': contract_metadata["casZverejneni"],
        'odkaz': contract_metadata["odkaz"],
        'hodnotaVcetneDph': contract_metadata["hodnotaVcetneDph"],
        'predmet': contract_metadata["predmet"],
        'timestamp': datetime.now(),
        'text': contract_text,
    }
    res = es.index(index="contracts", id=contract_id, body=doc)


