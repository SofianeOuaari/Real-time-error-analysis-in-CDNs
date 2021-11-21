import os
import json
import time
import datetime
import traceback
from dateutil import parser

import pandas as pd

from cdnlib.cdntools import cdntools as cdnt


class DataProvider:

    base_path = os.getcwd()

    def __init__(
        self,
        data_provider_id: int,
        path_data: str,
        kafka_topics: dict,
        seconds_to_wait: int
    ) -> None:
        self.dp_id = data_provider_id
        self.path_data = path_data
        self.kafka_topics = kafka_topics
        self.seconds_to_wait = seconds_to_wait
        self.kafka_helper = cdnt.kafka
        self.schema_helper = cdnt.schema.create_helper('ClientData')

    def record_publish_client_data(self) -> None:
        """Extracts client data from the pre-configured file and publishes
        it to the given topics.

        :return:
        """
        df = pd.read_csv(os.path.join(self.base_path, *self.path_data))
        df['timestamp'] = df['timestamp'].apply(lambda x: parser.parse(x))
        df.sort_values('timestamp', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['timestamp'] = df['timestamp'].apply(lambda x: str(x))
        df.fillna(value=-1, inplace=True)
        records = df.to_dict('records')

        # TODO publishing frequency simulation

        for i, rec in enumerate(records):
            try:
                cdnt.log.info(f'Received new client data! {rec}')

                self.schema_helper.validate(rec)
                self.kafka_helper.publish(
                    self.kafka_topics['cdn_ml_model_input'],
                    rec
                )
                self.kafka_helper.publish(
                    self.kafka_topics['cdn_client_data_storage'],
                    rec
                )
                time.sleep(self.seconds_to_wait)
            except:
                cdnt.log.error(
                    f'Unexpected event occurred!: {traceback.format_exc()}'
                )


if __name__ == '__main__':

    app_conf = cdnt.conf.parse_yaml(
        os.path.join(DataProvider.base_path, 'configs', 'app_config.yaml')
    )['data_provider']
    dp = DataProvider(**app_conf)
    dp.record_publish_client_data()
