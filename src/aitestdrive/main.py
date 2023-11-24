import uvicorn


def main(**kwargs):
    uvicorn.run("aitestdrive.controller.app:api", host="0.0.0.0", port=8000, **kwargs)


def main_dev():
    main(reload=True)


if __name__ == "__main__":
    main()
