import re

ERROR_PATTERN = re.compile(r"\| (ERROR|CRITICAL|WARNING) \|")
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}")


class LogParser:
    def __init__(self):
        self.current_block = []
        self.in_error_block = False

    def process_line(self, line: str):
        # Detect start of new log entry
        if TIMESTAMP_PATTERN.match(line):

            # If previous block was error → emit
            if self.in_error_block and self.current_block:
                event = "".join(self.current_block)
                self.current_block = []

                # Check if this new line starts new error
                if ERROR_PATTERN.search(line):
                    self.current_block.append(line)
                    self.in_error_block = True
                else:
                    self.in_error_block = False

                return event

            # New entry
            if ERROR_PATTERN.search(line):
                self.in_error_block = True
                self.current_block = [line]
            else:
                self.in_error_block = False

        else:
            if self.in_error_block:
                self.current_block.append(line)

        return None
