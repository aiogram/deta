# aiogram on Deta.space

## Deployment Example

To get started, message @BotFather on Telegram to register your bot and receive its authentication
token (`BOT_TOKEN`). To secure your webhook endpoint, you will need a secret word (`WEBHOOK_SECRET`)

Brief instructions:
- Create a new project using the [Space CLI](https://deta.space/docs/en/build/reference/cli) with the command ```space new```
- Then find out the ID of the created application on the site and use ```space link``` - this will connect your
 local repository with the remote application
- Once you have tested it locally with the ```space dev``` command
you can start the process of installing the bot on the cloud using ```space push```

[![Deploy](https://button.deta.dev/1/svg)](https://deta.space/)

Congratulations! Now you have deployed Telegram Bot on Deta.space

If you need to stop the webhook, run the following command:

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/deleteWebhook \
   -H "Content-Type: application/json"
```