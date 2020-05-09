import datetime

VERSION = "0.0.1"
PATCH = datetime.datetime.utcnow().strftime("%y%m%d%H%M")
RELEASE = f"{VERSION}"  # f"{VERSION}-{PATCH}"
