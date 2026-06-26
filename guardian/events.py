from guardian.logger import logger


def emit(event, **kwargs):

    logger.info(f"{event} {kwargs}")
