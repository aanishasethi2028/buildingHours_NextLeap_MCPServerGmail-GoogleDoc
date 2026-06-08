# Google Docs and Gmail MCP-style Server

A FastAPI application that provides tool endpoints to append text to Google Docs and create draft emails in Gmail.

## Setup

1. **Obtain Google Cloud Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the **Google Docs API** and **Gmail API**.
   - Navigate to **APIs & Services > Credentials**.
   - Create an **OAuth client ID** (Application type: Desktop app).
   - Download the JSON file and rename it to `credentials.json`.
   - Place `credentials.json` in this directory (`google-mcp-server/`).

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**:
   ```bash
   uvicorn server:app --reload
   ```

4. **First Run Authentication**:
   - The first time an endpoint is called, the server will open your browser to authenticate with Google.
   - After authentication, it will create a `token.json` file which will be used for subsequent requests.

## Endpoints

### POST `/append_to_doc`
Appends text to the end of a specified Google Document.

**Payload**:
```json
{
  "doc_id": "YOUR_DOCUMENT_ID",
  "content": "Text to append"
}
```

### POST `/create_email_draft`
Creates a new draft email in your Gmail account.

**Payload**:
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content"
}
```

## Interactive Approval
Before executing any action against Google APIs, the server will print the action details to the terminal and await your approval (`y/n`).
