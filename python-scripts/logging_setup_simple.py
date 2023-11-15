import logging
import sys


class ColorLogFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    colored_text = True
    if colored_text:
        FORMAT = "%(prefix)s%(msg)s%(suffix)s"
    else:
        FORMAT = "%(msg)s"

    LOG_LEVEL_COLOR = {
        "DEBUG": {'prefix': "\033[94m", 'suffix': "\033[0m"},
        "INFO": {'prefix': "\033[97m", 'suffix': "\033[0m"},
        "WARNING": {'prefix': "\033[93m", 'suffix': "\033[0m"},
        "ERROR": {'prefix': "\033[91m", 'suffix': "\033[0m"},
        "CRITICAL": {'prefix': "\033[1m"+"\033[91m", 'suffix': "\033[0m"},
    }

    def format(self, record):
        """Format log records with a default prefix and suffix to terminal color codes that corresponds to the log level name."""
        if not hasattr(record, 'prefix'):
            record.prefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('prefix')
        
        if not hasattr(record, 'suffix'):
            record.suffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('suffix')

        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)




logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(ColorLogFormatter())
logger.addHandler(stdout_handler)

