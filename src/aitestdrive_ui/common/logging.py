import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # Set the log level (e.g., INFO, DEBUG, ERROR)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]  # Use a stream handler to print to stdout
    )

    set_log_level('asyncio', logging.WARN)
    set_log_level('numexpr.utils', logging.WARN)

    set_log_level('aitestdrive_ui.app', logging.DEBUG)


def set_log_level(base, level):
    logging.getLogger(base).setLevel(level)
