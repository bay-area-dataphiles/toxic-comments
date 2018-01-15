# History

## January 14: Week 1 Review

Baris and Matthew met over Google Hangouts to review progress the team has made over the past week since our initial meeting on January 7. Most of the time was spent going over Steven and Matthew's Jupyter notebooks from the past week.

**Key Results:**
* We have 96,000 records in the training set and 227,000 in the test set, consisting of raw Wikipedia comments and ratings by human workers for each comment's toxicity. Toxicity comes in the following six categories: `toxic`, `severe_toxic`, `identity_hate`, `threat`, `obscene`, and `insult`.
* The most common words in comments generally are 'article', 'page', and 'wikipedia'.
* About 10% of comments are toxic in any form, mostly `toxic`, `obscene`, and `insult`. These three classes are most common and tend to occur together.
* The most common words for `toxic`, `severe_toxic`, `obscene`, and `insult` are all fairly similar, including 'fuck' 'suck', 'nigger', 'ass', and 'shit'. The top words for `threat` and `identity_hate` are more distinct.
* The data badly needs to be cleaned. In addition to excessive punctuation, misspellings, and escape sequences, we also have some comments with automatically generated messages and information (e.g., a notice that the message was edited or removed), and outliers, such as comments that are extremely long and spammy.
* Two baseline models have been fit, both separately-fitted logistic regressions. With counts, this achieves a logloss on submission to Kaggle of 0.084, and with Tfidf vectors, 0.057. This is a good baseline to improve on.

**Key Issues for Week 2:**
* Data quality/preprocessing: misspellings, outliers, auto-messages
	* How should we account for outliers in the form of long, spammy toxic comments? We could: remove, truncate, or leave as-is.
	* We should aim to clean off all escape sequences, auto-generated messages, and other corruptions after extracting them as separate features from the text, as a preprocessing step.
* Feature engineering: punctuation, capitalization, length, censorship, escape sequences
* Dimensionality and topic/genre analysis
* Correlates of toxicity
