from settings import ApiSettings
settings = ApiSettings()

TOKEN = settings.tg_api_token.get_secret_value()