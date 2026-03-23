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

    def process(self, data: Any) -> str:
        print("Initializing Numeric Processor...")

        if not data:
            print("There are no elements")
            return self.format_output(None)

        if isinstance(data, (list, set)):
            values = [int(v) for v in data]
        else:
            values = [int(data)]

        count = len(values)
        total = sum(values)
        avg = total / count

        return (count, total, avg)

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

    def format_output(self, result) -> str:
        if result is None:
            return "Output: No data to process"

        count, total, avg = result
        return f"Output: Processed {count} numeric values, sum={total},\
 avg={avg}\n"


class TextProcessor(DataProcessor):

    def process(self, data: Any) -> str:
        print("Initializing Text Processor...")

        length_text = len(data)
        count_words = 1
        i = 0

        if not data:
            count_words = 0
            length_text = 0

        for i in range(length_text):
            if data[i] == " ":
                count_words += 1

        return length_text, count_words

    def validate(self, data: Any) -> bool:
        try:
            if not data:
                return "Validation: Text data invalid"

            if isinstance(data, str) and not \
                    data.replace('.', '', 1).isdigit():
                return "Validation: Text data verified"
            else:
                return "Validation: Text data invalid"
        except ValueError:
            return "Wrong type"

    def format_output(self, result) -> str:
        if result is None:
            return "Output: No data to process"

        length_text, count_words = result
        return f"Output: Processed text: {length_text} characters,\
 {count_words} words\n"


class LogProcessor(DataProcessor):

    def process(self, data: Any) -> tuple:
        print("Initializing Log Processor...")
        print(f'Processing data: "{data}"')

        try:
            if data is None:
                raise ValueError("Empty log")
            if not isinstance(data, str):
                raise ValueError("Wrong type")

            liste = data.split(":")

            error_log = liste[0]
            message_log = liste[1]

            return error_log, message_log
        except IndexError:
            return "Validation: Missing ':' separator in log"
        except ValueError as e:
            return f"Validation: {e}"

    def validate(self, data: Any) -> bool:

        liste_errors = ["ERROR", "WARN", "INFO"]
        liste = data.split(':')
        validation = False
        if liste[0] in liste_errors:
            validation = True
        return validation

    def format_output(self, result) -> str:
        pass


if __name__ == "__main__":
    # num_pro = NumericProcessor()
    # values = [1, 2, 3, 4, 5]
    # result = num_pro.process(values)
    # print(f'Processing Data: {values}')
    # print(num_pro.validate(values))
    # print(num_pro.format_output(result))
    # text_pro = TextProcessor()
    # text = "Hello Nexus World"
    # result_text = text_pro.process(text)
    # print(f'Processing Data: {text}')
    # print(text_pro.validate(text))
    # print(text_pro.format_output(result_text))
    log_pro = LogProcessor()
    log = ""
    print(log_pro.process(log))
    result_log = log_pro.validate(log)
    print(log_pro.format_output(result_log))
