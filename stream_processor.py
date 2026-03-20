from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass


class NumericProcessor(DataProcessor):

    print("Initializing Numeric Processor...")

    def process(self, data: Any) -> str:
        if not data:
            print("There are no elements")

    def validate(self, data: Any) -> bool:
        liste_value: List[int] = []
        validation = True
        if not data:
            validation = False
        try:
            if not isinstance(data, (list, set)):
                try:
                    data = int(data)
                except ValueError:
                    raise ValueError
            elif isinstance(data, (list, set)):
                for value in data:
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValueError
                    liste_value.append(value)
            else:
                raise ValueError
        except ValueError:
            return "Validation: Invalid numeric data"

        if validation:
            return 'Validation: Numeric data verified'
        else:
            return 'Validation: Invalid numeric data'

    def format_output(self, result: str) -> str:
        pass


if __name__ == "__main__":
    num = NumericProcessor()
    values = []
    num.process(values)
    print(f'Processing Data: {values}')
    print(num.validate(values))

