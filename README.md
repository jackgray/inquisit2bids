Inquisit / Millisecond.com does not have a REST API

Data must be downloaded manually. It is recommended to configure a private server to host the data in order to have control over data automations as soon as it is collected.

The scripts in this folder aim to rename, organize, and generate metrics on completion of the task, after the dataset has been downloaded and unzipped.

rename.py - converts raw inquisit data into bids structure and labels the files with a date, then converts those dates into session numbers. Attempts to extrapolate gaps in dates to accurately express gaps in sessions for missed days

audit.sh - generates a tsv of completion statistics based on bids formatted data in a target directory


