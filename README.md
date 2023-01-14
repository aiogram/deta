# aiogram on Deta.sh

## Deployment Example

To get started, message @BotFather on Telegram to register your bot and receive its authentication
token (`TELEGRAM_TOKEN`).

To secure your webhook endpoint, you will need a secret word (`TELEGRAM_SECRET`)

Then click on this button:

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/aiogram/deta)

After that you can set webhook into new URL received from Deta, for example by using CURL:

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook
   -H "Content-Type: application/json"
   -d '{"url": "https://<example-bot>.deta.sh/webhook", "secret_token": "<TELEGRAM_SECRET>"}'
```

Congratulations! now you have deployed Telegram Bot on Deta.sh.
