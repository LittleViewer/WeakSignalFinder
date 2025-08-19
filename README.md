# WeakSignalFinder

This project is a Python-based tool designed to perform automated content analysis on a collection of RSS English feeds. It goes beyond simple keyword counting by leveraging Natural Language Processing (NLP) to identify significant topics, measure their frequency, and, most importantly, analyze the context in which they appear.

The primary goal is to act as an intelligence-gathering tool, helping users detect "low signals"—emerging trends, topics, and relationships that are not yet obvious but are gaining traction across various information sources.

## Key Features

-   **RSS Feed Aggregation**: Automatically fetches and parses the latest entries from a list of user-defined RSS feeds.
-   **Advanced NLP Processing**: Utilizes the `nltk` library for sophisticated text analysis, including:
    -   **Tokenization**: Breaking down text into individual words.
    -   **Part-of-Speech (POS) Tagging**: Identifying the grammatical role of each word (noun, verb, etc.).
    -   **Lemmatization**: Reducing words to their root form (e.g., "technologies" becomes "technology") for accurate counting.
-   **Intelligent Keyword Extraction**: Focuses specifically on nouns (`NN`) to extract key concepts, entities, and subjects, filtering out less meaningful words.
-   **Frequency Analysis**: Counts the occurrences of significant keywords to identify the most discussed topics.
-   **Contextual Analysis**: Its core strength. The tool captures the words immediately preceding and following a key term, allowing it to identify common phrases and relationships (e.g., detecting that "security" frequently appears in the context of "data security" or "security breach").
-   **Smart Filtering**: Excludes common stopwords (like "the", "a", "is") and the names of the RSS feed sources themselves to reduce noise and improve the quality of the results.

## How It Works

The script follows a systematic pipeline to transform raw text into actionable insights:

1.  **Configuration**: Reads a list of RSS feed URLs from `lowSignal/rss.txt` and a list of custom stopwords from `lowSignal/stopword.txt`.
2.  **Data Ingestion**: Parses each RSS feed to extract the title and summary of every article.
3.  **Text Processing**: For each article, the text is combined, tokenized, and tagged for part-of-speech.
4.  **Keyword Filtering**: The script iterates through the tagged words and selects only those that are:
    -   Identified as nouns.
    -   Alphanumeric and of a reasonable length.
    -   Not present in the stopword list or the list of RSS source names.
5.  **Analysis**:
    -   **Frequency Count**: The frequency of each valid, lemmatized keyword is tallied.
    -   **Context Capture**: For each valid keyword, the immediate preceding and succeeding words (if they are also meaningful) are saved as a "context triplet" or "context pair".
6.  **Reporting**: The script outputs two lists to the console:
    -   A list of the most frequent keywords that meet a certain threshold.
    -   A list of the most frequent contexts, revealing common phrases and word associations.

## Prerequisites

-   Python 3.x
-   The following Python libraries: `feedparser`, `nltk`.

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You may need to create a `requirements.txt` file with the following content):*
    ```
    feedparser
    nltk
    ```

3.  **Download NLTK data:**
    Run the following Python script once to download the necessary NLTK models:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    ```

## Usage

1.  **Create the configuration directory:**
    ```bash
    mkdir lowSignal
    ```

2.  **Configure RSS Feeds:**
    Create a file named `lowSignal/rss.txt`. Add the URLs of the RSS feeds you want to analyze, with one URL per line.
    *Example `lowSignal/rss.txt`:*
    ```
    http://rss.cnn.com/rss/cnn_topstories.rss
    https://www.wired.com/feed/rss
    https://feeds.arstechnica.com/arstechnica/index/
    ```

3.  **Configure Stopwords:**
    Create a file named `lowSignal/stopword.txt`. Add any common or domain-specific words you wish to ignore during the analysis, with one word per line.
    *Example `lowSignal/stopword.txt`:*
    ```
    the
    is
    a
    about
    and
    ```

4.  **Run the script:**
    Execute the main Python file from your terminal.
    ```bash
    python your_script_name.py
    ```

### Understanding the Output

The script will print two types of results to the console:

-   **Important Keywords**: A list of words and their frequency count. This shows the most discussed topics.
    ```
    ['security', 15]
    ['data', 12]
    ```

-   **Important Contexts**: A list of word groups and their frequency. This reveals how topics are being discussed.
    ```
    ['data', 'security', 10]          # The phrase "data security" appeared 10 times.
    ['cyber', 'attack', 'threat', 5] # The phrase "cyber attack threat" appeared 5 times.
    ```

## How to Customize

-   **Frequency Thresholds**: You can easily change the minimum frequency for a word or context to be considered "important" by modifying the integer values in the final loops of the script (e.g., `if wordIntensity[l][1] >= 5:`).
-   **Analysis Scope**: Add or remove URLs from `rss.txt` to change the scope of your analysis.
-   **Filtering**: Expand `stopword.txt` to fine-tune the noise reduction for your specific domain.

## Reusable GitHub Action

This repository contains a reusable GitHub Action workflow to run the NLP analysis. You can use it in your own repositories to run the `lowSignal/main.py` script.

### Usage

To use this action, create a file named `.github/workflows/main.yml` in your repository with the following content:

```yaml
name: Run NLP Analysis

on:
  push:
    branches:
      - main

jobs:
  run-nlp:
    uses: alphaleadership/WeakSignalFinder/.github/workflows/main.yml@main
```

**Note:** Your repository must contain the `lowSignal/main.py` script and the necessary configuration files (`lowSignal/rss.txt`, `lowSignal/stopword.txt`, and `requirements.txt`) for the action to work correctly.