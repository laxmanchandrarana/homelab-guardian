from guardian.database import init_db
from guardian.scheduler import start
from guardian.logger import logger
from guardian.settings import APP_NAME
from guardian.plugins import discover


def main():

    logger.info(f"{APP_NAME} starting")

    init_db()

    start()

    plugins = discover()

    logger.info(f"Plugins: {plugins}")

    print(f"{APP_NAME} started successfully.")


if __name__ == "__main__":
    main()
