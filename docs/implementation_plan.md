# Railway Deployment Plan

To deploy this MCP server to Railway, we need to adapt the code for a cloud environment. Railway is a PaaS (Platform as a Service) that builds applications from GitHub repositories and runs them in ephemeral containers.

## User Review Required

> [!WARNING]
> **Removing Interactive Approval**
> Currently, the server pauses and asks `Approve? (y/n)` in the terminal. Railway runs applications non-interactively in the background. If we leave this prompt, the server will hang forever waiting for input. **I will remove the interactive terminal approval** from `server.py` so the endpoints process requests immediately.

> [!IMPORTANT]
> **Secret Management via Environment Variables**
> Committing `client_secret.json` and `token.json` to GitHub is a severe security risk. Instead, I will update `auth.py` to read these JSON configurations from **Environment Variables** (`GOOGLE_CLIENT_SECRET_JSON` and `GOOGLE_TOKEN_JSON`). You will copy the contents of your local JSON files and paste them into Railway's Variables dashboard.

## Proposed Changes

### 1. Update `auth.py`
Modify `auth.py` to prioritize loading credentials from environment variables using `Credentials.from_authorized_user_info()` and `InstalledAppFlow.from_client_config()`. If environment variables are missing, it will safely fall back to the local files (`token.json` and `client_secret.json`) for local testing.

### 2. Update `server.py`
Remove the asynchronous terminal prompt logic (`ask_approval`) so the FastAPI server handles requests immediately without hanging.

### 3. Add `Procfile`
Create a `Procfile` in the root directory to tell Railway exactly how to start the FastAPI server on the cloud port:
```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### 4. Create `deployment-plan.md`
Generate the requested step-by-step markdown file containing the exact instructions on how to connect your GitHub repo to Railway, configure the Nixpacks builder, and add your secret variables.

## Verification Plan
1. Check that the server successfully reads secrets locally if environment variables aren't set.
2. Confirm the interactive prompt has been removed.
3. The `deployment-plan.md` artifact will be provided for you to execute the deployment on Railway.
