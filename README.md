Inquisit / Millisecond.com does not have a REST API

Data must be downloaded manually. It is recommended to configure a private server to host the data in order to have control over data automations as soon as it is collected.

The scripts in this folder aim to rename, organize, and generate metrics on completion of the task, after the dataset has been downloaded and unzipped.

# Step 1:
### rename.py 
`Converts raw inquisit data into bids structure and labels the files with a date, then converts those dates into session numbers. Attempts to extrapolate gaps in dates so that missed days are accurately represented in session number labels.`

# Step 2:
### audit.sh
`Scans bids directory and the content of files to determine completion statistics. Set a threshold for minimum number of runs that must be completed per session for the session to be considered complete (sometimes files are generated that contain little to no data.)`

# Step 3:
### plot.py
`Uses generated tsv's to plot completion rates`


