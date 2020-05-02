import datetime

VERSION = "0.0.0"
PATCH = datetime.datetime.utcnow().strftime("%y%m%d%H%M")
RELEASE = f"{VERSION}-{PATCH}"
