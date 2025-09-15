# WeakSignalFinder

This project is a Python-based tool designed to perform automated content analysis on a collection of English RSS feeds. It goes beyond simple keyword counting by leveraging Natural Language Processing (NLP) to identify significant topics, measure their frequency, and analyze the thematic context in which they appear.

The primary goal is to act as an intelligence-gathering tool, helping users detect "weak signals"—emerging trends, topics, and relationships that are not yet obvious but are gaining traction across various information sources.

## Key Features

-   **RSS Feed Aggregation**: Automatically fetches and parses the latest entries from a list of user-defined RSS feeds.
-   **Advanced NLP Processing**: Utilizes the `spaCy` library for efficient, production-grade text analysis, including tokenization, Part-of-Speech (POS) tagging, and lemmatization.
-   **Intelligent Keyword Extraction**: Focuses specifically on nouns to extract key concepts, entities, and subjects, filtering out less meaningful words.
-   **Visual Reporting**: Automatically generates a bar chart of the most frequent topics using `matplotlib`, providing an immediate visual summary of the data.
-   **Thematic Context Analysis**: Its core strength. Instead of just counting simple pairs or triplets, the tool builds a **semantic profile** for each major keyword. It aggregates all words that appear immediately before and after a key term across the entire dataset, revealing the complete thematic landscape around a topic.
-   **Smart Filtering**: Excludes common stopwords and the names of the RSS feed sources themselves to reduce noise and improve the quality of the results.

## How It Works

The script follows a systematic pipeline to transform raw text into actionable insights:

1.  **Configuration**: Reads a list of RSS feed URLs from `lowSignal/rss.txt` and a list of custom stopwords from `lowSignal/stopword.txt`.
2.  **Data Ingestion**: Parses each RSS feed to extract the title and summary of every article.
3.  **Text Processing & Filtering**: For each article, the text is combined and processed by spaCy. The script filters to keep only significant, lemmatized nouns that are not stopwords.
4.  **Analysis**:
    -   **Frequency Count**: The frequency of each valid keyword is tallied.
    -   **Context Capture**: The immediate preceding and succeeding words for each keyword are captured.
    -   **Thematic Aggregation**: The script builds a dictionary where each key is a significant topic, and the values are lists of all unique words that appeared before or after it.
5.  **Reporting**: The script generates three distinct outputs to provide a multi-layered view of the data:
    -   A list of the most frequent keywords printed to the console.
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

1.  **Important Keywords (Console Text)**: A simple list of the most discussed topics and their raw frequency count.
    ```
    ['security', 15]
    ['trade', 12]
    ```

2.  **Topic Frequency Chart (Pop-up Window)**: A bar chart that visually represents the most frequent keywords, allowing for a quick overview of the main topics.

3.  **Thematic Contexts (Console Dictionary)**: The most powerful output. It's a dictionary showing the complete "semantic neighborhood" for each key topic. This reveals how concepts are being discussed across all sources.
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

-   **Keyword Thresholds**: Modify the integer values in the filtering loops of the script (e.g., `if word_intensity[y][1] >= 5:`) to change the minimum count for a word to be considered important.
-   **Chart Customization**: In the `graph_intensity_word` function, change the `limit` parameter to control how many of the top keywords are displayed in the bar chart.
-   **Analysis Scope**: Add or remove URLs from `rss.txt` to change the scope of your analysis.
-   **Filtering**: Expand `stopword.txt` to fine-tune the noise reduction for your specific domain.

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
`
