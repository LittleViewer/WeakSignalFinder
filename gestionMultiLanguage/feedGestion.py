import json

class feedGestion :
    def scrapFeed(self, link):
        with open(link) as handler:
            data = handler.read()
            return json.loads(data)
    
    def class_by_language(self):
        data = self.scrapFeed("gestionMultiLanguage\\rssFeed.json")
        language_dict =  {}
        list_language_exist = set([])
        for one_obj_json in data:
            if one_obj_json["language"] in list_language_exist :
                language_dict[one_obj_json["language"]].append(one_obj_json["rss_link"])
            else: 
                list_language_exist.add(one_obj_json["language"])
                language_dict[one_obj_json["language"]] = [one_obj_json["rss_link"]]
        print(language_dict)
        print(list_language_exist)

    def __init__(self):
        self.class_by_language()