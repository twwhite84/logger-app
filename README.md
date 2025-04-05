# Aiven Web Monitor Homework

This app consists of two runnable files, Main.py and LogReader.py

To set up:
- Clone this repo to a new directory
- Set up a new venv virtual environment
- Install dependencies from the manifest: pip install -r requirements.txt
- You need to modify Loggers.py lines 59-62 to be your correct Kafka service details
- These details also need to be updated in lines 3-6 of LogReader.py
- By default, Kafka certificates are expected to be in the directory "certs"

To use:
- Make a new json file with a list of websites and optional regexes. For demonstration see config-example.json
- To start monitoring your websites, run python Main.py your-config-file.json
- By default, logging will be to console and to Kafka every 10 seconds.
- A class DiskLogger() can be added on line 70 of Main.py
- The monitoring frequency can be adjust on line 69 of Main.py
- To consume what has been uploaded to Kafka, run LogReader.py in a new terminal tab
- LogReader will poll Kafka until you press Ctrl+C / Command+C

Regarding the email on AI use, I did use GPT to help debug a JSON schema. I copied a generated
schema into it and asked why it was missing required urls. It informed me about use of the "anyOf"
modifier, and using this seems to have fixed the bug. I have left a note in ConfigReader.py about this.