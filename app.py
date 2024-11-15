import os, logging
from app import app

if __name__ == "__main__":
	app.run()
elif "GUNICORN_CMD_ARGS" in os.environ:
	logger = logging.getLogger("gnicorn.error")
	app.logger.handlers = logger.handlers
	app.logger.setLevel(logger.level)