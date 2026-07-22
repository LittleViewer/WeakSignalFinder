# 🗄️ Legacy Functions

This file documents parts of Weak Signal Finder that are kept **only for backward compatibility**. They still run on every `--engine_run`, but they are not the recommended way to consume the tool's output anymore, and they receive no new features. Think of this as a heads-up, not a warning that something is broken.

---

## 📦 What's legacy

| Output | Location | Status |
|---|---|---|
| `YYYY_M_D.savestate.txt` | `saveState/` | 🧊 Frozen, backward compatibility only |
| `YYYY_M_D.dataset.txt` | `dataset/` | 🧊 Frozen, backward compatibility only |

Both are written automatically at the end of every run, alongside the current, actively maintained output at `local_api/YYYY_M_D.local_api.txt`. They exist because earlier versions of the pipeline used them as the primary output format, and some external scripts or integrations may still expect them.

---

## 🤔 Why they still exist

Removing a file format that someone else's script depends on is a breaking change with no warning. Rather than deleting `saveState/` and `dataset/` outright, they're kept in place, written on every run, exactly as before, so nothing that currently reads them silently stops working.

---

## 🧭 Should I use them for new work?

**No.** If you're integrating with Weak Signal Finder today, read from `local_api/` instead:

- It's the format actively maintained and extended (`intensity_word`, `contextual_neighborhood`, `word_central_neighborhood`, and any future fields land here first).
- It's the format the persistent dictionary loader itself consumes (`read_data_class` reads `local_api/`, not `saveState/` or `dataset/`).
- It's the one covered in detail in the [📋 Run Outputs](README.md#-run-outputs) section of the main README.

---

## 🔀 Migrating off `saveState` / `dataset`

If you have a script currently reading `saveState/` or `dataset/`, point it at `local_api/*.local_api.txt` instead. The file is newline-delimited JSON, one dated snapshot per line, see the [Output format](README.md#output-format) section of the README for the exact schema. Nothing in the underlying data is lost by switching, `local_api/` is a superset of what the legacy formats expose.

---

## ⏳ Deprecation timeline

There's no scheduled removal date yet. If and when one is set, it will be announced well in advance through the project's release notes, not silently in a patch. If you still rely on these files, keep an eye on the repository's releases page.

---

## 💬 Questions?

If you're not sure whether something you depend on falls under this legacy umbrella, or you'd like a heads-up before any future removal, feel free to reach out: **📧 littleviewer@proton.me**