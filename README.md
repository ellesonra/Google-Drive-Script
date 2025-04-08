# Google Drive Export Scripts

This repository provides **two Python scripts** for downloading files from Google Drive:

- **`shared_drive_export.py`** – For exporting files from a **Google Workspace Shared Drive**
- **`personal_folder_export.py`** – For exporting files from a **personal Google Drive folder**

---

## 🚀 Overview

Google does not offer a direct method to export all contents of a Shared Drive or Personal Drive folder. These scripts fill that gap by using the Google Drive API to recursively download all files and folders to your local machine.

---

## 📁 Which Script Should You Use?

| Use Case | Script | Required OAuth Scope |
|----------|--------|----------------------|
| Shared Drive | `shared_drive_export.py` | `https://www.googleapis.com/auth/drive.readonly` (restricted) |
| Personal Folder | `personal_folder_export.py` | `https://www.googleapis.com/auth/drive.file` (not restricted) |

---

## ⚙️ Prerequisites

- Python 3.6 or higher
- A Google Cloud Project with OAuth 2.0 credentials
- Google Drive API enabled
- `client_secret.json` OAuth credentials in the same directory as the script

---

## 🛠️ Setup Instructions

### 1. Enable Google Drive API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **API & Services > Library**.
4. Search for **Google Drive API** and click **Enable**.

### 2. Create OAuth 2.0 Client ID

1. Go to **API & Services > Credentials**.
2. Click **Create Credentials** → **OAuth Client ID**.
3. Select **Desktop App** as the application type.
4. Add the appropriate scope based on the script you are using:
   - For Shared Drive: `https://www.googleapis.com/auth/drive.readonly`
   - For Personal Folder: `https://www.googleapis.com/auth/drive.file`
5. Download the `client_secret.json` and place it beside the script.

### 3. Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
▶️ Running the Scripts
For Shared Drive
bash
Copy
Edit
python shared_drive_export.py
You'll be prompted to enter the Shared Drive ID, which can be found in the URL:

bash
Copy
Edit
https://drive.google.com/drive/u/1/folders/{SHARED_DRIVE_ID}
⚠️ This script uses a restricted scope. You may need to go through Google verification for production use.

For Personal Folder
bash
Copy
Edit
python personal_folder_export.py
Enter the Folder ID from your personal Google Drive:

ruby
Copy
Edit
https://drive.google.com/drive/folders/{FOLDER_ID}
✅ This script uses a non-restricted scope and does not require special Google verification.

💻 Compatibility
Tested on:

Windows 11

It should also work on other platforms with minimal modification.

📄 Disclaimer
This software is provided under the MIT License. It is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

In no event shall the authors or copyright holders be liable for:

Any claim, damages, or other liability

In any action of contract, tort, or otherwise

Arising from, out of, or in connection with the software or the use or other dealings in the software

Important:
This software is not officially supported or endorsed by Google.
Use at your own risk.
