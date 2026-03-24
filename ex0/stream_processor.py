from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result) -> str:
        return f'Output: {result}'


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            if not data:
                raise ValueError("Empty data")
            if isinstance(data, (list, set)):
                values = [int(v) for v in data]
            elif isinstance(data, (int, float, str)):
                values = [int(data)]
            else:
                raise ValueError("Wrong type")
            count = len(values)
            total = sum(values)
            avg = total / count
            return (count, total, avg)
        except (TypeError, ValueError) as e:
            return f"{e}"

    def validate(self, data: Any) -> bool:
        if not data:
            return False
        try:
            if isinstance(data, (list, set)):
                for value in data:
                    int(value)
            else:
                int(data)
            return True
        except (ValueError, TypeError):
            return False

    def format_output(self, result) -> str:
        if isinstance(result, str):
            return f"Output: {result}"
        count, total, avg = result
        return f"Output: Processed {count} numeric values,\
 sum={total}, avg={avg}\n"


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            if data == "":
                raise ValueError("Empty text")
            if isinstance(data, str):
                length_text = len(data)
                count_words = len(data.split())
                return length_text, count_words
            else:
                raise ValueError("Wrong type")
        except TypeError:
            return "Invalid data type"
        except ValueError as e:
            return f"{e}"

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        if data.replace('.', '', 1).isdigit():
            return False
        return True

    def format_output(self, result) -> str:
        if isinstance(result, str):
            return f"Output: {result}"
        length_text, count_words = result
        return f"Output: Processed text: {length_text} characters,\
 {count_words} words\n"


class LogProcessor(DataProcessor):

    def process(self, data: Any) -> str:
        try:
            if data == "":
                raise ValueError("Empty log")
            if isinstance(data, str):
                liste = data.split(":")
                error_log = liste[0]
                message_log = liste[1]
                return f'{error_log} level detected: {message_log}'
            else:
                raise ValueError("Wrong type")
        except IndexError:
            return "Missing ':' separator in log"
        except ValueError as e:
            return f"{e}"

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        else:
            liste_errors = ["ERROR", "WARN", "INFO"]
            liste = data.split(':')
            validation = True
            if liste[0] not in liste_errors:
                validation = False
        return validation

    def format_output(self, result) -> str:
        if isinstance(result, str):
            result_split = result.split(" ")
            error_message = ""
            if result_split[0] == "ERROR":
                error_message = "[ALERT]"
            elif result_split[0] == "WARN":
                error_message = "[WARN]"
            elif result_split[0] == "INFO":
                error_message = "[INFO]"
            return f'Output: {error_message} {' '.join(result_split)}\n'


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    num_pro = NumericProcessor()
    print("Initializing Numeric Processor...")
    values = [1, 2, 3, 4, 5]
    print(f'Processing Data: {values}')
    validation_nums = num_pro.validate(values)
    if validation_nums:
        print("Validation: Numeric data verified")
        result_nums = num_pro.process(values)
        print(num_pro.format_output(result_nums))
    else:
        print("Validation: Incorrect values\n")
    text_pro = TextProcessor()
    print("Initializing Text Processor...")
    text = "Hello Nexus World"
    print(f'Processing Data: {text}')
    validation_text = text_pro.validate(text)
    if validation_text:
        print("Validation: Text data verified")
        result_text = text_pro.process(text)
        print(text_pro.format_output(result_text))
    else:
        print("Validation: Incorrect text\n")
    log_pro = LogProcessor()
    print("Initializing Log Processor...")
    log = "ERROR: Connection timeout"
    print(f'Processing data: "{log}"')
    validation_log = log_pro.validate(log)
    if validation_log:
        print("Validation: Log entry verified")
        result_log = log_pro.process(log)
        print(log_pro.format_output(result_log))
    else:
        print("Validation: Incorrect log")

    print("=== POLYMORPHIC PROCESSING DEMO ===")
    print("Processing multiple data types through same interface...")

    processors = [
        (NumericProcessor(), [1, 2, 3]),
        (TextProcessor(), "Hello Nexus!"),
        (LogProcessor(), "INFO: System ready"),
    ]

    for i, (processor, data) in enumerate(processors, 1):
        if processor.validate(data):
            result = processor.process(data)
            output = processor.format_output(result)
            print(f"Result {i}: {output.replace('Output: ', '').strip()}")
    print("\nFoundation systems online. Nexus ready for advanced streams.")
