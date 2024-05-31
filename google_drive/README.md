## Instructions

### 1. Configure Environment

1. Setup your Ollama Server

2. Install the following dependencies:
   ```
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

### 2. Setup Google Drive API Credentials

1. Go to your [Google Cloud Console](https://console.cloud.google.com/?ref=haihai.ai) and create a new project if needed.

2. Enable the [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com&ref=haihai.ai).

3. Setup Google API Credentials

   > To do this, Go to your Google Cloud Project and follow these steps:
   >
   > 1. Navigate to **APIs & Services**.
   > 2. Select **Credentials** on the side panel.
   > 3. Click on **CREATE CREDENTIALS**, then select **OAuth client ID**. If you wish to run it on your local machine, choose **Desktop app** as your **Application type**. Then, click on **CREATE**.
   > 4. After creating the credential, you will see a pop-up window (if not, you can click on the download button under **Actions** column). Download the credential as JSON.

4. Now you should have your credential downloaded to your machine as a `JSON` file. The filename should be something like `client_secret_*.json`. You will need it in `~/,credentials` directory. If you've never used Google Auth before, you may need to setup the directory by yourself.

5. To setup the directory, run `mkdir ~/.credentials` in terminal.

6. Move and rename your downloaded credentials to this directory. `mv [your-credential-json] ~/.credentials/credentials.json`. Replace `[your-credential-json]` by the path to your downloaded credential `JSON` file.

7. Setup environment variable for Google by running `export GOOGLE_APPLICATION_CREDENTIALS=~/.credentials/credentials.json`.

### 3. Run the Python Script

1. Navigate to the folder `/google_drive`.

2. (Optional) Create Python virtual environment `python -m venv .venv`.

3. (Optional) Activate the virtual environment `source .venv/bin/activate`. You can deactivate it by running `deactivate`.

4. Install dependencies `pip install -r requirements.txt`.

5. (Optional) Add persisted Chroma DB. Simply move your `chroma` folder under `/google_drive`.

6. Run the scripts `python main.py`.

When script is running, your browser may ask you to login using your Google account on the first run. If you need to load files from Google Drive, make sure the folder is visible to your account. A message will ask you for folder ID. You can find the folder ID in the URL. For example, in the link https://drive.google.com/drive/folders/XXXXXXXX, the `XXXXXXXX` should be the folder ID to enter.
