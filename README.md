# 🔍 Weak Signal Finder

Weak Signal Finder is a Python pipeline that **detects emerging themes and weak signals** from RSS news feeds. It aggregates articles by language/country, cleans and lemmatizes the text using NLP, computes word frequency scores, and builds contextual semantic neighborhoods, then exposes all results via a local JSON API.

---

## 📐 Architecture

```
rssFeed.json
     │
     ▼
 feed_class          ← RSS aggregation (feedparser)
     │
     ▼
 prepare_data_class  ← Cleaning, lemmatization, stopword removal (spaCy)
     │
     ▼
 frequency_one_word_class     ← Word intensity / frequency scoring
 contextual_neighborhood_class ← Semantic neighborhood computation
     │
     ▼
 api_local_class     ← Output as a dated local JSON file
```
![ULM plan of WeakSignalFinder](docs\ulmv1.png)
---

## 🖥️ System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.11+ |
| RAM | 2 GB | 4 GB+ |
| OS | Windows / Linux / macOS | Linux / macOS |

> spaCy language models can be memory-intensive, especially when processing large volumes of articles simultaneously. 4 GB+ of RAM is recommended if you monitor more than 10 feeds.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/weak-signal-finder.git
cd weak-signal-finder
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Download the required spaCy language model(s) defined in `libCore/input/languageModel.json`. Example for French and English:

```bash
python -m spacy download fr_core_news_sm
python -m spacy download en_core_web_sm
```

4. Make sure the following directories exist at the project root (they are used for output and logs):

```
log/
saveState/
dataset/
local_api/
```

---

## 🚀 Usage

Simply run the main script:

```bash
python main.py
```
>⚠️ Important : It is strongly recommended to run this program from a Unix system or via an IDE (e.g. VSCode).
>On Windows, the program must be launched from its own directory (C:\...\WeakSignalFinder), otherwise file paths will not resolve correctly.
>To do so, open a terminal in the project folder and run : python main.py

The pipeline will:
1. Read the RSS feed list from `libCore/input/rssFeed.json`
2. Fetch and parse all articles
3. Clean and lemmatize the text
4. Compute word frequency scores and semantic neighborhoods
5. Write the results to `local_api/YYYY_M_D.local_api.txt`

### Output format

The output is a newline-delimited JSON file. Each line is a full dated snapshot:

```json
{
  "time": "[2024-01-15 08:30:00]",
  "time_jobid": "[202411300123456]",
  "intensity_word": {
    "climate": 42,
    "energy": 31,
    "transition": 18
  },
  "contextual_neighborhood": {
    "before":   [["energy", "climate"], ["new", "policy"]],
    "beetween": [["green", "energy", "policy"], ["rapid", "climate", "shift"]],
    "after":    [["climate", "change"], ["policy", "reform"]]
  },
  "word_central_neighborhood": {
    "climate": { "before": ["energy", "new"], "after": ["change", "policy"] },
    "energy":  { "before": ["green", "cheap"], "after": ["transition", "crisis"] }
  }
}
```

**Field reference:**

| Field | Type | Description |
|---|---|---|
| `time` | string | Human-readable timestamp of the run |
| `time_jobid` | string | Unique job identifier for the run |
| `intensity_word` | object | Words appearing more than once, with their frequency score |
| `contextual_neighborhood` | object | All word pairs/triplets found in `before`, `beetween`, `after` positions |
| `word_central_neighborhood` | object | For each word: its unique direct neighbors (left and right) |

---

## 🛠️ Configuration

### RSS Feeds, `libCore/input/rssFeed.json`

Define the feeds to monitor, grouped by country/language code:

```json
[
  { "country": "fr", "rss_link": "https://www.lemonde.fr/rss/une.xml" },
  { "country": "en", "rss_link": "https://feeds.bbci.co.uk/news/rss.xml" }
]
```

### Language Models, `libCore/input/languageModel.json`

Maps language codes to their spaCy model names:

```json
[
  { "code_language": "fr", "model_name": "fr_core_news_sm" },
  { "code_language": "en", "model_name": "en_core_web_sm" }
]
```

### Stopwords, `libCore/input/stopword.txt`

One word per line. These words are excluded from the analysis in addition to the spaCy POS filter (only nouns, proper nouns, verbs and adjectives are kept).

```
the
and
for
...
```

---

## 📋 Log & State Files

The pipeline automatically generates several output files each day, all named with the pattern `YYYY_M_D.*`:

| File | Location | Description |
|---|---|---|
| `YYYY_M_D.log.txt` | `log/` | Execution trace with severity levels (`INFO`, `WARN`, `ERROR`, `CRITICAL`) and the calling function |
| `YYYY_M_D.savestate.txt` | `saveState/` | Two snapshots of the article data: one before NLP cleaning (`Brut`) and one after (`Clean`) |
| `YYYY_M_D.dataset.txt` | `dataset/` | Intermediate datasets: word intensity and semantic neighborhoods |
| `YYYY_M_D.local_api.txt` | `local_api/` | Final output, the full JSON result ready to be consumed |

Each log entry is a JSON object:

```json
{
  "content": "The word intensity is calculated as well as saved in the dataset.",
  "severity": "INFO",
  "function_call": "frequency_one_word() : pipe_frequency_one_word()",
  "timestamp": "2024-01-15 08:30:12.456789"
}
```

---

## ⚠️ Known Limitations

- **Single-word blocks are silently skipped.** If an article produces only one meaningful word after cleaning, its contextual neighborhood cannot be computed and it is ignored without raising an error.
- **Inaccessible feeds do not raise a soft error.** If a feed URL is unreachable, `feedparser` returns an empty result, the pipeline continues without warning.
- **Language code must match exactly.** If a `country` key in `rssFeed.json` does not appear in `languageModel.json`, the language is skipped with a `WARN` log but no exception is raised.
- **Words appearing only once are filtered out.** The `delete_little_intensity` function removes any word with a frequency ≤ 1, so very rare signals are excluded from the final output.
- **Output directories must exist before running.** The pipeline does not auto-create `log/`, `saveState/`, `dataset/`, or `local_api/`, missing directories will cause a crash.

---

## 📁 Project Structure

```
weak-signal-finder/
├── main.py
├── libCore/
│   ├── feed_class.py
│   ├── prepare_data_class.py
│   ├── frequency_one_word_class.py
│   ├── contextual_neighborhood_class.py
│   ├── api_local_class.py
│   ├── log_class.py
│   ├── utils_class.py
│   └── input/
│       ├── rssFeed.json
│       ├── languageModel.json
│       └── stopword.txt
├── log/
├── saveState/
├── dataset/
└── local_api/
```
---

## Disclaimer

This tool is designed as an analytical aid to support **media monitoring and weak signal analysis**. The outputs it generates are not definitive conclusions but rather data points intended to guide and inform human interpretation. The quality, accuracy, and relevance of the analysis are directly dependent on the RSS feeds provided as input. The tool does not verify the factual accuracy or reliability of the source material, it solely counts and groups words without interpreting meaning. The results represent a snapshot in time based on the content available at the moment of execution. 
**A high frequency score does not imply importance.** A word that appears frequently across feeds may simply be overrepresented in the selected sources, not genuinely significant. Users should interpret intensity scores in light of the feeds they have configured. The quality of lemmatization and part-of-speech filtering depends on the spaCy language model used. An unsuitable or low-accuracy model may produce incorrect lemmas and distort the analysis. It is recommended to use a model appropriate to the language and domain of your feeds. All processing is performed locally. The tool does not collect, transmit, or store any personal data. All output files remain on the user's machine.
**The outputs are not anonymized.** If the configured RSS feeds contain proper nouns, names of individuals, organizations, or places, these will appear as-is in the semantic neighborhood results and output files. Users operating in a professional, shared, or regulated environment should be aware of this and handle the output files accordingly.
**Users are solely responsible for ensuring compliance with the terms of service of each RSS feed they configure.** Some publishers explicitly prohibit automated aggregation or redistribution of their content. This tool provides no guarantee of legal compliance for any given feed, and the responsibility for verifying authorized use rests entirely with the user. Users should always apply critical judgment and cross-reference findings with other sources before drawing any conclusions.
