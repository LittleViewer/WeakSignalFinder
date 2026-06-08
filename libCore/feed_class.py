import libCore.utils_class as utils
import libCore.log_class as log
import libCore.config_tool_class as ctC
import libCore.telegram_class as tgC
import feedparser
import json
import asyncio

class feed:

    def extract_feed_link(self, link):
        dict_feed = {}
        dict_telegram = {}
        if self.utC_.check_file_exist(link):
            handle = self.utC_.file_open(link)
            content = json.load(handle)
            tick = 0
            for only_one_content in content:
                source_type = only_one_content.get("type", "rss")
                if source_type == "telegram":
                    source_link = only_one_content.get("telegram_link", only_one_content.get("rss_link", ""))
                    dict_telegram = self.utC_.order_dict(source_link, only_one_content["country"], dict_telegram, tick)
                else:
                    dict_feed = self.utC_.order_dict(only_one_content["rss_link"], only_one_content["country"], dict_feed, tick)
                tick += 1
            return [dict_feed, dict_telegram]
        else:
            self.utC_.error_with_reason("Bad File Path of RSS Feed", True)

    async def parse_rss(self, dict_feed):
        list_key = list(dict_feed.keys())
        tick_feed = 0
        task = {}
        for one_key in list_key:
            task[one_key] = []
            for one_feed in dict_feed[one_key]:
                task[one_key].append(asyncio.to_thread(feedparser.parse, one_feed))
        result = {}
        for one_index in task:
            result[one_index] = await asyncio.gather(*task[one_index], return_exceptions=True)
            print(f"RSS Feed in {one_index} is read!")
        return result

    async def parse_telegram(self, dict_telegram):
        """Asynchronously fetch and parse all Telegram channels"""
        result = {}
        for country_key in dict_telegram:
            tasks = []
            for channel_url in dict_telegram[country_key]:
                tasks.append(asyncio.to_thread(self.tgC_.fetch_and_parse, channel_url))
            channel_results = await asyncio.gather(*tasks, return_exceptions=True)
            result[country_key] = channel_results
            print(f"Telegram channels in {country_key} are read!")
        return result


    def formated_result(self, parsed_feed_list):
        index_list = list(parsed_feed_list.keys())
        formated_feed_list = {}
        tick = 0
        for one_key in index_list:
            formated_feed_list[one_key] = []
            one_feed = parsed_feed_list[one_key]
            for one_index in range(len(one_feed)):
                for one_article in one_feed[one_index].entries:
                    formated_feed_list[one_key].append([getattr(one_article, "title", ""), getattr(one_article,"description",""), getattr(one_article,"published",""), getattr(one_article,"link","")])
            tick += 1
        return formated_feed_list

    def formated_telegram_result(self, parsed_telegram_list):
        """Format Telegram results into the same structure as RSS"""
        formated_list = {}
        for country_key in parsed_telegram_list:
            if country_key not in formated_list:
                formated_list[country_key] = []
            for channel_messages in parsed_telegram_list[country_key]:
                if isinstance(channel_messages, Exception):
                    self.lC_.pipe_log(f"Telegram channel fetch error: {channel_messages}", "WARN", "feed() : formated_telegram_result()")
                    continue
                if isinstance(channel_messages, list):
                    formated_list[country_key].extend(channel_messages)
        return formated_list

    def merge_sources(self, rss_formatted, telegram_formatted):
        """Merge RSS and Telegram results into a single dict keyed by country"""
        merged = dict(rss_formatted)
        for country_key in telegram_formatted:
            if country_key in merged:
                merged[country_key].extend(telegram_formatted[country_key])
            else:
                merged[country_key] = telegram_formatted[country_key]
        return merged

    async def pipe_extract_rss(self):
        sources = self.extract_feed_link(self.utC_.absolute_link(self.ctC_.key_return("path", "extract_feed_Path","class_feed")))
        dict_feed = sources[0]
        dict_telegram = sources[1]

        all_formatted = {}

        # RSS feeds
        if dict_feed:
            parsed_feed_list = await self.parse_rss(dict_feed)
            all_formatted = self.formated_result(parsed_feed_list)

        # Telegram channels
        if dict_telegram:
            parsed_telegram_list = await self.parse_telegram(dict_telegram)
            telegram_formatted = self.formated_telegram_result(parsed_telegram_list)
            all_formatted = self.merge_sources(all_formatted, telegram_formatted)

        source_count = f"RSS: {len(dict_feed)} countries" if dict_feed else "RSS: none"
        tg_count = f"Telegram: {len(dict_telegram)} countries" if dict_telegram else "Telegram: none"
        self.lC_.pipe_log(f"All articles were aggregated ({source_count}, {tg_count})","INFO","feed() : pipe_extract_rss()")
        return all_formatted


    def __init__(self):
        self.utC_ = utils.utils()
        self.lC_ = log.log()
        self.ctC_ = ctC.config_toml_tool()
        self.tgC_ = tgC.telegram()
