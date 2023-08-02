# Cardano Block Production Monitor

The Cardano Block Production Monitor is a Python-based tool designed to monitor the production of blocks for a Cardano stake pool during a specific epoch. It compares the actual block production with the leadership schedule to identify any discrepancies or missing blocks.

## Features
* Fetches block timestamps using the Koios REST API.
* Compares block production with the provided leadership schedule.
* Sends Telegram alerts for missing blocks or prolonged periods of inactivity.
* Displays the epoch completion percentage in the logs.

## Prerequisites
* Python 3.x

## Getting Started
1. Clone repository:
<pre>
git clone https://github.com/yourusername/CardanoMonitor.git
cd CardanoMonitor
</pre>
2. Create a virtual environment (optional but recommended):
<pre>
python3 -m venv venv
source venv/bin/activate
</pre>
3. Install the required packages:
<pre>
pip install -r requirements.txt
</pre>
4. Configure the tool by editing 'block-production-monitor.py':
   * Replace YOUR_BOT_TOKEN with your actual Telegram bot token.
   * Replace YOUR_CHAT_ID with your actual Telegram chat ID.
   * Set the 'epoch' variable appropriately
5. Make sure 'leadership_schedule.txt' contains information of the epoch you want.

## Usage
### Running the Script
To run the monitoring tool as a standalone script, execute the following command:
<pre>
python3 block-production-monitor.py
</pre>
### Running as a Systemd Service (Linux)
1. Open block_monitor.service and modify the 'User', 'Group', 'WorkingDirectory' and 'ExecStart' fields as needed.
2. Copy block_monitor.service to '/etc/systemd/system/':
<pre>
sudo cp block_monitor.service /etc/systemd/system/
</pre>
3. Reload the systemd manager configuration:
<pre>
sudo systemctl daemon-reload
</pre>
4. Start and enable the service:
<pre>
sudo systemctl start block_monitor.service
sudo systemctl enable block_monitor.service
</pre>
### Monitoring the Progress (Checking Logs)
The monitoring tool utilizes the systemd service to ensure continuous execution and logs its activities using the system journal. The service configuration directs the output of the tool's logs to the journal, which can be accessed using the journalctl command. To view the logs in real-time as the monitoring tool runs, use the following command:
<pre>
sudo journalctl -u block_monitor.service -f
</pre>
### Stopping the Monitoring Tool
If you wish to stop the Block Monitoring Tool that you have set up as a systemd service, follow these steps:
1. Open a terminal window.
2. Run the following command to stop the service:
<pre>
sudo systemctl stop block_monitor.service
</pre>
   This will immediately stop the monitoring tool
3. If you want to disable the automatic startup of the service at system boot, you can run:
<pre>
sudo systemctl disable block_monitor.service
</pre>
  This will prevent the service from starting automatically the next time you boot your system.
By stopping the service, you can temporarily halt the monitoring process. Remember that you can always start it again using the command sudo systemctl start block_monitor.service.
