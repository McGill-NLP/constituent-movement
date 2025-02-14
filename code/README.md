# Code Folder

## Data Creation
We use `data_creation.py` to generate synthetic data, and `shift_miner.py` to mine data from publicly available natural language corpora. To clean the data and prepare for scoring, we use `data_processing.py`. To remove model scores and token weights from data, we use `get_base_data.py`.

## Data Scoring
Originally, we computed *mean* sequence scores for the data using `data_mean_scoring.py`, but made the decision to switch to using *summed* sequence scores instead using `compute_sums.py`. For simplicity, we also provide `data_sum_scoring.py`, to cleanly compute summed sequence scores from scratch.

## Modelling
To compute correlation and ablation results, we use `modelling.R`, and to generate all plots in the paper (and more), we use `plots.R`.
