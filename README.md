# twitter covid 19 network analysis 

Download dataset from: https://www.kaggle.com/smid80/coronavirus-covid19-tweets-late-april, extract, and put individual CSV files in /data.

## Data pre-processing

* The original dataset from Kaggle is about 2.03GB
* `prunedata.ipynb` in `/data` takes the individual (original) CSV files from the Kaggle dataset (this is not included in this repository).
* It then filters out the dataset such that we are only looking at tweets that match the following criteria:
    * `lang=en`
    * `followers_count>500`
    * `favourites_count>10`
    * `retweets_count>10`
* It also removes unnecessary columns to reduce dataset file size
* Lastly, it outputs each `pruned-*` versions of the original dataset files
* And finally, all these pruned datasets are combined into `merged-and-pruned-dataset.csv`. *This is our dataset.* From 2.03GB to 38.4 MB :)
