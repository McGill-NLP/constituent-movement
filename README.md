# Language Models Largely Exhibit Human-like Constituent Ordering Preferences

*Ada D. Tur, Gaurav Kamath, Siva Reddy*

:tada:Accepted at NAACL 2025!:tada:

## Details

See the ```data``` and ```code``` folders for information on accessing our public data corpus, as well as code used to generate/collect and process data for experimentation.

## Summary

Though English sentences are typically inflexible vis-à-vis word order, constituents often show far more variability in ordering. One prominent theory presents the notion that constituent ordering is directly correlated with constituent weight: a measure of the constituent length or complexity. Such theories are interesting in the context of natural language processing (NLP), because while recent advances in NLP have led to significant gains in the performance of large language models (LLMs), much remains unclear about how these models process language, and how this compares to human language processing. 

In particular, the question remains whether LLMs display the same patterns with constituent movement, and may provide insights into existing theories on when and  how the shift occurs in human language. 

We compare a variety of LLMs with diverse properties to evaluate broad LLM performance on four types of constituent movement: 

**heavy NP shift**, **particle movement**, **dative alternation**, and **multiple PPs**. 

Despite performing unexpectedly around particle movement, LLMs generally align with human preferences around constituent ordering.

![Figure One](fig1.jpg)

Broadly speaking, a clear trend is maintained across humans and models, following what has been presented in prior linguistic research. Where human language sees motivation for  movement with increasing weight, model behavior follows closely.
Interestingly, we observe an unexpected trend where instruction-tuned models, which
consistently correlate less with human data than their corresponding base model, as well as,
quite often, lower R-squared scores. This runs against our initial hypothesis around
instruction-tuned models, and suggests inadequacy in providing consistent and explainable
trends compared to base models.
