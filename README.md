# deep-learning-workshop

Here are some awesome papers/tutorials on machine/deep learning and related fields, along with some notes and codes if applied.  
You are always welcomed to share your own thoughts here with us !

I roughly categorise the resources into paper and tutorial (perhaps more in the future) and tag the them with either of these two. The original pdf of papers are stored locally only, whereas a scirpt, `sync.py`, was created to download them using `wget`. 

**Usage**:

To run this script, simply do a `python sync.py` which downloads the papers (urls of resources with tag `[paper]` in their titles) to the according directory. 

Please make sure that you have `Python` and `wget` installed and configured properly. 

**PR**:

Everything that is interesting is welcomed! Please follow the same pattern which might make things eaiser:

* The type of the resource is defined in tags together with its title in header 4 (####)
* The notes and codes are stored in separate files in the same folder
* Elements like url, links to the notes and codes are placed in bullet points under its title (header 4)

For example, a typical organisation of resources would be sth as follows.

```markdown
## natural language processing

### text classification

#### [paper] Convolutional Neural Networks for Sentence Classification

* [url](http://aclweb.org/anthology/D/D14/D14-1181.pdf)
* [notes](/natural_language_processing/text_classification/Convolutional_Neural_Networks_for_Sentence_Classification.md)
* codes

#### [tutorial] Home Credit Default Risk 1st Place Solution

* [url](https://www.kaggle.com/c/home-credit-default-risk/discussion/64821)
```

---

## natural language processing

### text classification

#### [paper] Convolutional Neural Networks for Sentence Classification

* [url](http://aclweb.org/anthology/D/D14/D14-1181.pdf)
* [notes](/natural_language_processing/text_classification/Convolutional_Neural_Networks_for_Sentence_Classification.md)
* codes

#### [paper] Document Modeling with Gated Recurrent Neural Network

* [url](https://www.cs.cmu.edu/~ark/EMNLP-2015/proceedings/EMNLP/pdf/EMNLP167.pdf)
* notes
* codes

#### [paper] Hierarchical Attention Networks for Document Classification

* [url](http://aclweb.org/anthology/N/N16/N16-1174.pdf)
* notes
* codes

## computer vision
