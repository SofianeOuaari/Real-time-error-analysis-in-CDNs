import os
import traceback
from dateutil import parser, tz

from influx_db_helper import InfluxDBLoader
from cdnlib.cdntools import cdntools as cdnt

CDN_TIME_ZONE = "Europe/Budapest"
CDN_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S:.%f%z"


class CDNMessageLoader:
    def __init__(
        self,
        schema: str,
        group_id: str,
        kafka_input_topic: str,
        influx_db_config: dict
    ) -> None:
        self.schema_helper = cdnt.schema.create_helper(schema)
        self.group_id = group_id
        self.kafka_input_topic = kafka_input_topic
        self.influx_db_config = influx_db_config
        self.influx_db_config.update(cdnt.conf.get("influx_db"))
        self.idbl = InfluxDBLoader(**influx_db_config)
        self.idbl.connect_to_influxdb(self.idbl.input_conf["database"])
        self.messages = []

    def run(self) -> None:
        self.idbl.check_database_existence(
            self.influx_db_config['output_conf']['database']
        )
        cdnt.kafka.consume_forever(
            group_id=self.group_id,
            topics=[self.kafka_input_topic],
            callback_functions=[self.consume_messages]
        )

    def consume_messages(self, message: dict) -> None:
        """Consumes messages from the configured Kafka topic and writes them
        to the configured InfluxDB measurement after a certain batch of
        messages are received.

        :param message: Message from Kafka describes by key-value pairs
        :return:
        """
        try:
            cdnt.log.info(f"Received message: {message}")
            self.schema_helper.validate(message)
            time = self.idbl.output_conf['schema']["time"]
            message[time] = parser.isoparse(
                message[time]).replace(tzinfo=tz.gettz(CDN_TIME_ZONE))
            self.messages.append(message)

            if len(self.messages) > 5:
                self.write_data_to_influx_db()
                self.messages = []
        except:
            cdnt.log.error(
                f"Unexpected event occurred! {traceback.format_exc()}"
            )

    def write_data_to_influx_db(self) -> None:
        """Writes the stored messages to the configured InfluxDB measurement.

        :return:
        """
        try:
            out_meas = self.idbl.output_conf["measurement"]
            data = [
                self.idbl.map_json_to_schema(
                    d, out_meas
                ) for d in self.messages
            ]
            self.idbl.write_to_influxdb(
                data, self.idbl.output_conf["database"]
            )
        except:
            cdnt.log.error(
                f"Unexpected event occurred! Error: {traceback.format_exc()}"
            )


if __name__ == '__main__':

    app_conf = cdnt.conf.parse_yaml(
        os.path.join(os.getcwd(), 'configs', 'app_config.yml')
    )['CDNInfluxDBLoader']

    ml = CDNMessageLoader(**app_conf)
    ml.run()
