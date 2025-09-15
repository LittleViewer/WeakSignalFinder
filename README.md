# WeakSignalFinder

This project provides a Python-based toolkit for automated informational analysis of English-language RSS feeds. It moves beyond simple keyword counting, leveraging Natural Language Processing (NLP) to identify significant topics, quantify their prominence, and analyze their surrounding thematic context.

The primary objective is to function as a powerful intelligence-gathering aid. By processing large volumes of text, it helps analysts detect "weak signals"—emerging trends, nascent topics, and subtle shifts in discourse that are not yet mainstream but are gaining traction across diverse information sources.

## Key Features

-   **RSS Feed Aggregation**: Seamlessly aggregates and parses the latest entries from a user-defined list of RSS feeds.
-   **Advanced NLP Processing**: Leverages the high-performance `spaCy` library for production-grade text analysis, including tokenization, Part-of-Speech (POS) tagging, and lemmatization.
-   **Intelligent Keyword Extraction**: Strategically focuses on nouns to extract core concepts, entities, and subjects, filtering out less meaningful words for a cleaner signal.
-   **Visual Reporting**: Generates an instant visual summary with a `matplotlib` bar chart, highlighting the most frequent topics at a glance.
-   **Thematic Context Analysis**: This is the tool's core strength. Instead of just tracking co-occurrence, it builds a **semantic profile** for each major keyword. It aggregates all words appearing immediately before and after a key term across the entire dataset, revealing the complete thematic landscape and the nuances of how a topic is being discussed.
-   **Smart Filtering**: Reduces noise and improves signal quality by automatically excluding common stopwords and the names of the RSS feed sources from the analysis.

## How It Works

The script follows a systematic pipeline to transform raw text into actionable insights:

1.  **Configuration**: Reads a list of RSS feed URLs from `lowSignal/rss.txt` and a list of custom stopwords from `lowSignal/stopword.txt`.
2.  **Data Ingestion & Parsing**: Parses each RSS feed to extract the title and summary of every article.
3.  **Text Normalization & Filtering**: For each article, text is combined and processed by spaCy. The script then isolates significant, lemmatized nouns that are not stopwords.
4.  **Analysis**:
    -   **Frequency Count**: The frequency of each valid keyword is tallied.
    -   **Context Capture**: The immediate preceding and succeeding words for each keyword are captured.
    -   **Thematic Aggregation**: A thematic dictionary is constructed where each key is a significant topic, and its values are lists of all unique words that appeared in its immediate context.
5.  **Reporting**: The script generates three distinct outputs to provide a multi-layered view of the data:
    -   A ranked list of the most frequent keywords printed to the console.
    -   A bar chart visualizing the frequency of top keywords.
    -   A structured dictionary of thematic contexts, showing the semantic neighborhood of each topic.

## Prerequisites

-   Python 3.x
-   The following Python libraries: `feedparser`, `spacy`, `matplotlib`.

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
    *Make sure your `requirements.txt` file contains:*
    ```
    feedparser
    spacy
    matplotlib
    ```

3.  **Download spaCy Model:**
    spaCy requires a pre-trained language model. Run the following command in your terminal to download the small English model:
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

1.  **Create the configuration directory:**
    ```bash
    mkdir lowSignal
    ```

2.  **Configure RSS Feeds:**
    Create a file named `lowSignal/rss.txt`. Add the URLs of the RSS feeds you want to analyze, one per line.

3.  **Configure Stopwords:**
    Create a file named `lowSignal/stopword.txt`. Add any words you wish to ignore, one per line.

4.  **Run the script:**
    ```bash
    python main.py
    ```

### Understanding the Output

The script produces three types of results:

1.  **Important Keywords (Console Text)**: A ranked list of the most discussed topics and their raw frequency count.
    ```
    ['security', 15]
    ['trade', 12]
    ```

2.  **Topic Frequency Chart (Pop-up Window)**: A bar chart that provides a quick, visual overview of the dominant topics.

3.  **Thematic Contexts (Console Dictionary)**: This is the most powerful output, revealing the "semantic neighborhood" of each key topic. It shows *how* concepts are being framed and discussed across all sources, providing crucial context beyond simple frequency counts.
    ```python
    {
        'security': {
            'Before': ['homeland', 'aspen', 'food', 'national', 'vital'],
            'After': ['law', 'interests', 'experts', 'forum', 'guarantees']
        },
        'trade': {
            'Before': ['cold', 'free', 'reaches', 'trump'],
            'After': ['agreement', 'deal', 'disputes']
        }
    }
    ```

## How to Customize

-   **Keyword Thresholds**: Adjust the threshold in the script (e.g., `if word_intensity[y][1] >= 5:`) to control the minimum count for a word to be considered significant.
-   **Chart Customization**: In the `graph_intensity_word` function, customize the `limit` parameter to control how many top keywords are displayed in the bar chart.
-   **Analysis Scope**: Expand or narrow the scope of your analysis by adding or removing URLs from `rss.txt`.
-   **Filtering**: Refine noise reduction for your specific domain by expanding the `stopword.txt` file.

## Reusable GitHub Action

This repository contains a reusable GitHub Action that runs the NLP analysis script. The action provides the Python script and its dependencies. Your repository only needs to provide the configuration files.

### Usage

1.  In your repository, create a `lowSignal` directory.
2.  Inside `lowSignal`, add your configuration files:
    *   `rss.txt`: A list of RSS feed URLs, one per line.
    *   `stopword.txt`: A list of stopwords, one per line.
3.  Create a workflow file at `.github/workflows/main.yml` with the following content:

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

---

## Disclaimer

This tool is designed as an analytical aid to support intelligence gathering and weak signal analysis. The outputs it generates are not definitive conclusions but rather data points intended to guide and inform human interpretation. The quality, accuracy, and relevance of the analysis are directly dependent on the RSS feeds provided as input. The tool processes content as-is and does not verify the factual accuracy of the source material. The results represent a snapshot in time based on the content available at the moment of execution. Users should always apply critical judgment and cross-reference findings with other sources.
