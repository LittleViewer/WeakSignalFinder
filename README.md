# 🔍 Weak Signal Finder

Weak Signal Finder is a Python pipeline that **detects emerging themes and weak signals** from RSS news feeds. It aggregates articles by language/country, cleans and lemmatizes the text using NLP, computes word frequency scores, builds contextual semantic neighborhoods, persists every run in a local SQLite database, and exposes the final results as a dated JSON file.

It also maintains a **persistent neighborhood dictionary** in a second SQLite database, which is enriched automatically across runs and lets you observe how each word's semantic neighborhood evolves over time. A **cross-run intensity engine** computes absolute and relative word frequencies over time, with optional weighted aggregation. An optional **SMTP email notification** can be sent at the end of every run.

---

## 📐 Architecture

```
                rssFeed.json
                     │
                     ▼
              feed_class                ← RSS aggregation (feedparser, async)
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
                     │
                     ▼
   read_data_class                      ← Reads local_api/ snapshots,
                                          extracts neighborhoods + intensity data
                     │
                     ├──► enter_data_dictionnary_class
                     │         ← Inserts new words and neighbor triplets
                     │           into the persistent dictionary
                     │
                     └──► intensity_db_word_engine_class
                              ← Cross-run word intensity computation:
                                per-corpus relative frequency, then
                                weighted multi-corpus aggregation
                     │
                     ▼
              email_smtp_class          ← Optional end-of-run SMTP notification

   ─────────────────────────────────────────────────────────────
   Support modules:
     • config_tool_class        → TOML configuration loader
     • log_class                → Logging, job ID generation, legacy outputs
     • utils_class              → File I/O, path normalization, type checks
     • date_utils_tool_class    → Date comparisons, cooldown enforcement
     • prepare_request_class    → SQLite helper (connect, insert, delete, query)
   ─────────────────────────────────────────────────────────────
   Two SQLite databases, tagged with a per-run job_id:

     • db_Weak_Signal_Finder.db
         Tables: jobIdDateTime, saveData, idCountryFeed, feedLinkRss

     • dictionnaryWord.db
         Tables: dictionnary, word, run, know_folder,
                 last_seen, intensity_word,
                 run_integrated_intensity_word,
                 multiple_intensity_word,
                 run_global_calcul_intensity
   ─────────────────────────────────────────────────────────────
```

![UML plan of WeakSignalFinder](docs/ulmvone.png)

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

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weak-signal-finder.git
cd weak-signal-finder
```

### 2. Install the dependencies

`requirements.txt` pulls spaCy **and** the medium models for English, French, German, Spanish, and Russian:

```bash
pip install -r requirements.txt
```

> **Note on package names.** The `requirements.txt` ships `dotenv`; depending on your environment you may need to replace it with `python-dotenv`. Both refer to the same library but some package managers only recognize the latter.

*(Optional)* Download an additional spaCy model if you want to support a language beyond the preinstalled set. The mapping is defined in `libCore/input/languageModel.json`. Example:

```bash
python -m spacy download it_core_news_md
```

Then add the corresponding entry to `languageModel.json`:

```json
{ "language": "Italian", "code_language": "it", "model_name": "it_core_news_md" }
```

### 3. Create the two SQLite databases

> ⚠️ **The repository does not ship with prebuilt `.db` files.** You must create both databases yourself and apply the schemas before the first run. This step is **mandatory**, the pipeline will not start without them.

The project uses **two** independent SQLite databases:

| Database file | Role | Schema |
|---|---|---|
| `database_rss_run/database_don_t_touch/db_Weak_Signal_Finder.db` | Per-run pipeline state (job IDs, raw snapshots, intensity scores, neighborhoods, feed metadata). | `database_rss_run/request/schema_db.sql` |
| `dictionnary_neighbord/database/dictionnaryWord.db` | Persistent cross-run dictionary, intensity aggregation, and tracking tables. | `dictionnary_neighbord/database/schema_table.sql` |

Create them both and load the schemas. Run all commands from the project root.

**On Linux / macOS:**

```bash
# Main run database
sqlite3 database_rss_run/database_don_t_touch/db_Weak_Signal_Finder.db \
  < database_rss_run/request/schema_db.sql

# Dictionary database
sqlite3 dictionnary_neighbord/database/dictionnaryWord.db \
  < dictionnary_neighbord/database/schema_table.sql
```

**On Windows (PowerShell):**

```powershell
Get-Content database_rss_run\request\schema_db.sql |
  sqlite3 database_rss_run\database_don_t_touch\db_Weak_Signal_Finder.db

Get-Content dictionnary_neighbord\database\schema_table.sql |
  sqlite3 dictionnary_neighbord\database\dictionnaryWord.db
```

**Alternative, pure Python (works everywhere, no `sqlite3` CLI required):**

```bash
python -c "
import sqlite3
sqlite3.connect('database_rss_run/database_don_t_touch/db_Weak_Signal_Finder.db') \
  .executescript(open('database_rss_run/request/schema_db.sql').read())
"

python -c "
import sqlite3
sqlite3.connect('dictionnary_neighbord/database/dictionnaryWord.db') \
  .executescript(open('dictionnary_neighbord/database/schema_table.sql').read())
"
```

After this step you should have:

```
database_rss_run/database_don_t_touch/db_Weak_Signal_Finder.db
dictionnary_neighbord/database/dictionnaryWord.db
```

The dictionary schema seeds initial rows in the `run`, `run_global_calcul_intensity`, and `run_integrated_intensity_word` tables (all with `jobId="0"` and a `1970-01-01` date) so that the very first execution considers every cooldown elapsed and triggers a full update. This is intentional.

> 💡 To wipe all data and start fresh without recreating the files, run `erase_all_table.sql` (run DB) and `erase_table.sql` (dictionary DB) the same way.

### 4. (Optional) Set up email notifications

See the [📧 Email Notifications (SMTP)](#-email-notifications-smtp) section below. Set `authorize_run = false` in the TOML and skip this step if you don't need it.

---

## 🚀 Usage

Once the databases are in place, run the main script from the project root:

```bash
python main.py
```

> **Run from the project root.** Paths declared in `config_weakSignalFinder.toml` are resolved relative to the current working directory. Running `python /some/other/path/main.py` from a different directory will not find the input files or the databases.

### What happens during a run

1. A unique `job_id` is generated and registered in the run database.
2. The RSS feed list is read from `libCore/input/rssFeed.json`.
3. All articles are fetched and parsed asynchronously.
4. Text is cleaned and lemmatized (spaCy POS filter: nouns, proper nouns, verbs, adjectives only).
5. Word frequency scores and semantic neighborhoods are computed.
6. Every intermediate state is persisted in the run database (tagged with the `job_id`).
7. The final result is written to `local_api/YYYY_M_D.local_api.txt`.
8. **Dictionary cooldown check.** If enough days have elapsed since the last dictionary update (see `cooldown_day_launch_dictionnary`), the pipeline reads the `local_api/` outputs and enriches the persistent neighborhood dictionary.
9. **Intensity engine.** If `authorize_run_intensity_engine = true`, per-word absolute and relative frequencies are stored in `intensity_word`. When the intensity cooldown (`cooldown_day_launch_inter_calcul_intensit_word`) is also met, a weighted multi-corpus aggregation is computed and stored in `multiple_intensity_word`.
10. **Notification email** is sent if `authorize_run = true` in `[parameter .email_auto]`.

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
| `time` | string | Human-readable timestamp of the run. |
| `time_jobid` | string | Unique job identifier for the run. |
| `intensity_word` | object | Words appearing more than once, with their frequency score. |
| `contextual_neighborhood` | object | All word pairs/triplets found in `before`, `beetween`, `after` positions. |
| `word_central_neighborhood` | object | For each word: its unique direct neighbors (left and right). |

---

## 📚 Persistent Neighborhood Dictionary

The `dictionnary_neighbord/` module is the **long-term memory** of the tool. While each run produces a snapshot of the current semantic landscape in `local_api/`, the dictionary database accumulates these snapshots over time so you can study how the neighborhood of any given word evolves.

### How it works

At the end of every run, `main.py` checks the `run` table of `dictionnaryWord.db` via `date_utils_tool_class`. If the difference (in days) between today and the most recent entry is **greater than or equal to** `cooldown_day_launch_dictionnary`, a dictionary update is triggered. Otherwise it is skipped.

When an update is triggered:

1. `read_data_class` scans `local_api/` for every dated output file, **except** those listed in `dictionnary_neighbord/exclude_file.txt` and those already recorded in the `know_folder` table.
2. It picks the JSON field configured by `part_of_local_api` (default: `word_central_neighborhood`) from every snapshot and merges all blocks into a single deduplicated structure (one `before` set and one `after` set per central word). It simultaneously extracts `intensity_word` data from each snapshot, keyed by `job_id`.
3. `enter_data_dictionnary_class` opens `dictionnaryWord.db`:
   - New central words are inserted into the `word` table, tagged with the current `job_id`.
   - New `(central_word, position, neighbor)` triplets are inserted into the `dictionnary` table. Existing triplets are skipped.
   - Words and triplets that already exist are recorded in the `last_seen` table with a timestamp and type, so you can track when known items were last encountered.
   - Consumed file names are recorded in `know_folder` to avoid re-reading.
   - The current `job_id` and date are recorded in the `run` table for cooldown enforcement.

### Database schema, `dictionnaryWord.db`

The dictionary database contains **nine** tables:

```sql
-- Core dictionary tables
CREATE TABLE IF NOT EXISTS dictionnary(
   central_word TEXT,
   position_     TEXT,        -- "before" or "after"
   word_neighbor TEXT,
   run_added     TEXT         -- job_id that inserted this triplet
);

CREATE TABLE IF NOT EXISTS word(
   word      TEXT,
   run_added TEXT,
   PRIMARY KEY(word),
   FOREIGN KEY(word) REFERENCES dictionnary(central_word)
);

-- Run tracking
CREATE TABLE IF NOT EXISTS run(
   jobId TEXT,
   date_ TEXT,
   PRIMARY KEY(jobId)
);

CREATE TABLE IF NOT EXISTS know_folder(
   jobId       TEXT,
   name_folder TEXT,
   PRIMARY KEY(name_folder)
);

-- Observation tracking
CREATE TABLE IF NOT EXISTS last_seen(
   date      TEXT,
   jobId     TEXT,
   type_seen TEXT,     -- "central_word" or "neighbord_word"
   data      TEXT,
   FOREIGN KEY (jobId) REFERENCES run(jobId)
);

-- Per-corpus intensity
CREATE TABLE IF NOT EXISTS intensity_word(
   jobId          TEXT,
   word           TEXT,
   absolute_value INTEGER,
   relative_value REAL,
   FOREIGN KEY (jobId) REFERENCES run_integrated_intensity_word(jobId),
   FOREIGN KEY (word)  REFERENCES word(word)
);

CREATE TABLE IF NOT EXISTS run_integrated_intensity_word(
   jobId TEXT,
   date  TEXT,
   PRIMARY KEY(jobId)
);

-- Cross-corpus weighted intensity
CREATE TABLE IF NOT EXISTS multiple_intensity_word(
   jobId                TEXT,
   word                 TEXT,
   absolute_value       INTEGER,
   total_relative_value REAL,
   number_corpus        INTEGER,
   relative_value       REAL,     -- weighted: total_relative_value / number_corpus
   FOREIGN KEY (jobId) REFERENCES run_integrated_intensity_word(jobId),
   FOREIGN KEY (word)  REFERENCES word(word)
);

CREATE TABLE IF NOT EXISTS run_global_calcul_intensity(
   jobId TEXT,
   date_ TEXT,
   PRIMARY KEY(jobId)
);
```

### Tuning the cooldowns

Cooldowns are set under `[parameter .for_launch]` in the TOML:

```toml
[parameter .for_launch]
cooldown_day_launch_dictionnary = 1
cooldown_day_launch_inter_calcul_intensit_word = 7
```

| Parameter | Default | Effect |
|---|---|---|
| `cooldown_day_launch_dictionnary` | `1` | Minimum days between two dictionary updates. `0` = every run. |
| `cooldown_day_launch_inter_calcul_intensit_word` | `7` | Minimum days between two cross-corpus intensity aggregations. |

### Choosing the source field

```toml
[parameter .for_launch]
part_of_local_api = "word_central_neighborhood"
```

The dictionary loader expects a `{ word: { before: [...], after: [...] } }` shape. Changing this value without adapting the loader will break the dictionary update.

### Excluding output files

`dictionnary_neighbord/exclude_file.txt` lists, one per line, the file names from `local_api/` that the dictionary loader must ignore. Defaults: `test`, `placeholder`.

---

## 📊 Cross-Run Intensity Engine

The intensity engine (`intensity_db_word_engine_class`) adds a **quantitative dimension** to the dictionary's qualitative neighborhood data. It is enabled by default and runs as part of the dictionary update step.

### How it works

1. **Per-corpus storage.** For every `local_api/` snapshot consumed, the engine extracts each word's absolute count and computes its relative frequency within that corpus (`absolute / total_words`). These values are stored in `intensity_word`, one row per `(jobId, word)`.

2. **Multi-corpus aggregation.** When the intensity cooldown (`cooldown_day_launch_inter_calcul_intensit_word`) is met, the engine reads all rows from `intensity_word`, groups them by word, and computes:
   - `total_occurence`, sum of absolute values across all corpora.
   - `total_relative_value`, sum of relative frequencies.
   - `number_corpus`, number of corpora in which the word appeared.
   - `total_relative_value_weighted`, `total_relative_value / number_corpus`.

   The result is stored in `multiple_intensity_word`.

### Configuration

```toml
[parameter .for_launch]
authorize_run_intensity_engine = true
single_multiple_intensity_save = false

[parameter .optimize]
batch_longer_list = 5000
```

| Parameter | Default | Effect |
|---|---|---|
| `authorize_run_intensity_engine` | `true` | Set to `false` to disable the intensity engine entirely. |
| `single_multiple_intensity_save` | `false` | When `true`, the `multiple_intensity_word` table is wiped before each new aggregation (useful on low-memory systems). When `false`, rows accumulate. |
| `batch_longer_list` | `5000` | Number of INSERT rows per batch commit. Higher values are faster but use more memory. |

---

## 📧 Email Notifications (SMTP)

The pipeline can send a **notification email at the end of every run**. It is optional and built on the Python standard library (`smtplib`) plus `python-dotenv` for the password.

### What it sends

When enabled, the end-of-run email contains the run's timestamp, the `job_id`, a link to the project repository, and a copyright line. If an `ERROR` or `CRITICAL` log event occurs during the run, a separate error notification is also sent with the severity, function name, and message.

If the email cannot be prepared or sent, the pipeline does **not** fail, it logs an `ERROR` and finishes normally.

### Configuration

```toml
[parameter .email_auto]
authorize_run = true
server        = "smtp.gmail.com"
port          = 587
sender        = "[EMAIL_ADDRESS]"
password_file = "password_app.env"
receiver      = "[EMAIL_ADDRESS]"
```

| Key | Role |
|---|---|
| `authorize_run` | `true` enables the email, `false` disables it entirely. |
| `server` | SMTP server hostname. Gmail = `smtp.gmail.com`. |
| `port` | SMTP submission port. Use `587` (STARTTLS). The implementation does **not** support implicit TLS on `465`. |
| `sender` | The "from" address, also used for authentication. |
| `password_file` | Path (relative to project root) of the `.env` file containing `PASSWORD_EMAIL`. |
| `receiver` | The "to" address. Can be the same as `sender`. |

### Setup (Gmail example)

1. **Enable 2-Step Verification** on your Google account.
2. **Generate a Google App Password** at <https://myaccount.google.com/apppasswords>, pick "Mail". You'll get a 16-character code.
3. **Create the password file** from the shipped template:
   ```bash
   cp archive_configuration/password_app.env.archive password_app.env
   ```
4. **Edit `password_app.env`** and replace the placeholder:
   ```env
   PASSWORD_EMAIL=abcd efgh ijkl mnop
   ```
5. **Fill `sender` and `receiver`** in `config_weakSignalFinder.toml`.

For other providers, adjust `server`, `port`, `sender`, and `PASSWORD_EMAIL`. The server must accept STARTTLS on the chosen port.

### 🔒 Security notes

- **Never commit `password_app.env`.** The `.gitignore` already excludes `*.env` and `.env`.
- **Use an App Password, not your account password.**
- **The TOML is committed, the password is not.** If `sender`/`receiver` are personal, keep the repo private or replace them with placeholders before publishing.
- **Revoke and rotate.** If the password file leaks, revoke the App Password from your provider and generate a new one.
- **Disable when unused.** Set `authorize_run = false` to fully skip the SMTP step.

---

## 🛠️ Configuration

All runtime configuration lives in a single TOML file at the project root, alongside the input files used by the NLP pipeline.

### Main configuration, `config_weakSignalFinder.toml`

Loaded once at startup by `libCore/config_tool_class.py` and consumed by every module via `key_return(table, key, sub_table)`.

```toml
[path]

[path .class_feed]
extract_feed_Path = "libCore\\input\\rssFeed.json"

[path .api_local]
open_file = "local_api\\"

[path .log]
save_data_set = "dataset\\"
save_state    = "saveState\\"
log_file      = "log\\"

[path .prepare_data]
file_model    = "libCore\\input\\languageModel.json"
file_stopword = "libCore\\input\\stopword.txt"

[path .read_data_dictionnary]
exclude_file = "dictionnary_neighbord\\exclude_file.txt"
dataset      = "local_api\\"

[path .database]
database_run_sqlite         = "database_rss_run\\database_don_t_touch\\db_Weak_Signal_Finder.db"
database_dictionnary_sqlite = "dictionnary_neighbord\\database\\dictionnaryWord.db"


[parameter]

[parameter .frequency_one_word]
filter_word = 1

[parameter .for_launch]
cooldown_day_launch_dictionnary              = 1
cooldown_day_launch_inter_calcul_intensit_word = 7
part_of_local_api                            = "word_central_neighborhood"
authorize_run_intensity_engine               = true
single_multiple_intensity_save               = false

[parameter .email_auto]
authorize_run = true
server        = "smtp.gmail.com"
port          = 587
sender        = "[EMAIL_ADDRESS]"
password_file = "password_app.env"
receiver      = "[EMAIL_ADDRESS]"

[parameter .optimize]
batch_longer_list = 5000
```

**Full parameter reference:**

| Section | Key | Role |
|---|---|---|
| `[path .class_feed]` | `extract_feed_Path` | Path to the JSON list of RSS feeds. |
| `[path .api_local]` | `open_file` | Folder where dated `*.local_api.txt` outputs are written. |
| `[path .log]` | `log_file` / `save_state` / `save_data_set` | Folders for logs, legacy savestate, and legacy dataset files. |
| `[path .prepare_data]` | `file_model` / `file_stopword` | spaCy language-model mapping and stopword list. |
| `[path .read_data_dictionnary]` | `exclude_file` / `dataset` | Dictionary exclusion list and the folder it reads from. |
| `[path .database]` | `database_run_sqlite` | Path to the per-run pipeline SQLite database. |
| `[path .database]` | `database_dictionnary_sqlite` | Path to the persistent dictionary SQLite database. |
| `[parameter .frequency_one_word]` | `filter_word` | Minimum frequency floor. Words with count ≤ this value are dropped. Default: `1`. |
| `[parameter .for_launch]` | `cooldown_day_launch_dictionnary` | Days between dictionary updates. Default: `1`. |
| `[parameter .for_launch]` | `cooldown_day_launch_inter_calcul_intensit_word` | Days between cross-corpus intensity aggregations. Default: `7`. |
| `[parameter .for_launch]` | `part_of_local_api` | JSON field consumed by the dictionary loader. Default: `word_central_neighborhood`. |
| `[parameter .for_launch]` | `authorize_run_intensity_engine` | Enable (`true`) or disable (`false`) the cross-run intensity engine. |
| `[parameter .for_launch]` | `single_multiple_intensity_save` | `true` = wipe `multiple_intensity_word` before each aggregation. `false` = accumulate. |
| `[parameter .email_auto]` | `authorize_run` | Enable/disable the SMTP notification. |
| `[parameter .email_auto]` | `server` / `port` / `sender` / `receiver` / `password_file` | SMTP connection details (see Email section). |
| `[parameter .optimize]` | `batch_longer_list` | Rows per batch INSERT commit for the intensity engine. Default: `5000`. |

> Paths use Windows-style backslashes (`\\`) but are normalized internally, the file works on Windows, Linux, and macOS.

A pristine copy is shipped as `archive_configuration/config_weakSignalFinder.toml.archive`. A `.env` template is at `archive_configuration/password_app.env.archive`.

### RSS Feeds, `libCore/input/rssFeed.json`

Each entry has a source name, a feed URL, and a country/language code:

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

Maps language codes to spaCy model names. The shipped file supports four languages:

```json
[
  { "language": "English",  "code_language": "en", "model_name": "en_core_web_md" },
  { "language": "Spanish",  "code_language": "es", "model_name": "es_core_news_md" },
  { "language": "German",   "code_language": "de", "model_name": "de_core_news_md" },
  { "language": "French",   "code_language": "fr", "model_name": "fr_core_news_md" }
]
```

> **Note.** `requirements.txt` also installs the Russian model (`ru_core_news_md`). To use it, add a corresponding entry here with `"code_language": "ru"`.

### Stopwords, `libCore/input/stopword.txt`

One word per line. Pre-populated with English/French structural words plus a thematic block tied to politics, media, and institutions. Edit freely to fit your monitoring scope, anything listed here is excluded from analysis on top of the spaCy POS filter.

### Dictionary exclusions, `dictionnary_neighbord/exclude_file.txt`

One file name per line. Any file in `local_api/` whose name appears here is skipped during dictionary enrichment. Defaults: `test`, `placeholder`.

---

## 📋 Run Outputs

Every run writes to several places, all tagged with the same `job_id`:

| Storage | Location | Role |
|---|---|---|
| **Run SQLite DB** | `database_rss_run/database_don_t_touch/db_Weak_Signal_Finder.db` | Primary per-run store. Tables: `jobIdDateTime`, `saveData`, `idCountryFeed`, `feedLinkRss`. |
| **Dictionary SQLite DB** | `dictionnary_neighbord/database/dictionnaryWord.db` | Cross-run memory. Tables: `dictionnary`, `word`, `run`, `know_folder`, `last_seen`, `intensity_word`, `run_integrated_intensity_word`, `multiple_intensity_word`, `run_global_calcul_intensity`. |
| `YYYY_M_D.local_api.txt` | `local_api/` | Final consumable JSON output; also consumed as input by the dictionary loader. |
| `YYYY_M_D.log.txt` | `log/` | Execution trace with severity levels (`INFO`, `WARN`, `ERROR`, `CRITICAL`). |
| `YYYY_M_D.savestate.txt` | `saveState/` | *Legacy file output*, kept for backward compatibility (see `LEGACY_FUNCTION.md`). |
| `YYYY_M_D.dataset.txt` | `dataset/` | *Legacy file output*, same as above. |
| End-of-run email | `receiver` mailbox | *Optional.* Sent only if `authorize_run = true`. |

> ⚠️ Do **not** open either `.db` file with another tool while the pipeline runs, risk of corruption.

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
- **Frequency floor.** Words appearing only once are filtered out by `delete_little_intensity` (controlled by `filter_word`), so very rare signals never reach the final output unless you lower the threshold.
- **Dictionary growth.** The `dictionnary` table is append-only with deduplication on `(central_word, neighbor)`. Over long monitoring periods it can grow large, plan accordingly if you set a low cooldown on a heavily configured feed list.
- **Intensity table growth.** The `intensity_word` table grows with every corpus. When `single_multiple_intensity_save = false`, `multiple_intensity_word` also accumulates across aggregation runs. Monitor database size on long-lived deployments.
- **Missing databases.** If either `.db` file is missing or uninitialized, the pipeline fails at startup. Re-run the commands from **Installation, step 3**.
- **Email failures are non-fatal.** If the SMTP step fails, the pipeline only logs an `ERROR` and exits normally.

---

## 📁 Project Structure

```
weak-signal-finder/
├── main.py
├── config_weakSignalFinder.toml
├── requirements.txt
├── password_app.env                                  ← created by you, NOT committed
├── archive_configuration/
│   ├── config_weakSignalFinder.toml.archive
│   └── password_app.env.archive
├── libCore/
│   ├── feed_class.py                                 ← RSS fetching (feedparser, async)
│   ├── prepare_data_class.py                         ← Text cleaning, spaCy lemmatization
│   ├── frequency_one_word_class.py                   ← Word frequency scoring
│   ├── contextual_neighborhood_class.py              ← Semantic neighborhood computation
│   ├── api_local_class.py                            ← JSON output writer
│   ├── email_smtp_class.py                           ← SMTP notification
│   ├── log_class.py                                  ← Logging, job ID generation
│   ├── config_tool_class.py                          ← TOML configuration loader
│   ├── utils_class.py                                ← File I/O, path, type utilities
│   ├── date_utils_tool_class.py                      ← Date comparison, cooldown logic
│   └── input/
│       ├── rssFeed.json                              ← Feed definitions
│       ├── languageModel.json                        ← Language → spaCy model mapping
│       └── stopword.txt                              ← Stopword list
├── database_rss_run/
│   ├── prepare_request_class.py                      ← SQLite helper (connect, query, insert)
│   ├── database_don_t_touch/
│   │   └── db_Weak_Signal_Finder.db                  ← created by you
│   └── request/
│       ├── schema_db.sql
│       └── erase_all_table.sql
├── dictionnary_neighbord/
│   ├── read_data_class.py                            ← Reads local_api/ snapshots
│   ├── enter_data_dictionnary_class.py               ← Inserts words & neighbors into dictionary
│   ├── intensity_db_word_engine_class.py              ← Cross-run intensity computation
│   ├── pointwise_mutual_information_engine_class.py   ← PMI engine (experimental)
│   ├── exclude_file.txt
│   └── database/
│       ├── dictionnaryWord.db                        ← created by you
│       ├── schema_table.sql
│       └── erase_table.sql
├── docs/
│   └── ulmvone.png                                   ← Architecture diagram
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

This tool is designed as an analytical aid to support **media monitoring and weak signal analysis**. The outputs are not definitive conclusions but data points intended to guide human interpretation. The quality of the analysis depends on the RSS feeds provided as input, the tool does not verify source accuracy, it solely counts and groups words without interpreting meaning.

**A high frequency score does not imply importance.** A word appearing frequently may simply be overrepresented in the selected sources. Interpret intensity scores in light of the feeds you have configured. Lemmatization quality depends on the spaCy model used, an unsuitable model may produce incorrect lemmas.

All processing is performed locally. The tool does not collect, transmit, or store personal data. **The outputs are not anonymized.** If configured feeds contain proper nouns, names, or places, these appear as-is in the results and accumulate in the persistent dictionary over time.

**Users are solely responsible for ensuring compliance with the terms of service of each RSS feed they configure.** Some publishers prohibit automated aggregation or redistribution. This tool provides no guarantee of legal compliance.