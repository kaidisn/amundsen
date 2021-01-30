# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

import boto3
import csv
import logging

from io import StringIO
from pyhocon import ConfigTree
from typing import Any

from databuilder.models.graph_serializable import GraphSerializable
from databuilder.loader.base_loader import Loader

# bucket = 'my_bucket_name' # already created on S3
# csv_buffer = StringIO()
# df.to_csv(csv_buffer)
# s3_resource = boto3.resource('s3')
# s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())


class S3SystemCSVLoader(Loader):
    """
    Loader class to write csv files to s3 in expected format for neptune
    """

    def init(self, conf: ConfigTree) -> None:
        """
        Initialize file handlers from conf
        :param conf:
        """
        self.conf = conf

        # local file writers
        self.node_file_handler = open('nodes.csv', 'w')
        self.edge_file_handler = open('edges.csv', 'w')
        self.node_fieldnames = ['~id','~label']
        self.edge_fieldnames = ['~id','~from','~to','~label']

        self.node_writer = csv.DictWriter(self.node_file_handler, fieldnames=self.node_fieldnames)
        self.edge_writer = csv.DictWriter(self.edge_file_handler, fieldnames=self.edge_fieldnames)

        # write to buffer for s3
        # self.node_writer = csv.writer(StringIO())
        # self.edge_writer = csv.writer(StringIO())
        # write header?


        self.node_writer.writeheader()
        self.edge_writer.writeheader()


    def load(self, csv_serializable: GraphSerializable) -> None:
        """,
        Write csv serializable into two files, one for vertix information, one for edge information
        :param record:
        :return:
        """
        node = csv_serializable.next_node()
        while node:
            print(node)
            node_dict = {
                '~id': node.key,
                '~label': node.label
            }
            self.node_writer.writerow(node_dict)
            # self.node_writer.writerow(node_dict)
            print(node_dict)
            node = csv_serializable.next_node()

        relation = csv_serializable.next_relation()
        i = 0
        while relation:
            print(relation)
            relation_dict = {
                '~id': relation.start_key + '_e'+str(i),
                '~from': relation.start_key,
                '~to': relation.end_key,
                '~label': relation.end_label
            }
            print(relation_dict)
            self.edge_writer.writerow(relation_dict)
            #self.edge_writer.writerow(relation_dict.values())
            relation = csv_serializable.next_relation()
            i += 1


    def close(self) -> None:
        """
        Close file handlers
        :return:
        """
        try:
            if self.node_file_handler:
                self.node_file_handler.close()
            if self.edge_file_handler:
                self.edge_file_handler.close()
        except Exception as e:
            logging.warning("Failed trying to close a file handler! %s",
                            str(e))

    def get_scope(self) -> str:
        return "loader.s3.csv"
