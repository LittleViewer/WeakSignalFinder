import libCore.utils_class as utils
import libCore.log_class as log
import libCore.config_tool_class as ctC
import requests
import re
from bs4 import BeautifulSoup

class telegram:

    def extract_channel_name(self, url):
        """Extract channel name from t.me/s/channelname URL"""
        match = re.search(r't\.me/s/([a-zA-Z0-9_]+)', url)
        if match:
            return match.group(1)
        match = re.search(r't\.me/([a-zA-Z0-9_]+)', url)
        if match:
            return match.group(1)
        return None

    def fetch_channel_page(self, url):
        """Fetch public Telegram channel web preview page"""
        channel_name = self.extract_channel_name(url)
        if not channel_name:
            self.lC_.pipe_log(f"Invalid Telegram channel URL: {url}", "ERROR", "telegram() : fetch_channel_page()")
            return None

        fetch_url = f"https://t.me/s/{channel_name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

        try:
            response = requests.get(fetch_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.lC_.pipe_log(f"Failed to fetch Telegram channel {channel_name}: {e}", "ERROR", "telegram() : fetch_channel_page()")
            return None

    def parse_messages(self, html_content, channel_url):
        """Parse Telegram messages from the web preview HTML"""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        messages = []

        message_wraps = soup.find_all("div", class_="tgme_widget_message")

        for msg in message_wraps:
            text_div = msg.find("div", class_="tgme_widget_message_text")
            if not text_div:
                continue

            message_text = text_div.get_text(separator=" ", strip=True)
            if not message_text:
                continue

            # title: first line or first 120 chars
            first_line = message_text.split("\n")[0].strip()
            title = first_line[:120] if len(first_line) > 120 else first_line

            # description: full text
            description = message_text

            # date
            published = ""
            time_tag = msg.find("time", {"datetime": True})
            if time_tag:
                published = time_tag.get("datetime", "")

            # link
            link = ""
            date_link = msg.find("a", class_="tgme_widget_message_date")
            if date_link and date_link.get("href"):
                link = date_link["href"]
            elif msg.get("data-post"):
                link = f"https://t.me/{msg['data-post']}"

            messages.append([title, description, published, link])

        return messages

    def fetch_and_parse(self, url):
        """Fetch a Telegram channel and return parsed messages"""
        html = self.fetch_channel_page(url)
        messages = self.parse_messages(html, url)
        self.lC_.pipe_log(f"Telegram channel {url}: {len(messages)} messages extracted", "INFO", "telegram() : fetch_and_parse()")
        return messages

    def __init__(self):
        self.utC_ = utils.utils()
        self.lC_ = log.log()
        self.ctC_ = ctC.config_toml_tool()
