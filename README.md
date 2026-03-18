# Discord Bot with CI/CD Pipeline Implementation
**Created by Javier Coll-Roman**

A python based Discord bot hosted on a Raspberry Pi that utilizes GitHub's webhooks to update the bot in real time whenever the repository is updated with new code, files, or anything else!

## Features

- **Hosted on Raspberry Pi**:
  &nbsp;&nbsp;• In order to keep bot running at all times, the python files required are run on a Raspberry Pi as a background process. This ensures that the bot runs at all time as long as power is being supplied to the Raspberry Pi and there is an internet connection.
- **CI/CD Pipeline** (`webhook_server.py'):
  &nbsp;&nbsp;• Utilizes HTTPServer and ReqeustHandler to receive posts from GitHub's webhook
  &nbsp;&nbsp;• Checks if webhook contains the correct secret key, if it does it pulls the GitHub repository to the Raspberry Pi and then restarts the bot
- **Medal.tv Latest Clips Uploads** (`main.py`):  
  &nbsp;&nbsp;• Bot calls on Medal.tv's API every 10 seconds in order to check if the registered user ID's have posted any new clips. If they have, the bot posts the links to the clips in registered clip channels that the user must register themselves.

# W.I.P.
