import libCore.utils_class as utils
import libCore.log_class as log
import feedparser
import json
import asyncio

class feed:

    def extract_feed_link(self, link):
        dict_feed = {}
        if self.utC_.check_file_exist(link):
            handle = self.utC_.file_open(link)
            content = json.load(handle)
            tick = 0
            for only_one_content in content:
                dict_feed = self.utC_.order_dict(only_one_content["rss_link"], only_one_content["country"], dict_feed, tick)
                tick += 1
            return dict_feed                
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
    
    async def pipe_extract_rss(self, link = "configFolder/rssFeed.json"):
        dict_feed = self.extract_feed_link(self.utC_.absolute_link(link))
        parsed_feed_list = await self.parse_rss(dict_feed)
        formated_feed = self.formated_result(parsed_feed_list)
        total_article = 0
        for one_index in formated_feed:
            total_article =+ len(formated_feed[one_index])
        self.lC_.pipe_log(f"{total_article} articles were aggregated via Feed RSS","INFO","feed() : pipe_extract_rss()")
        return formated_feed


    def __init__(self):
        self.utC_ = utils.utils()
        self.lC_ = log.log()
        