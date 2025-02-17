# This program is designed to scrap web page information:

 1. The program scans web page headers and provides recommendations on how they can be changed to improve information accessibility
 2. After scanning the web page information, the program checks for grammatical errors and, if there are any, provides suggestions on how to correct them.
 3. Databases are created, all scanned information and suggestions are entered into the databases.
 4. After the program finishes its work, an email is sent to the specified e-mail address.

# How to use the program:

 1. You need to enable the Gmail API. To use the Gmail API, you will need to:
 2. Create a project "Google Cloud Console".
 3. Enable the Gmail API service in the project.
 4. Generate an authentication key in Google API
 5. Download key in JSON format from Google API
 5. Rename the downloaded file "credentials.json"
 6. To use the application, you need to create a creds folder and put the credentials.json file in it.
 7. Generate API key in "Google Cloud Console" and put it to file "api_key"
 8. Create .gitignore file and write file "api_key"
