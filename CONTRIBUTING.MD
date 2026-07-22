# 🛠️ Contributing to Weak Signal Finder

Thanks for considering a contribution, whether it's a bug fix, a new language, a doc improvement, or a whole new module. This guide covers everything you need to get set up and send a good pull request.

---

## 📋 Before you start

Please read these first, they're short:

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), how we expect people to treat each other here.
- [`CLA.md`](CLA.md), the Individual Contributor License Agreement you implicitly accept by submitting a contribution.
- [`SECURITY.md`](SECURITY.md), if what you found is a **vulnerability**, report it privately instead of opening a PR or public issue.

---

## 🧰 Setting up a dev environment

```bash
git clone https://github.com/LittleViewer/WeakSignalFinder.git
cd WeakSignalFinder
pip install -r requirements.txt
```

Then create both SQLite databases before running anything:

```bash
python main.py --install
```

Copy the config and email templates so you have your own sandbox to test against:

```bash
cp archive_configuration/config_weakSignalFinder.toml.archive config_weakSignalFinder.toml
cp archive_configuration/password_app.env.archive password_app.env
```

Set `authorize_run = false` under `[parameter .email_auto]` while developing, unless you're specifically testing the SMTP path, no need to spam a real inbox on every test run.

Run the pipeline in silent mode to iterate faster without the startup banner:

```bash
python main.py --engine_run --silent_mode
```

---

## 🧩 Understanding the architecture before you add code

This matters more here than in most projects: **classes are not manually imported and wired together**. `routerClassPackage/routerClass.py` walks the project tree at runtime, finds every class definition via AST parsing, and exposes them by name through `obj_class_router["YourClassName"]`.

Practical implications for contributors:

- If you add a new class anywhere under the project root, it's **auto-discovered**, you don't need to register it anywhere by hand.
- **Do not** call any of the denylisted functions (`eval`, `exec`, `os.system`, `os.popen`, `subprocess.run`, `pickle.load()`/`loads()`, `yaml.load()`, `marshal.load()`/`loads()`, `shelve.open`) anywhere in a file that defines a class you want discovered, the router will silently skip that file for safety. If your feature genuinely needs one of these, open an issue first, so we can discuss a safe way to do it.
- Keep one primary class per file where possible, it matches the existing style and keeps the router's discovery predictable.

---

## 🎨 Code style

- Match the existing naming convention: `snake_case` for functions/variables, `PascalCase`-ish class names ending in `_class` where the codebase already does so (e.g. `feed_class`, `log_class`).
- Prefer small, single-purpose methods (`pipe_*` methods that orchestrate, smaller private-ish helpers underneath), the existing modules follow this pattern.
- New config values go in `config_weakSignalFinder.toml` **and** in `archive_configuration/config_weakSignalFinder.toml.archive`, plus a row in the parameter reference table in `README.md`.
- No hardcoded absolute paths, everything should resolve through `utils_class` / `config_tool_class` like the rest of the code.

---

## 🌐 Adding a new language

1. Download the spaCy model: `python -m spacy download <model_name>`.
2. Add an entry to `libCore/input/languageModel.json`:
   ```json
   { "language": "Italian", "code_language": "it", "model_name": "it_core_news_md" }
   ```
3. Add the model's wheel URL to `requirements.txt` if you'd like it preinstalled for everyone, otherwise leave it as an opt-in step documented in the README.
4. Mention the addition in your PR description so it can be called out in the changelog.

---

## ✅ Before opening a pull request

- [ ] Run the pipeline end-to-end at least once (`python main.py --engine_run`) with your change and confirm it doesn't crash or silently produce empty output.
- [ ] If you touched the database schema, update **both** `schema_db.sql`/`schema_table.sql` and their `erase_*.sql` counterparts.
- [ ] If you added or changed a config key, update `README.md`'s parameter reference table and the `.archive` template.
- [ ] Keep the PR focused, one feature or fix per PR is much easier to review than a bundle of unrelated changes.
- [ ] Add a short entry to [`CHANGELOG.md`](CHANGELOG.md) under `Unreleased`.

---

## 🐛 Reporting bugs (non-security)

Open a GitHub issue with:

- What you ran (exact command / flags).
- What you expected vs. what happened.
- The relevant lines from your log file (`log/YYYY_M_D.log.txt`), logs are structured JSON and usually pinpoint the failing function fast.

For anything security-sensitive, see [`SECURITY.md`](SECURITY.md) instead, do not open a public issue.

---

## 💬 Questions

Not sure whether something belongs in a PR, an issue, or just a question? Reach out at **📧 littleviewer@proton.me**, happy to point you in the right direction.

Thanks again for helping improve Weak Signal Finder! 🙌