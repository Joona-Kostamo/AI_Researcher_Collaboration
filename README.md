# Source code for "Collaboration Networks of AI Researchers" project for Collaborative Innovation Networks (COINs) Seminar 2022/2023

The goal of this code was to build a data set of AI research papers containing citation infromation between papers, and then investigate the citation relationships between papers. A co-citation network was generated with Gephi (https://gephi.org/) based on this data set to examine these relationships.

A pre-trained SBERT model (https://www.sbert.net/) was fine tuned on this data set to estimate semantic similarity between paper abstracts. The training was performed using cosine similarity loss on a binary classification task predicting existence of citation between papers. The model could then be used as a base for a AI research paper recommendation engine that takes an abstract as an input and returns a list of recommended papers based on semantic similarity of abstracts.

The model output embeddings were further analyzed by clustering the embeddings using hierarchical clustering, and the optimal number of clusters was briefly investigated.

The data set of papers with their citing paper info is in file WoS_With_Citations.xls, which is available here: https://docs.google.com/spreadsheets/d/1eVI1LieuzR3RDYQ2RABkHEZCk2f7rSnG/edit?usp=share_link&ouid=114372124154328258965&rtpof=true&sd=true

## To run the code locally
The code is not intended to be widely distributed, and its quality and structure reflect this. Names for files are hard coded, and it is assumed all needed files are stored in the same folder with the code. This should be customized if your setup does not reflect this. The related files are available from https://drive.google.com/drive/folders/1Tz4PgypaVWHvDB8wGDk39yRBXXYMiLmN?usp=share_link

If you run all the notebooks in order, only WoS_All_Most_cited.xls and Abstract.xls are needed, all other files will be generated at different stages along the process. An API key is needed for SerpAPI to fech the citation info for the papers. This must to be provided in SerpAPIBuildDataset.ipynb.

The order of execution for the files here is as follows:

    1. SerpAPIBuildDataset.ipynb
    
    2. ML_Large_dataset.ipynb
    
    3. CreateEmbeddings.ipynb
    
    4. EmbeddingsClustering.ipynb
    
AbstractSearchService.py contains the search engine service code running on a Virtual Private Server.

UseAbstractSearchAPI.ipynb contains an example code snippet for how the search service can be used programmatically.
