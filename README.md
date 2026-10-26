# Mongodb-checker

🚀 Deployment Instructions
Method A: Deploying on Render
Push your code to a GitHub repository.

Go to your Render Dashboard.

Click New+ -> Blueprint and connect your GitHub repository.

Render will automatically read render.yaml.

Add your environment variable:

TELEGRAM_BOT_TOKEN: (Get this from @BotFather)

Click Apply. Once deployed, copy your Render Web Service URL (e.g., https://your-app.onrender.com).

Set your Telegram webhook by visiting this link in your browser:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app.onrender.com/webhook

Method B: Deploying on Vercel
Install the Vercel CLI or go to Vercel Dashboard.

Import your GitHub repository.

In the project settings, add the Environment Variable:

Name: TELEGRAM_BOT_TOKEN

Value: <Your Bot Telegram Token>

Click Deploy. Once deployed, Vercel will give you a production domain (e.g., [https://your-app.vercel.app](https://your-app.vercel.app)).

Set your Telegram webhook by visiting this link in your browser:
[https://api.telegram.org/bot](https://api.telegram.org/bot)<YOUR_BOT_TOKEN>/setWebhook?url=[https://your-app.vercel.app/webhook](https://your-app.vercel.app/webhook)
