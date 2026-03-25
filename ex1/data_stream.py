from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self,
                    data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class StreamProcessor(DataStream):
    pass


class SensorStream(DataStream):
    def __init__(self, stream_id):
        self.stream_id = stream_id

    def process_batch(self, data_batch):
        try:
            liste_valeurs = ["temp", "humidity", "pressure"]
            if not isinstance(data_batch, list[str]):
                raise ValueError("Incorrect type")
            liste_element = []
            temp_element = ""
            for element in data_batch:
                liste_element = element.split(":")
                if liste_element[0] in liste_valeurs:
                    
        except IndexError:
            return "Missing ':' separator in log"
        except (ValueError, KeyError) as e:
            print(f'Processing sensor batch: {e}')


if __name__ == "__main__":
    sensor_id = "SENSOR_001"
    sensor_batch = ["temp: 22.5", "humidity: 65", "pressure: 1013"]

    stream_id = "TRANS_001"
    stream_batch = ["buy:100", "sell:150", "buy:75"]

    trans_id = "EVENT_001"
    trans_batch = ["login", "error", "logout"]
