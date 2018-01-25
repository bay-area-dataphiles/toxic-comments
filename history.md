
# History

## January 21: Week 2 Review

No meeting this week because we all have lives and there is plenty of time until the competition deadlines.

**Key Results:**
* Toxic comments tend to be shorter than non-toxic comments, on average. However, there is a significant subset of toxic comments that are extremely long.
* `toxic`, `severe_toxic`, and `identity_hate` tend to be the longer toxicities.
* There seem to be 3 main types of comments, based on length:

|Length|Topic|Top Words| % of Training Set |
|--|--|--|--|
| < 250 chars| Talk | talk |
| 250-3000 chars | Article/Wikipedia Policy (?)| article, wikipedia |
| > 3000 chars| Toxicity | fuck |
![](https://files.slack.com/files-pri/T87KDTP3Q-F8UNWE7NZ/image.png)
* Toxic comments tend to have lower polarity (?) and sentiment than non-toxic ones.
* We have now fit 3 models:

|Modeling Strategy							|	Public Leaderboard Score	|
|-----|-----|
|CountVectorizer -> LogisticRegression		|	.084						|
TfidfVectorizer -> LogisticRegression 		|	.057						|
Stemming -> TfidfVectorizer -> LogisticRegression |.055 					|

## January 14: Week 1 Review

Baris and Matthew met over Google Hangouts to review progress the team has made over the past week since our initial meeting on January 7. Most of the time was spent going over Steven and Matthew's Jupyter notebooks from the past week.

**Key Results:**
* We have 96,000 records in the training set and 227,000 in the test set, consisting of raw Wikipedia comments and ratings by human workers for each comment's toxicity. Toxicity comes in the following six categories: `toxic`, `severe_toxic`, `identity_hate`, `threat`, `obscene`, and `insult`.
* The most common words in comments generally are 'article', 'page', and 'wikipedia'.
* About 10% of comments are toxic in any form, mostly `toxic`, `obscene`, and `insult`. These three classes are most common and tend to occur together.
* The most common words for `toxic`, `severe_toxic`, `obscene`, and `insult` are all fairly similar, including 'fuck' 'suck', 'nigger', 'ass', and 'shit'. The top words for `threat` and `identity_hate` are more distinct.
* The data badly needs to be cleaned. In addition to excessive punctuation, misspellings, and escape sequences, we also have some comments with automatically generated messages and information (e.g., a notice that the message was edited or removed), and outliers, such as comments that are extremely long and spammy.
* Two baseline models have been fit, both separately-fitted logistic regressions. With counts, this achieves a logloss on submission to Kaggle of 0.084, and with Tfidf vectors, 0.057. This is a good baseline on which to improve.
