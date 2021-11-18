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


def reindex_keyword_filter():
    print("Probíhá reindexace ICT smluv na pozadí, tato operace může trvat několik minut...")
    es = create_elastic_conn()
    result = es.reindex(body={
        "source": {
            "index": 'contracts',
            "query": {
                "query_string": {
                    "default_field": "*",
                    "query": "android OR (aplikac*) OR (cloud*) OR (databáz*) OR (disk*) OR (hardwar*) OR (hw) OR ICT "
                             "OR iOS OR IS OR LCD OR linux OR (notebook*) OR PC OR (počítač*) OR (procesor*) OR SEO "
                             "OR server OR (softwar*) OR SSD OR SW OR (switch*) OR (systém*) OR (telekomunika*) OR "
                             "upgrade OR (web*) OR wifi OR windows "
                }
            }
        },
        "dest": {
            "index": 'ict_contracts'
        }
    }, wait_for_completion=False, scroll="1m")
