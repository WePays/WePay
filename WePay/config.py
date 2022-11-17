from decouple import config

OMISE_PUBLIC = config("OMISE_PUBLIC", cast=str, default="missing-omise-public")
OMISE_SECRET = config("OMISE_SECRET", cast=str, default="missing-omise-secret")
