import sys

import uvicorn


def main(**kwargs):
    from aitestdrive_ui.common.logging import configure_logging
    configure_logging()

    from aitestdrive_ui.common.config import config

    uvicorn.run("aitestdrive_ui.controller.app:app", host="0.0.0.0", port=config.listen_port, **kwargs)


def main_dev():
    main(reload=True)


if __name__ == "__main__":
    if "--dev" in sys.argv:
        main_dev()
    else:
        main()
