# 🔍 Weak Signal Finder

Weak Signal Finder is a Python pipeline that **detects emerging themes and weak signals** from RSS news feeds. It aggregates articles by language/country, cleans and lemmatizes the text using NLP, computes word frequency scores, builds contextual semantic neighborhoods, persists every run in a local SQLite database, and exposes the final results as a dated JSON file.

---

## 📐 Architecture

```
                rssFeed.json
                     │
                     ▼
              feed_class                ← RSS aggregation (feedparser)
                     │
                     ▼
              prepare_data_class        ← Cleaning, lemmatization, stopword removal (spaCy)
                     │
                     ▼
   frequency_one_word_class             ← Word intensity / frequency scoring
   contextual_neighborhood_class        ← Semantic neighborhood computation
                     │
                     ▼
              api_local_class           ← Output as a dated local JSON file

   ─────────────────────────────────────
   Every step writes to a shared SQLite DB,
   tagged with a per-run job_id.
   Tables: jobIdDateTime, saveData
   ─────────────────────────────────────
```

![ULM plan of WeakSignalFinder](docs/ulmvone.png)

---

## 🖥️ System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.11+ |
| RAM | 2 GB | 4 GB+ |
| OS | Windows / Linux / macOS | Linux / macOS |

> spaCy `_md` language models can be memory-intensive, especially when processing large volumes of articles simultaneously. 4 GB+ of RAM is recommended if you monitor more than 10 feeds.

---

## ⚙️ Installation

1. Clone the repository (the SQLite database and required folders are already shipped with the repo, no manual init needed):

```bash
git clone https://github.com/your-username/weak-signal-finder.git
cd weak-signal-finder
```

2. Install the dependencies. `requirements.txt` already pulls spaCy **and** the medium models for English, French, German, Spanish, and Russian:

```bash
pip install -r requirements.txt
```

3. *(Optional)* Download an additional spaCy model if you want to support a language beyond the five preinstalled. The mapping is defined in `libCore/input/languageModel.json`. Example:

```bash
python -m spacy download it_core_news_md
```

---

## 🚀 Usage

Simply run the main script:

```bash
python main.py
```

> **Run from the project root.** The pipeline is designed to be launched with the project root as the working directory, either from an IDE configured that way, or from a terminal opened directly in the project folder (e.g. `cd weak-signal-finder` then `python main.py`). This is a deliberate design choice: paths declared in `config_weakSignalFinder.toml` and elsewhere are resolved relative to the current working directory, so executing `python /some/other/path/main.py` from a different location will not find the input files. It is not a bug, just how the pipeline expects to be invoked.

Each run:
1. Generates a unique `job_id` and registers it in the SQLite database.
2. Reads the RSS feed list from `libCore/input/rssFeed.json`.
3. Fetches and parses all articles asynchronously.
4. Cleans and lemmatizes the text.
5. Computes word frequency scores and semantic neighborhoods.
6. Persists every intermediate state in the database (tagged with the `job_id`).
7. Writes the final result to `local_api/YYYY_M_D.local_api.txt`.

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

All runtime configuration lives in a single TOML file at the project root, with three input files used by the NLP pipeline. Edit them to fit your monitoring scope.

### Main configuration, `config_weakSignalFinder.toml`

`config_weakSignalFinder.toml` is the **central configuration file**. It declares every path the pipeline uses (inputs, outputs, database, log/dataset/savestate folders) and exposes the tunable parameters of the analysis. It is loaded once at startup by `libCore/config_tool_class.py` and consumed by every module via `key_return(table, key, sub_table)`.

```toml
[path]

[path .class_feed]
extract_feed_Path = "libCore\\input\\rssFeed.json"

[path .api_local]
open_file = "local_api\\"

[path .log]
save_data_set = "dataset\\"
save_state = "saveState\\"
log_file = "log\\"

[path .prepare_data]
file_model = "libCore\\input\\languageModel.json"
file_stopword = "libCore\\input\\stopword.txt"

[path .database]
database_sqlite = "database\\database_don_t_touch\\db_Weak_Signal_Finder.db"


[parameter]

[parameter .frequency_one_word]
filter_word = 1
```

**Section reference:**

| Section | Key | Role |
|---|---|---|
| `[path .class_feed]` | `extract_feed_Path` | Path to the JSON list of RSS feeds. |
| `[path .api_local]` | `open_file` | Folder where the dated `*.local_api.txt` output is written. |
| `[path .log]` | `log_file` / `save_state` / `save_data_set` | Folders for the execution log, the legacy savestate file, and the legacy dataset file. |
| `[path .prepare_data]` | `file_model` / `file_stopword` | Path to the spaCy language-model mapping and to the stopword list. |
| `[path .database]` | `database_sqlite` | Path to the SQLite database file. |
| `[parameter .frequency_one_word]` | `filter_word` | Minimum frequency floor, words with a count `<=` this value are dropped from the final output. Default: `1`. |

> Paths use Windows-style backslashes (`\\`) but are normalized internally, so the file works the same on Windows, Linux, and macOS.

A pristine copy of the configuration is shipped as **`archive_configuration/config_weakSignalFinder.toml.archive`**. If you ever break the active TOML during edits, you can restore the defaults by copying this archive back to `config_weakSignalFinder.toml` at the project root.

### RSS Feeds, `libCore/input/rssFeed.json`

Define the feeds to monitor. Each entry has a source name, a feed URL, and a country/language code:

```json
[
  {
    "name_organization": "Le Monde",
    "rss_link": "https://www.lemonde.fr/rss/une.xml",
    "country": "fr"
  },
  {
    "name_organization": "BBC News",
    "rss_link": "https://feeds.bbci.co.uk/news/rss.xml",
    "country": "en"
  }
]
```

### Language Models, `libCore/input/languageModel.json`

Maps language codes to their spaCy model names. The `language` field is informational, `code_language` is the key actually used to dispatch articles:

```json
[
  { "language": "French",  "code_language": "fr", "model_name": "fr_core_news_md" },
  { "language": "English", "code_language": "en", "model_name": "en_core_web_md" }
]
```

### Stopwords, `libCore/input/stopword.txt`

One word per line. The shipped file is **pre-populated** with a large default set: English/French structural words plus a thematic block tied to politics, media, and institutions (e.g. `parliament`, `commission`, `bbc`, `nytimes`, `monday`, `region`, `million`...). Edit it freely to fit your monitoring scope, anything listed here is excluded from analysis on top of the spaCy POS filter (only nouns, proper nouns, verbs, and adjectives are kept).

---

## 📋 Run Outputs

Every run writes to several places, all tagged with the same `job_id`:

| Storage | Location | Role |
|---|---|---|
| **SQLite DB** | `database/database_don_t_touch/db_Weak_Signal_Finder.db` | **Primary store.** Contains the `jobIdDateTime` table (one row per run) and the `saveData` table (raw and cleaned snapshots, intensity scores, neighborhoods). |
| `YYYY_M_D.local_api.txt` | `local_api/` | Final consumable JSON output. |
| `YYYY_M_D.log.txt` | `log/` | Execution trace with severity levels (`INFO`, `WARN`, `ERROR`, `CRITICAL`) and the calling function. |
| `YYYY_M_D.savestate.txt` | `saveState/` | *Legacy file output*, kept for backward compatibility (see `LEGACY_FUNCTION.md`). The database is now the source of truth. |
| `YYYY_M_D.dataset.txt` | `dataset/` | *Legacy file output*, same as above. |

> ⚠️ Do **not** open `db_Weak_Signal_Finder.db` manually with another tool while the pipeline runs, risk of corruption.

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

- **Silent skips.** Single-word articles, unreachable feeds, and language codes missing from `languageModel.json` are skipped without raising an exception (a `WARN` is logged when relevant). If a run produces nothing, check the log file.
- **Frequency floor.** Words appearing only once are filtered out by `delete_little_intensity` (controlled by `filter_word` in the TOML), so very rare signals never reach the final output unless you lower the threshold.

---

## 📁 Project Structure

```
weak-signal-finder/
├── main.py
├── config_weakSignalFinder.toml
├── archive_configuration/
│   └── config_weakSignalFinder.toml.archive
├── libCore/
│   ├── feed_class.py
│   ├── prepare_data_class.py
│   ├── frequency_one_word_class.py
│   ├── contextual_neighborhood_class.py
│   ├── api_local_class.py
│   ├── log_class.py
│   ├── config_tool_class.py
│   ├── utils_class.py
│   └── input/
│       ├── rssFeed.json
│       ├── languageModel.json
│       └── stopword.txt
├── database/
│   ├── prepare_request_class.py
│   ├── database_don_t_touch/
│   │   └── db_Weak_Signal_Finder.db
│   └── request/
│       ├── request_savedata.sql
│       ├── request_idCountry.sql
│       └── erase_all_table.sql
├── log/
├── saveState/
├── dataset/
└── local_api/
```

---

## 🤝 Contributing

Contributions are welcome. Before opening a pull request, please review:

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), community standards.
- [`CLA.md`](CLA.md), the Individual Contributor License Agreement you implicitly accept by submitting a contribution.
- [`SECURITY.md`](SECURITY.md), how to responsibly disclose a vulnerability (do **not** open a public issue for security matters).

---

## Disclaimer

This tool is designed as an analytical aid to support **media monitoring and weak signal analysis**. The outputs it generates are not definitive conclusions but rather data points intended to guide and inform human interpretation. The quality, accuracy, and relevance of the analysis are directly dependent on the RSS feeds provided as input. The tool does not verify the factual accuracy or reliability of the source material, it solely counts and groups words without interpreting meaning. The results represent a snapshot in time based on the content available at the moment of execution.
**A high frequency score does not imply importance.** A word that appears frequently across feeds may simply be overrepresented in the selected sources, not genuinely significant. Users should interpret intensity scores in light of the feeds they have configured. The quality of lemmatization and part-of-speech filtering depends on the spaCy language model used. An unsuitable or low-accuracy model may produce incorrect lemmas and distort the analysis. It is recommended to use a model appropriate to the language and domain of your feeds. All processing is performed locally. The tool does not collect, transmit, or store any personal data. All output files remain on the user's machine.
**The outputs are not anonymized.** If the configured RSS feeds contain proper nouns, names of individuals, organizations, or places, these will appear as-is in the semantic neighborhood results and output files. Users operating in a professional, shared, or regulated environment should be aware of this and handle the output files accordingly.
**Users are solely responsible for ensuring compliance with the terms of service of each RSS feed they configure.** Some publishers explicitly prohibit automated aggregation or redistribution of their content. This tool provides no guarantee of legal compliance for any given feed, and the responsibility for verifying authorized use rests entirely with the user. Users should always apply critical judgment and cross-reference findings with other sources before drawing any conclusions.
