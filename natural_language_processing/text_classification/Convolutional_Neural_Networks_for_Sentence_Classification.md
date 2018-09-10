# Convolutional Neutral Networks for Sentence Classification

## TLDR

* Build one layer convolutional network on top of word vectors, which works pretty well on text classification.
* Extract features with *multiple* convolutional filters from word vectors, which are combined later with max-over-time-pooling.
* Different choices of word vectors are experimented as model variances.
* Employ dropout on the penultimate layer with a constraint on l2-norms of the weight vectors for regularisation.

## Approach

### 1. Compose word vecotrs.

The choices for word vectors include static pre-trained word vectors like word2vec by Google, word vectors trained by the Collobert et al. (2011) on Wikipedia and non-static randomly initialised vectors. 
Word vectors could have 1 or 2 channels: 
  * one channel: static pre-trained
  * one channel: trained end-to-end from random initialisation
  * two channel: one static and the other one get trained over data.

The author also proposes an idea to maintain a single channel but employ extra dimensions that are allowed to be modified during training instead of using an additional channel for the non-static portion.

> This idea is somewhat like they way ppl deal with RGB channels in computer vision, which is really amazing!

Another interesting idea here is :

*"When randomly initializing words not in word2vec, slight improvements was obtained by sampling each dimension from U[−a,a] where a was chosen such that the randomly initialized vectors have the same variance as the pre-trained ones. It would be interesting to see if employing more sophisticated methods to mirror the distribution of pre-trained vectors in the initialization pro- cess gives further improvements."*

> This implies that the consistency of among distributions of data might have a great impact! This idea deserves further experiments.


### 2. Apply convolution

One convolutional layer is applied a window of `h` words, generating `h` features.  

Then dropout with a constraint on l2-norms of the weight vectors is adpoted.

> Two methods are used here!
> One is a element-wise multiplication to mask variables with probility of `p`
> Gradients pass only through unmasked variables
> 
> The other is to scale the l2-norm of weights to a certain level whenever it exceeds.

### 3. Apply max-over-time pooling

Apply pooling on `h` features extracted from convolutional layer, which is designed to capture the most important feature -- one with the highest value -- for each feature map.

### 4. Softmax

Output from previous layer was then sent to a fully connected layer with softmax to generate the probability distribution of the labels.
