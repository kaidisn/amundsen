# NeputuneCsvBulkPublisher
from amundsen_gremlin.neptune_bulk_loader.api import (
    NeptuneBulkLoaderApi, get_neptune_graph_traversal_source_factory
)
from amundsen_gremlin.neptune_bulk_loader.gremlin_model_converter import GetGraph

class NeputuneCsvBulkPublisher(Publisher):
        """
        1. Uploading the CSV files to Amazon's S3.
        2. Making a request to the Neptune's bulk loader endpoint 
        pointing at the s3 files. (details can be found https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html) 
        
        Thanks to the team at Square most of the process of publishing 
        Amundsen data to Neptune is already implemented in the Neptune bulk loader API 
        found in the repo https://github.com/amundsen-io/amundsengremlin.
    """

    def __init__(self) -> None:
        super(NeputuneCsvBulkPublisher, self).__init__()

    def init(self, conf: ConfigTree) -> None:
        self.neptune_bulk_loader_api = NeptuneBulkLoaderApi.create_from_config(bulk_loader_config)
        self.neptune_graph_traversal_source_factory = get_neptune_graph_traversal_source_factory(session=password,
                                                                                                 neptune_url=host)
        return

    def publish_impl(self) -> None:
        return

    def _load_some_tables(self, data: Iterable[Table]) -> None:
        _data = list(data)
        entities = GetGraph.table_entities(table_data=_data, g=self.neptune_graph_traversal_source_factory())
        self.neptune_bulk_loader_api.bulk_load_entities(entities=entities)