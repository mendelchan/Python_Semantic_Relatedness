# Python_Semantic_Relatedness
Semantic relatedness measures how related two concepts are, using any kind of relation.<br> 
<br> 
To find the semantic relatedness between two distinct words obtained from Twitter: <br> 

1.Create a graph where nodes are words from tweets, edges are the conditional probability from one node to another based on the cooccurrence frequency and occurrence frequency.<br> 
<br> 
2. Apply Random Walk from a target node(word) to create static distribution for it which represent the features of the target word. <br> 
<br> 
3. Apply cosine similarity method on two static distributions for two words respectively to get the final semantic relatedness score.




