import google.auth

DEFAULT_PORT = 8000


def get_google_cloud_project():
    _, project = google.auth.default()
    assert project is not None, ("No project ID could be determined. Consider running `gcloud config set project` or"
                                 " setting the GOOGLE_CLOUD_PROJECT environment variable")
    return project
