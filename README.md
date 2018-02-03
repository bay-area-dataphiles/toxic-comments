# [Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)

Paragraphs in quote boxes are from the Kaggle description.

>The [Conversation AI](https://conversationai.github.io/) team, a research initiative founded by Jigsaw and Google (both a part of Alphabet) are working on tools to help improve online conversation. One area of focus is the study of negative online behaviors, like toxic comments (i.e. comments that are rude, disrespectful or otherwise likely to make someone leave a discussion). So far they’ve built a range of publicly available models served through the [Perspective API](https://perspectiveapi.com/), including toxicity. But the current models still make errors, and they don’t allow users to select which types of toxicity they’re interested in finding (e.g. some platforms may be fine with profanity, but not with other types of toxic content).

>In this competition, you’re challenged to build a multi-headed model that’s capable of detecting different types of of toxicity like threats, obscenity, insults, and identity-based hate better than Perspective’s [current models](https://github.com/conversationai/unintended-ml-bias-analysis). You’ll be using a dataset of comments from Wikipedia’s talk page edits. Improvements to the current model will hopefully help online discussion become more productive and respectful.

## Evaluation

>Submissions are evaluated on the mean column-wise log loss. In other words, the score is the average of the log loss of each predicted column. 

Log loss is a way of measuring error when predicting a binary variable that takes into account how certain you are of the prediction. For example, for a given record where the target is 1, a prediction of 0.9 would be scored much more highly than a prediction of 0.7, because the higher score is much more certain of the correct prediction. However, a score of 0.1 would be scored much lower than a score of 0.5 for the same target of 1, because 0.1 is very certain of the *wrong* answer.

## Timeline

>March 13, 2018 - Entry deadline. You must accept the competition rules before this date in order to compete.

>March 13, 2018 - Team Merger deadline. This is the last day participants may join or merge teams.

>March 20, 2018 - Final submission deadline.

>All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary.

## Useful Links

**Natural Language Toolkit**: NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

http://www.nltk.org

**scikit-learn Feature Extraction**: Text Analysis is a major application field for machine learning algorithms. However the raw data, a sequence of symbols cannot be fed directly to the algorithms themselves as most of them expect numerical feature vectors with a fixed size rather than the raw text documents with variable length.

http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

**Tf-idf**: In information retrieval, tf–idf or TFIDF, short for term frequency–inverse document frequency, is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.

https://en.wikipedia.org/wiki/Tf–idf

**Stop words**: In computing, stop words are words which are filtered out before or after processing of natural language data (text).

https://en.wikipedia.org/wiki/Stop_words


