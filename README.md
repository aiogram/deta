# aiogram on Deta.space

## Deployment Example

To get started, message @BotFather on Telegram to register your bot and receive its authentication
token (`TELEGRAM_TOKEN`). To secure your webhook endpoint, you will need a secret word (`TELEGRAM_SECRET`)

Brief instructions:
- Create a new project using the [Space CLI](https://deta.space/docs/en/build/reference/cli) with the command ```space new```
- Then find out the ID of the created application on the site and use ```space link``` - this will connect your
 local repository with the remote application
- Once you have tested it locally with the ```space dev``` command
you can start the process of installing the bot on the cloud using ```space push```

[![Deploy](https://button.deta.dev/1/svg)](https://deta.space/)

After that you can set webhook into new URL received from Deta, for example by using CURL:

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook
   -H "Content-Type: application/json"
   -d '{"url": "https://<example-bot>.deta.sh/webhook", "secret_token": "<TELEGRAM_SECRET>"}'
```

Congratulations! Now you have deployed Telegram Bot on Deta.space

To stop the webhook, run the following command:

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/deleteWebhook
   -H "Content-Type: application/json"
```