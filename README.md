# Website Availability Logger

This app monitors website status by pinging given URLs, categorising the response and logging to console, disk or a Kafka service. Software development concepts it demonstrates include use of static types (via mypy); object-oriented design with classes and interfaces; interfacing with a cloud-based service; and unit testing.

To set up:
- Clone this repo to a new directory
- Set up a new venv virtual environment
- Install dependencies from the manifest: pip install -r requirements.txt
- Default loggers are the console and disk logger, this can be changed on Main.py line 72
- To use the Kafka logger, add it in Main.py line 72 with the service URL, topic name and certificates directory

To use:
- Make a new json file with a list of websites and optional regexes. For demonstration see config-example.json
- To start monitoring your websites, run python Main.py your-config-file.json
- By default, logging will be to console and disk every 10 seconds.
- The monitoring frequency can be adjusted on Main.py line 71
- To check your Kafka log, run KafkaReader.py <service_url> <topic_name> <certs_dir>
- KafkaReader will poll your Kafka service until you press Ctrl+C / Command+C