### **TS-Finder: privacy enhanced web crawler detection model using temporal–spatial access behaviors**



I am Rui Chen, the author of Ts-finder, from Dalian University of Technology, a PhD candidate. My **linkedin** link is: https://www.linkedin.com/in/rui-chen-aa0a932a4/ 

This paper was published in The Journal of Supercomputing, can found in: https://link.springer.com/article/10.1007/s11227-024-06133-6  

**To address the scarcity of crawler detection solutions issues, we are fully opening our crawler detection code to the public !**



From this source code, the detection model was implemented by pyTorch, and we also have implemented this detection model used by scala (Spark Framework). 

We have identified that crawler detection models **are crucial for websites  and other network service providers**, who typically possess sophisticated big data frameworks (like Spark Framework). Therefore, we have rewritten the model in Scala to reduce the cost of utilizing this model for these providers. The code comments are writen by Chinese, and they will be translated into english when I have more time **[Thank you so much]**. 





### Abstract

**Background:** Web crawler detection is critical for preventing unauthorized extraction of  valuable information from websites. 

**Current issues what needed to solved urgently:** Current methods rely on heuristics,  leading to time-consuming processes and inability to detect novel  crawlers. Privacy protection and communication burdens during training  are overlooked, resulting in potential privacy leaks. 

**Our methods:** To address these  issues, we propose a federated deep learning crawler detection model  that analyzes access behaviors while preserving privacy. First,  individual clients locally host website data, while the central server  aggregates information for detection model parameters, eliminating raw  user data transmission or access. We then develop an innovative  algorithm constructing access path trees from user logs, effectively  extracting temporal and spatial behavior features. Additionally, we  propose a novel time series model with fused additive attention,  enabling effective web crawler detection while preserving privacy and  reducing data transmission. 

Finally, comprehensive evaluations on public datasets demonstrate robust privacy protection and effective detection  of emerging crawler types.

![](image/model-img.png)





  
