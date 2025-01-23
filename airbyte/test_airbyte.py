import airbyte as ab
import json
import logging
from copy import deepcopy

logger = logging.getLogger("airbyte")

"""config = {
        "dataset_name": "test",
        "format": "json",
        # "reader_options": json.dumps({}),
        # "url": f"../orchestration/airflow/data/resync_datadump_sample220218/000/0b/194813.json",
        "url": f"../orchestration/airflow/data/sample.json",
        # "url": f"../orchestration/airflow/data/resync_datadump_sample220218",
        "provider": {"storage": "local"},
    }
# setup source for airbyte
source = ab.get_source(
"source-file", 
config=config,
install_if_missing=True,)
print(source.check())
print(source.get_available_streams())
print(source.get_stream_json_schema(stream_name='test'))
print(source.read(streams='test'))
print(source.discovered_catalog)
"""

config = {"instance_type":{
                            "instance":"standalone",
                             "host": "http://localhost",
                            "port":27017,
                            "tls": False
                          }, 
          "database":"db",
          "auth_type":{"authorization":"login/password",
                       "username":"mongoadmin",
                       "password":"password"},
          "tunnel_method":{"tunnel_method":"NO_TUNNEL"},
          "destinationType":"mongodb",
          }
# setup destination
source = ab.get_source(
    "source-mongodb-v2",
    config=config,
    # docker_image=True,
    install_if_missing=True,
)
print(source.check())
destination = ab.get_destination(
    "destination-mongodb",
    config=config,
    docker_image=True,
    # install_if_missing=True,
)
print(destination.get_config())
destination.check()
# destination.write(source_data=source)
