# 🔒 Security Policy

Weak Signal Finder touches things worth taking seriously: SMTP credentials, two local SQLite databases, RSS feed parsing, and a dynamic class router that auto-discovers Python classes across the project. This policy explains how to report a problem safely.

---

## ✅ Supported Versions

| Version | Supported |
|---|---|
| `main` (latest) | ✅ Yes |
| Older tags / forks | ❌ No |

Only the latest state of the `main` branch receives security fixes. If you're running an older clone, please update before reporting.

---

## 📣 Reporting a Vulnerability

> ⚠️ **Do not open a public GitHub issue for a security vulnerability.** Public issues are for bugs and feature requests only, disclosing a vulnerability there puts every user at risk before a fix exists.

Instead, report privately by email:

**📧 littleviewer@proton.me**

Please include, as far as you're able:

- A clear description of the issue and its potential impact.
- Steps to reproduce (a minimal config, feed list, or input file helps a lot).
- The commit hash or date of the clone you tested against.
- Whether you believe the issue is exploitable remotely, locally, or only in a misconfigured deployment.

### What happens next

| Step | Target timeframe |
|---|---|
| Acknowledgment of your report | Within **72 hours** |
| Initial assessment (severity, scope) | Within **7 days** |
| Fix or mitigation, depending on severity | Best effort, prioritized by impact |

You'll be kept in the loop throughout. If a fix requires more time, you'll be told why and given a revised estimate rather than left waiting silently.

---

## 🎯 Scope

**In scope:**

- Anything in `main.py`, `core_engine_pipe.py`, `libCore/`, `database_rss_run/`, `dictionnary_neighbord/`, `endpoint_user_core/`, `routerClassPackage/`, and `install/`.
- SQL injection or unsafe query construction against either SQLite database.
- Ways to bypass the `routerClass` denylist (the check that blocks files calling `eval`, `exec`, `os.system`, `pickle.load(s)`, `yaml.load()`, `marshal.load(s)`, `shelve.open`, and similar) so that a scanned file still gets wired in.
- Credential handling issues around `password_app.env` / SMTP (e.g., leaking the password to logs, emails, or error output).
- Path traversal or unsafe file handling triggered by a crafted `rssFeed.json`, `languageModel.json`, or feed response.
- Any way for a malicious RSS feed to trigger code execution rather than just being parsed as text.

**Out of scope:**

- Vulnerabilities in third-party dependencies (spaCy, feedparser, click, etc.) that are already public, please report those to the upstream project instead.
- Issues that require an attacker to already have local shell access to the machine running the pipeline.
- The content of RSS feeds you personally choose to configure (this tool trusts the feeds you give it; it does not vet news sources).
- Denial-of-service through simply configuring an enormous number of feeds or an oversized dictionary, that's a capacity-planning concern, not a vulnerability (see the `warning_size_object` setting).

---

## 🙏 Responsible Disclosure

- Please give us a reasonable window to investigate and ship a fix before disclosing publicly.
- We're happy to credit you (by name, handle, or anonymously, your choice) once a fix is out, if you'd like.
- Good-faith security research that stays within this scope and doesn't degrade the experience of other users won't be met with legal action from this project.

---

## 🔑 A note on secrets

`password_app.env` should never be committed, it's already excluded via `.gitignore`. If you believe a credential has leaked (yours or a maintainer's), say so explicitly in your report so it can be rotated immediately, independent of any code fix.

---

Thanks for helping keep Weak Signal Finder and the people running it safe. 🙌