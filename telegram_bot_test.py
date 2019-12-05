from telegram.ext import Updater
import sensitive_info as si

print('test')
creds = si.SecurityCreds()
updater = Updater(token=creds.telegram_token, use_context=True)

