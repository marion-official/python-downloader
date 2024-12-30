import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )


USER_AGENTS_LIST_LOCATION = './db/user-agent.txt'

HTTP_RESPONSE_ACCEPTED = [200, 201, 204]
