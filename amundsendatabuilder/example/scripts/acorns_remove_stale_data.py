# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

"""
Delete stale data from Neo4j

"""

import os
import sys
import textwrap
import uuid
from elasticsearch import Elasticsearch
from pyhocon import ConfigFactory
from sqlalchemy.ext.declarative import declarative_base

from databuilder.job.job import DefaultJob
from databuilder.task.task import DefaultTask
from databuilder.task.neo4j_staleness_removal_task import Neo4jStalenessRemovalTask


neo_host = '54.198.220.53'
if len(sys.argv) > 2:
    neo_host = sys.argv[2]

DB_FILE = '/tmp/test.db'
SQLITE_CONN_STRING = 'sqlite:////tmp/test.db'
Base = declarative_base()

NEO4J_ENDPOINT = 'bolt://{}:7687'.format(neo_host if neo_host else 'localhost')
neo4j_endpoint = NEO4J_ENDPOINT
neo4j_user = 'neo4j'
neo4j_password = '@acornsloader'

neo_host = os.getenv('CREDENTIALS_NEO4J_PROXY_HOST', 'localhost')
neo_port = os.getenv('CREDENTIALS_NEO4J_PROXY_PORT', 7687)


task = Neo4jStalenessRemovalTask()
job_config_dict = {
    'job.identifier': 'remove_stale_data_job',
    'task.remove_stale_data.neo4j_endpoint': neo4j_endpoint,
    'task.remove_stale_data.neo4j_user': neo4j_user,
    'task.remove_stale_data.neo4j_password': neo4j_password,
    'task.remove_stale_data.target_relations': ['READ', 'READ_BY'],
    'task.remove_stale_data.milliseconds_to_expire': 86400000 * 3
}
job_config = ConfigFactory.from_dict(job_config_dict)
job = DefaultJob(conf=job_config, task=task)
job.launch()