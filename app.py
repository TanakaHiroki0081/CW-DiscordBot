import sys
import json
import threading
import time
import logging
from main_ui import MainUI
from scraper import CrowdWorksScraper
from filter import JobFilter
from discord_bot import DiscordJobBot
from PyQt5.QtWidgets import QApplication

CONFIG_FILE = 'config.json'
LOG_FILE = 'logs/app.log'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(cfg):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def monitor_loop(ui, stop_event):
    while not stop_event.is_set():
        try:
            url = ui.url_input.text()
            lower = ui.lower_price.value()
            upper = ui.upper_price.value()
            channel_id = ui.channel_id_input.text()
            token = ui.token_input.text()
            interval = ui.poll_interval.value()
            save_config({
                'url': url,
                'lower_price': lower,
                'upper_price': upper,
                'channel_id': channel_id,
                'poll_interval': interval
            })
            scraper = CrowdWorksScraper(url)
            jobs = scraper.fetch_jobs()
            ftr = JobFilter(lower, upper)
            new_jobs = ftr.filter_jobs(jobs)
            if new_jobs:
                bot = DiscordJobBot(token, channel_id)
                bot.run(new_jobs)
                ui.status_display.append(f"Posted {len(new_jobs)} new jobs.")
                logging.info(f"Posted {len(new_jobs)} new jobs.")
            else:
                ui.status_display.append("No new jobs found.")
                logging.info("No new jobs found.")
        except Exception as e:
            msg = f"Error: {e}"
            ui.status_display.append(msg)
            logging.error(msg)
        for _ in range(ui.poll_interval.value() * 60):
            if stop_event.is_set():
                break
            time.sleep(1)

def main():
    app = QApplication(sys.argv)
    ui = MainUI()
    cfg = load_config()
    if cfg:
        ui.url_input.setText(cfg.get('url', ''))
        ui.lower_price.setValue(cfg.get('lower_price', 0))
        ui.upper_price.setValue(cfg.get('upper_price', 10000))
        ui.channel_id_input.setText(cfg.get('channel_id', ''))
        ui.poll_interval.setValue(cfg.get('poll_interval', 5))
    stop_event = threading.Event()
    thread = None
    def start():
        nonlocal thread
        if thread and thread.is_alive():
            return
        stop_event.clear()
        thread = threading.Thread(target=monitor_loop, args=(ui, stop_event), daemon=True)
        thread.start()
        ui.status_display.append('Started monitoring.')
    def stop():
        stop_event.set()
        ui.status_display.append('Stopped monitoring.')
    ui.start_btn.clicked.connect(start)
    ui.stop_btn.clicked.connect(stop)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

