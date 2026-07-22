# ❓ FAQ

Quick answers to the questions that come up most. For anything not covered here, see the full [`README.md`](README.md) or reach out at **📧 littleviewer@proton.me**.

---

### What exactly is a "weak signal"?

A weak signal is a word or topic that's **unevenly distributed** across your monitored sources, present in very few corpora, but with a high relative weight where it does appear. That's different from a simply *frequent* word: something that appears constantly everywhere (like "war" during an ongoing conflict) is a **recurring signal**, not a weak one. The `concentration` calculation in `--endpoint_user` scores exactly this distinction, see the README's [Word concentration score](README.md#word-concentration-score) section for the full breakdown.

---

### The pipeline won't start, it says a database is missing. What do I do?

Run:

```bash
python main.py --install
```

This recreates any missing folders and both SQLite databases from their schema files automatically. Restart the program afterward as instructed on screen.

---

### Do I need an internet connection to run this?

Yes. The startup diagnostics actively check connectivity before anything else runs, since RSS aggregation obviously needs it, and the pipeline will exit early with a clear message if it can't reach the network.

---

### How do I add my own RSS feeds?

Edit `libCore/input/rssFeed.json`, add an entry with a `name_organization`, `rss_link`, and `country` code:

```json
{
  "name_organization": "Le Monde",
  "rss_link": "https://www.lemonde.fr/rss/une.xml",
  "country": "fr"
}
```

---

### Can I monitor a language that isn't preinstalled?

Yes. Download the matching spaCy model and add it to `libCore/input/languageModel.json`. Full steps are in the README's [Installation](README.md#️-installation) section and in [`CONTRIBUTING.md`](CONTRIBUTING.md#-adding-a-new-language).

---

### A run finished but produced (almost) nothing. What happened?

Check the log file at `log/YYYY_M_D.log.txt` first, it's structured JSON with a `severity` field. Most "empty run" cases come from:

- A feed being unreachable (`WARN` logged, that feed is skipped).
- A language code in your feed list missing from `languageModel.json` (also skipped with a `WARN`).
- Very short articles that don't produce enough word pairs to analyze.
- The frequency floor (`filter_word` in the TOML): words appearing only once are dropped by default, lower this value if you want rarer words to survive.

---

### Why does the pipeline use so much memory / take a while to start?

spaCy's `_md` models are loaded into memory for lemmatization and can be memory-hungry, especially with several languages and a large feed list processed at once. 4 GB+ of RAM is recommended once you're monitoring more than ~10 feeds. See [System Requirements](README.md#️-system-requirements) in the README.

---

### My email notifications aren't sending. What should I check?

1. Is `authorize_run = true` under `[parameter .email_auto]` in your TOML?
2. Are you using an **App Password**, not your regular account password? (Required for Gmail with 2-Step Verification.)
3. Is `password_app.env` actually present and does it contain `PASSWORD_EMAIL=...`?
4. Is the port set to `587`? Implicit TLS on `465` isn't supported.

If the email genuinely can't be sent, the pipeline logs an `ERROR` but still finishes the run normally, it never blocks the pipeline. Check the log file for the specific SMTP error.

---

### What's `--endpoint_user` and is it safe to rely on?

It's an interactive terminal for querying the persistent dictionary directly (stats, pattern search, and the concentration calculation) without triggering a new pipeline run. It's functional but still labeled **work in progress**, the menu structure and available calculations may change between versions. It requires that at least one `--engine_run` has already populated the dictionary.

---

### What's the difference between `local_api/`, `saveState/`, and `dataset/`?

`local_api/` is the current, actively maintained output, the one to build any integration against. `saveState/` and `dataset/` are legacy formats kept only for backward compatibility, they're frozen and won't get new fields. See [`LEGACY_FUNCTION.md`](LEGACY_FUNCTION.md) for the full explanation and a migration note.

---

### If I add a new Python class, do I need to import and register it manually somewhere?

No. Classes are auto-discovered at runtime by `routerClassPackage/routerClass.py`, which scans the project tree and wires in any class it finds, as long as the file doesn't call a denylisted function (`eval`, `exec`, `os.system`, `pickle.load()`, etc.). See [`CONTRIBUTING.md`](CONTRIBUTING.md#-understanding-the-architecture-before-you-add-code) for the details and safety implications.

---

### How do I wipe everything and start fresh without deleting the `.db` files?

Run `erase_all_table.sql` against the run database and `erase_table.sql` against the dictionary database, the same way you'd apply any schema file (see [Installation, step 3](README.md#3-create-the-two-sqlite-databases)).

---

### Does this tool collect or transmit any personal data?

No. All processing happens locally. That said, **outputs are not anonymized**, if your configured feeds contain names or places, they'll appear as-is in the results and accumulate in the persistent dictionary over time. See the [Disclaimer](README.md#disclaimer) section for the full picture.

---

### Am I allowed to scrape any RSS feed I want?

That's on you to check. Some publishers prohibit automated aggregation or redistribution in their terms of service. This tool provides no guarantee of legal compliance, you're responsible for the feeds you configure.

---

### What license is this under, can I use it commercially?

[GPLv3](LICENSE). Read the license text for the exact terms before commercial use, and note that contributions are accepted under the terms of [`CLA.md`](CLA.md).

---

### I found a bug. Where do I report it?

Open a GitHub issue with the command you ran and the relevant lines from your log file. For anything that looks like a **security vulnerability**, don't open a public issue, email **littleviewer@proton.me** instead, see [`SECURITY.md`](SECURITY.md).

---

### I want to contribute, where do I start?

[`CONTRIBUTING.md`](CONTRIBUTING.md) has the full dev setup, code style notes, and a pre-PR checklist. Also worth a read: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and [`CLA.md`](CLA.md).