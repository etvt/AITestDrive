import sys

import uvicorn

from aitestdrive.common.config import config


def main(**kwargs):
    uvicorn.run("aitestdrive.controller.app:api", host="0.0.0.0", port=config.listen_port, **kwargs)


def main_dev():
    main(reload=True)


if __name__ == "__main__":
    if "--dev" in sys.argv:
        main_dev()
    else:
        main()
