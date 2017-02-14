# Python_Semantic_Relatedness
Semantic relatedness measures how related two concepts are, using any kind of relation.
To find the semantic relatedness between two words obtained from tweets, the proposed method is as follows:

create a graph where nodes are words from tweets, edges are the conditional probability from one node to another based on the cooccurrence frequency and occurrence frequency.
apply Random Walk from a target node(word) to create static distribution for it which represent the features of the target word.
apply cosine similarity method on two static distributions for two words respectively to get the final semantic relatedness score.
