# Utility to find who has access to google drive

This python script provides a simple tool to list all the files in a google drive that are owned by a particular user.

## Setup 

1. Follow the instructions here https://developers.google.com/drive/api/v3/quickstart/python
2. Once you have obtained `credentials.json`, run `pip3 install -r requirements.txt` in the project folder
3. Finally, run `python __main__.py -C /path/to/credentials.json example@example.com`

That command will prompt you to signin in your web browser, and then print out the search results for example@example.com. If you need to run it again, it will remember your credentials & you can just run `python __main__.py example@example.com`

