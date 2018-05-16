from chess.app import create_app
from config import DEBUG, HTTP_HOST, HTTP_PORT

app = create_app()


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host=HTTP_HOST, port=HTTP_PORT)
