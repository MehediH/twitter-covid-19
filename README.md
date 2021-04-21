# twitter covid 19 network analysis 

* `/data/` includes all the datasets used for different analysis in this report. Please get the original [dataset from here](https://www.kaggle.com/smid80/coronavirus-covid19-tweets-late-april) , extract, and put individual CSV files in `/data/` and run `prunedata.ipynb` to prune the dataset according to the report.
* `/gephis/` includes all the networks used in this report in a `.gefx` format to be used with Gephi.
Download dataset from: https://www.kaggle.com/smid80/coronavirus-covid19-tweets-late-april, extract, and put individual CSV files in /data.
* `/viz/` includes some of the visualizations.
* `generatingDataset.ipynb` uses the pruned dataset to generate networks.
* `networkStatistics.ipynb` includes some basic network statistics. 
* `thematicAnalysis.ipynb` includes all the code for LDA.
* `toxicityAnalysis.ipynb` includes all the code for generating the toxicity dataset, and creating a network with the toxicity data.
