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

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            liste_valeurs = ["temp", "humidity", "pressure"]
            if not isinstance(data_batch, List):
                raise ValueError('Incorrect type')
            liste_element = []
            for element in data_batch:
                liste_element = element.split(":")
                if liste_element[0] not in liste_valeurs:
                    raise ValueError(f'"{liste_element[0]}" is incorrect')
            return f'Processing sensor batch: {data_batch}'
        except IndexError:
            return "Missing ':' separator in log"
        except (ValueError, TypeError) as e:
            return f'Processing sensor batch: {e}'

    def filter_data(self,
                    data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        liste_valeurs = ["temp", "humidity", "pressure"]
        try:
            if not isinstance(data_batch, list):
                raise ValueError('Incorrect type')

            if criteria == "" or criteria is None:
                values = []
                for element in data_batch:
                    try:
                        partie_element = element.split(":")
                        if partie_element[0] not in liste_valeurs:
                            raise ValueError("Incorrect Values (enter 'temp',\
 'pressure' or 'humidity')")
                        if partie_element[0] == "temp":
                            values.append(float(partie_element[1]))
                    except (IndexError, ValueError):
                        raise ValueError("Incorrect Values (enter criteria:\
value)")

                if not values:
                    return ["No temp readings found", ""]

                count = len(values)
                readings = "readings" if count > 1 else "reading"
                avg = sum(values) / count
                return [f'{count} {readings} processed', f'avg temp: {avg}°C']

            if criteria not in liste_valeurs:
                raise ValueError(f'"{criteria}" is incorrect, enter "temp",\
 "humidity" or "pressure"')

            values = []
            for element in data_batch:
                try:
                    partie_element = element.split(":")
                    if partie_element[0] not in liste_valeurs:
                        raise ValueError("Incorrect Values")
                    if partie_element[0] == criteria:
                        values.append(float(partie_element[1]))
                except (IndexError, ValueError):
                    raise ValueError("Incorrect Values")

            if not values:
                return [f'No valid "{criteria}" readings found', ""]

            count = len(values)
            sign = "°C" if criteria == "temp" else ""
            readings = "readings" if count > 1 else "reading"
            avg = sum(values) / count
            return [f'{count} {readings} processed', f'avg {criteria}:\
 {avg}{sign}']

        except (ValueError, TypeError) as e:
            return [f'{e}', ""]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "type": "Environmental Data",
        }


class TransactionStream(DataStream):
    def __init__(self, stream_id):
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            liste_valeurs = ["buy", "sell"]
            if not isinstance(data_batch, List):
                raise ValueError('Incorrect type')
            liste_element = []
            for element in data_batch:
                liste_element = element.split(":")
                if liste_element[0] not in liste_valeurs:
                    raise ValueError(f'"{liste_element[0]}" is incorrect')
            return f'Processing transaction batch: {data_batch}'
        except IndexError:
            return "Missing ':' separator in log"
        except (ValueError, TypeError) as e:
            return f' {e}'

    def filter_data(self,
                    data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        liste_valeurs = ["buy", "sell"]
        count = 0
        count_buy = 0.0
        count_sell = 0.0
        try:
            if not isinstance(data_batch, list):
                raise ValueError('Incorrect type')

            if criteria == "" or criteria is None:
                criteria = "buy"

            if criteria not in liste_valeurs:
                raise ValueError(f'"{criteria}" is incorrect, enter "buy"\
 or "sell"')

            for element in data_batch:
                partie_element = element.split(":")
                if partie_element[0] not in liste_valeurs:
                    raise ValueError('Incorrect values, enter "buy" or "sell"')
                try:
                    valeur = int(partie_element[1])
                except ValueError:
                    valeur = float(partie_element[1])
                if partie_element[0] == "buy" and valeur > 0:
                    count += valeur
                    count_buy += valeur
                elif partie_element[0] == "sell" and valeur > 0:
                    count -= valeur
                    count_sell += valeur

            operations = "operations" if len(data_batch) > 1 else "operation"
            if criteria == "buy":
                result = f'buy {count_buy} units'
            elif criteria == "sell":
                result = f'sell {count_sell} units'
            if count > 0:
                count_units = f'+{count}'
            else:
                count_units = count
            return [f'{len(data_batch)} {operations} processed, net flow:\
 {count_units} units, {result}']

        except IndexError:
            return ["Missing ':' separator in log"]
        except (ValueError, TypeError) as e:
            return [f'{e}']

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "type": "Financial Data",
        }


class EventStream(DataStream):
    def __init__(self, stream_id):
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            liste_valeurs = ["login", "error", "logout"]
            if not isinstance(data_batch, List):
                raise ValueError('Incorrect type')
            for element in data_batch:
                if element not in liste_valeurs:
                    raise ValueError(f'"{element}" is incorrect')
            return f'Processing event batch: {data_batch}'
        except (ValueError, TypeError) as e:
            return f'Processing event batch: {e}'

    def filter_data(self,
                    data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        liste_valeurs = ["login", "error", "logout"]
        count_login = 0
        count_error = 0
        count_logout = 0

        try:
            if not isinstance(data_batch, list):
                raise ValueError('Incorrect type')

            if criteria == "" or criteria is None:
                return [f'{len(data_batch)} events']
            if criteria not in liste_valeurs:
                raise ValueError(f'"{criteria}" is incorrect, enter "error",\
 "login" or "logout"')
            for element in data_batch:
                if element == "login":
                    count_login += 1
                elif element == "logout":
                    count_logout += 1
                elif element == "error":
                    count_error += 1
            events = "events" if len(data_batch) > 1 else "event"

            if criteria == "login":
                count_units = count_login
            elif criteria == "logout":
                count_units = count_logout
            elif criteria == "error":
                count_units = count_error
            return [f'{len(data_batch)} {events},\
 {count_units} {criteria} detected']
        except (ValueError, TypeError) as e:
            return [f'{e}']

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "type": "Systems Events",
        }


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    sensor_stats = sensor.get_stats()
    print(f"Stream ID: {sensor_stats['stream_id']},\
 Type: {sensor_stats['type']}")
    sensor_batch = ["temp:22.5", "humidity:65", "pressure:103"]
    print(f"Processing sensor batch: {sensor_batch}")
    sensor_result = sensor.filter_data(sensor_batch)
    if len(sensor_result) >= 2:
        print(f"Sensor analysis: {sensor_result[0]} {sensor_result[1]}")
    else:
        print(f"Sensor analysis: {sensor_result[0]}")

    print("\nInitializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    transaction_stats = transaction.get_stats()
    print(f"Stream ID: {transaction_stats['stream_id']}, \
Type: {transaction_stats['type']} ")
    transaction_batch = ["buy:100", "sell:150", "buy:75"]
    print(f"Processing transaction batch: {transaction_batch}")
    transaction_result = transaction.filter_data(transaction_batch)
    print(f"Transaction analysis: {transaction_result[0]}")

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    event_stats = event.get_stats()
    print(f"Stream ID: {event_stats['stream_id']}, \
Type: {event_stats['type']} ")
    event_batch = ["login", "error", "logout", "error"]
    print(f"Processing event batch: {event_batch}")
    event_result = event.filter_data(event_batch, "error")
    print(f"Event analysis: {event_result[0]}")
