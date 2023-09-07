from envparse import env

BOT_TOKEN = env.str('BOT_TOKEN')

USE_WEBHOOKS = env.bool('USE_WEBHOOKS', default=True)
if USE_WEBHOOKS:
	DETA_SPACE_APP_HOSTNAME = env.str('DETA_SPACE_APP_HOSTNAME')
	WEBHOOK_URL = f'https://{DETA_SPACE_APP_HOSTNAME}/webhook'
	WEBHOOK_SECRET = env.str('WEBHOOK_SECRET')

DETA_PROJECT_KEY = env.str('DETA_PROJECT_KEY', default=None)
