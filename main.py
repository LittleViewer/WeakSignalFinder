import libCore.feed_class as lfC
import libCore.prepare_data_class as lpC
import libCore.log_class as llC
import libCore.utils_class as luC
import libCore.frequency_one_word_class as fowC
import libCore.contextual_neighborhood_class as cnC

lfC_ = lfC.feed()
llC_ = llC.log()
luC_ = luC.utils()
lpC_ = lpC.prepare_data()
fowC_ = fowC.frequency_one_word()
cnC_ = cnC.contextual_neighboord()

llC_.pipe_log("Start execute program", "INFO","main")
all_article = lfC_.pipe_extract_rss(luC_.absolute_link("libCore\\input\\rssFeed.json"))
data_clean_for_analyse = lpC_.pipe_prepare_data(all_article)
fowC_.pipe_frequency_one_word(data_clean_for_analyse)
neighboord_multiple_dict = cnC_.pipe_contextual_neighboord(data_clean_for_analyse)
cnC_.pipe_neighborhood_center_on_word(neighboord_multiple_dict)
llC_.pipe_log("Stop execute program", "INFO","main")
