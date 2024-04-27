import logging
from settings import settings
from milvus import Milvus, IndexType, MetricType
import numpy as np



def create_connection() -> Milvus:
    return Milvus(host= settings._HOST, port= settings._PORT)


def create_collections_if_not_exist(db: Milvus, name_collection: str):
    status, ok = db.has_collection(name_collection)
    if not ok:
        resources_params = {
            'collection_name': name_collection,
            'dimension': settings._DIM,
            'index_file_size': settings._INDEX_FILE_SIZE,
            'metric_type': MetricType.IP
        }
        db.create_collection(resources_params)

        # index_param = {
        #     'nlist': 2048
        # }
        # status = db.create_index(name_collection, IndexType.IVF_FLAT, index_param)
        # if not status.OK():
        #     logging.error("Creating Index failed: {}".format(status))
        # else:
        #     logging.info(f"Created collection {name_collection} and Index!")
    else:
        logging.info(f"Collection {name_collection} already exists!")


connection = create_connection()