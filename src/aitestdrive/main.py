import os

import uvicorn


def main(**kwargs):
    port = int(os.environ.get('PORT', 8000))  # Google Cloud sends us the $PORT it wants us to listen on
    uvicorn.run("aitestdrive.controller.app:api", host="0.0.0.0", port=port, **kwargs)


def main_dev():
    main(reload=True)


if __name__ == "__main__":
    main()
