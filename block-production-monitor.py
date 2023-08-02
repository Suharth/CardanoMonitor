# -*- coding: utf-8 -*-

import requests
import time
import datetime
import logging
import os
import sys

#Set up logging configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace these placeholders with your actual values
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID" # Replace with your Telegram chat ID

#Block checking interval
HOURS=6
BLOCK_CHECK_INTERVAL = HOURS * 60 * 60

# Function to read leadership schedule from a file
def read_leadership_schedule(file_path):
    with open(file_path, "r") as file:
        # Skip the first two lines (column names and dashed line)
        lines = file.readlines()[2:]
        leadership_schedule = {}
        for line in lines:
            epoch_info = line.strip().split()
            slot_no = int(epoch_info[0])
            utc_time = epoch_info[1] + " " + epoch_info[2]
            leadership_schedule[slot_no] = utc_time
    return leadership_schedule

# Define the path to the leadership schedule file
leadership_schedule_file = "leadership_schedule.txt"
leadership_schedule = read_leadership_schedule(leadership_schedule_file)

# Function to fetch block timestamps from the API
def get_block_timestamps(pool_id, epoch):
    logger.info("Calling API to fetch block timestamps.")
    block_info = {}
    url = "https://api.koios.rest/api/v0/pool_blocks?_pool_bech32={}&_epoch_no={}".format(pool_id, epoch)
    headers = {"accept": "application/json"}
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        logger.info("API call successful.")
        data = response.json()
        for block in data:
            slot_no = block["abs_slot"]
            utc_time = datetime.datetime.utcfromtimestamp(block["block_time"]).strftime("%Y-%m-%d %H:%M:%S")
            block_info[slot_no] = utc_time
        return block_info
    else:
        logger.warning("Failed to fetch block timestamps. Status code: {}".format(response.status_code))
        return block_info

# Function to send a Telegram alert
def send_telegram_alert(alert_message):
    logger.info("Sending Telegram alert.")
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID,alert_message)
    requests.get(url).json() #bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=alert_message)

# Function to compare block production with leadership schedule
def compare_block_production(leadership_schedule,block_info):
    logger.info("Comparing block production with leadership schedule.")
    current_time = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    latest_block_time = datetime.datetime.strptime(block_info[max(block_info)], "%Y-%m-%d %H:%M:%S").replace(tzinfo=None)
    n_hours_ago = current_time - datetime.timedelta(hours=HOURS)
    if latest_block_time < n_hours_ago:
        logger.info("Comparing block production with leadership schedule.")
        send_telegram_alert("No new block in 6 hours")
    elif current_time > latest_block_time:
        for slot_no, expected_time in leadership_schedule.items():
            if datetime.datetime.strptime(expected_time, "%Y-%m-%d %H:%M:%S") < current_time:
                if slot_no not in block_info:
                    message = "Alert: Missing scheduled block!\nSlotNo: {}\nExpected Time: {}".format(slot_no,expected_time)
                    logger.warning(message)
                    send_telegram_alert(message)

# Function to calculate the epoch completion percentage
def calculate_epoch_completion(block_info, leadership_schedule):
    total_blocks = len(block_info)
    total_slots = len(leadership_schedule)
    percentage_completion = (total_blocks / total_slots) * 100
    return percentage_completion

if __name__ == "__main__":
    logger.info("Monitoring tool started.")
    pool_id = "pool1qvudfuw9ar47up5fugs53s2g84q3c4v86z4es6uwsfzzs89rwha"
    epoch = 427  # Replace with your desired epoch
    
    while True:
        block_info = get_block_timestamps(pool_id, epoch)
	completion_percentage = calculate_epoch_completion(block_info, leadership_schedule)
	logger.info("Epoch Completion Percentage: {:.2f}%".format(completion_percentage))
        compare_block_production(leadership_schedule, block_info)
        time.sleep(BLOCK_CHECK_INTERVAL)
