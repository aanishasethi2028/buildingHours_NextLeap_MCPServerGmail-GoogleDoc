# Deploying your MCP Server to Railway

Railway is a cloud platform that automatically builds your code using Nixpacks. Because your code is written in Python, Railway will see your `requirements.txt` and know how to install your packages. 

I've added a `Procfile` and modified the server code to run non-interactively and read secrets from Environment Variables so that you don't commit your Google credentials to GitHub!

## Deployment Steps

1. **Push your code to GitHub**
   Commit everything inside `google-mcp-server` to a GitHub repository. **Make sure `client_secret.json`, `token.json`, and `.venv/` are in your `.gitignore` and are NOT pushed to GitHub.**

2. **Create a Railway Project**
   - Go to [railway.app](https://railway.app/) and log in with GitHub.
   - Click **New Project** → **Deploy from GitHub repo**.
   - Select the repository you just pushed.
   - Railway will automatically detect the `Procfile` and begin building your project using Python.

3. **Add Environment Variables**
   Once your project is created on Railway, the first build will likely fail because it needs your Google secrets. Go to your Railway project dashboard:
   - Click on your deployed service.
   - Navigate to the **Variables** tab.
   - Click **Raw Editor** and add the following two environment variables exactly as they appear in your local files:
     
     ```
     GOOGLE_CLIENT_SECRET_JSON={"web":{"client_id":"..." ... paste entire client_secret.json content here}
     GOOGLE_TOKEN_JSON={"token":"ya29..." ... paste entire token.json content here}
     ```
   *(Note: You can open your local `client_secret.json` and `token.json` files and literally copy all the text, pasting it directly as the values for these variables).*

4. **Generate a Domain**
   - Go to the **Settings** tab for your service in Railway.
   - Under **Networking**, click **Generate Domain** (or set up a custom domain). 
   - This URL will be your server's public endpoint.

5. **Restart & Test**
   - Adding the variables will trigger a new deployment. Wait for it to turn green.
   - Your public server is now live!
   - You can test it by going to `https://<YOUR-RAILWAY-DOMAIN>.up.railway.app/docs` to see your FastAPI documentation and send a test payload!

> [!TIP]
> **Token Expiry**: The `GOOGLE_TOKEN_JSON` contains a refresh token. Even if the actual access token expires, Google will use the refresh token to silently request a new access token in the background, so your deployment will keep working seamlessly.
