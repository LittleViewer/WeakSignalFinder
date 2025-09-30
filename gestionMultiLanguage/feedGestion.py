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
        return [language_dict, list_language_exist]
    
    def list_model_by_language(self, list_language_exist):
        data = self.scrapFeed("gestionMultiLanguage\\languageModel.json")
        for model in data:
            if model["code_language"] in list_language_exist[0]:
                list_language_exist[0][model["model_name"]] =  list_language_exist[0].pop(model["code_language"])
        print(self.delete_not_exist_model(list_language_exist[0],list_language_exist[1]))
    
    def delete_not_exist_model(self, list_model_with_feed, country_code):
        for key in list(list_model_with_feed):
            if key in country_code:
                list_model_with_feed.pop(key)
        return list_model_with_feed

    def __init__(self):
        language_dict = self.class_by_language()
        self.list_model_by_language(language_dict)
