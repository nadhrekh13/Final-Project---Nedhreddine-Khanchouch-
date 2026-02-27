import logging
import uuid
from config import settings

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Example function that does some work and logs errors

def example_function():
    try:
        logging.info('Starting example function')
        # Simulating some computation
        data_id = uuid.uuid4()  # Create a unique identifier
        logging.info(f'Generated UUID: {data_id}')
        # Using settings from the config
        logging.info(f'Loading data from {settings.data_file}')
        # More processing here...
        logging.info(f'{settings.APP_NAME} version {settings.APP_VERSION} is running')
    except Exception as e:
        logging.error(f'Error occurred: {e}')

if __name__ == '__main__':
    configure_logging()
    example_function()