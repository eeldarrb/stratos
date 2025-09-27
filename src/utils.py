from pathlib import Path


# TODO: gets extension atm, change to mimetype
def get_mimetype(file_path):
    path = Path(file_path)
    return path.suffix.lower()


def get_filename(file_path):
    path = Path(file_path)
    return path.name
