library(tidyverse)
library(mgcv)
library(glue)
library(itsadug)
library(ggeffects)

HNPS <- read_csv("final_data/processed_data/hnps_synth.csv")
PM <- read_csv("final_data/processed_data/pm_synth.csv")
DA <- read_csv("final_data/processed_data/da_synth.csv")
MPP <- read_csv("final_data/processed_data/mpp_synth.csv")
HNPS <- HNPS %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
PM <- PM %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
MPP <- MPP %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
DA <- DA %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)

model_columns <- c("gpt2", "gpt2_med", "gpt2_large","gpt2_xl",
                   "llama_3", "llama_3_chat",
                   "babyopt", "babyllama",
                   "mistral_0.3", "mistral_0.3_chat",
                   "olmo", "olmo_chat")

df_list <- list(MPP = MPP, HNPS = HNPS, DA = DA, PM = PM)

# Initialize an empty data frame to store the results
results_df <- data.frame(
  model = character(),
  dataset = character(),
  full_r_sq = numeric(),
  token_ab_r_sq = numeric(),
  token_ab_p_better_fit = numeric(),
  word_ab_r_sq = numeric(),
  word_ab_p_better_fit = numeric(),
  syll_ab_r_sq = numeric(),
  syll_ab_p_better_fit = numeric(),
  mods_ab_r_sq = numeric(),
  mods_ab_p_better_fit = numeric(),
  stringsAsFactors = FALSE
)

for (name in names(df_list)){
  print(glue("--------------{name}-------------\n"))
  # Loop through each model name:
  for (model_col in model_columns) {
    print(glue("{model_col}:"))
    
    # Dynamically construct the formulas for the full and ablated models...
    formula_str_full <- glue("{model_col}_score ~ s({model_col}_token_ratio) + s(verb, {model_col}_token_ratio, bs='re') + ",
                             "s(syll_ratio) + s(verb, syll_ratio, bs='re') + ",
                             "s(wordlength_ratio) + s(verb, wordlength_ratio, bs='re') + ",
                             "s(mods_ratio, k=6) + s(verb, mods_ratio, bs='re') + ",
                             "s(verb, bs='re')")
    
    formula_str_no_token <- glue("{model_col}_score ~ ",
                                 "s(syll_ratio) + s(verb, syll_ratio, bs='re') + ",
                                 "s(wordlength_ratio) + s(verb, wordlength_ratio, bs='re') + ",
                                 "s(mods_ratio, k=6) + s(verb, mods_ratio, bs='re') + ",
                                 "s(verb, bs='re')")
    
    formula_str_no_word <- glue("{model_col}_score ~ s({model_col}_token_ratio) + s(verb, {model_col}_token_ratio, bs='re') + ",
                                "s(syll_ratio) + s(verb, syll_ratio, bs='re') + ",
                                "s(mods_ratio, k=6) + s(verb, mods_ratio, bs='re') + ",
                                "s(verb, bs='re')")
    
    formula_str_no_syll <- glue("{model_col}_score ~ s({model_col}_token_ratio) + s(verb, {model_col}_token_ratio, bs='re') + ",
                                "s(wordlength_ratio) + s(verb, wordlength_ratio, bs='re') + ",
                                "s(mods_ratio, k=6) + s(verb, mods_ratio, bs='re') + ",
                                "s(verb, bs='re')")
    
    formula_str_no_mods <- glue("{model_col}_score ~ s({model_col}_token_ratio) + s(verb, {model_col}_token_ratio, bs='re') + ",
                                "s(syll_ratio) + s(verb, syll_ratio, bs='re') + ",
                                "s(wordlength_ratio) + s(verb, wordlength_ratio, bs='re') + ",
                                "s(verb, bs='re')")
    
    # Convert the formula string to a formula object
    formula_full <- as.formula(formula_str_full)
    formula_no_token <- as.formula(formula_str_no_token)
    formula_no_word <- as.formula(formula_str_no_word)
    formula_no_syll <- as.formula(formula_str_no_syll)
    formula_no_mods <- as.formula(formula_str_no_mods)
    
    # Fit the bam model
    m_full <- bam(formula_full, data = df_list[[name]], method = "ML")
    m_no_token <- bam(formula_no_token, data = df_list[[name]], method = "ML")
    m_no_word <- bam(formula_no_word, data = df_list[[name]], method = "ML")
    m_no_syll <- bam(formula_no_syll, data = df_list[[name]], method = "ML")
    m_no_mods <- bam(formula_no_mods, data = df_list[[name]], method = "ML")
    
    # Get model summaries
    m_full_summary <- summary(m_full)
    m_no_token_summary <- summary(m_no_token)
    m_no_token_p_better_fit <- compareML(m_full, m_no_token, print.output=F)$table$p.value[2]
    m_no_word_summary <- summary(m_no_word)
    m_no_word_p_better_fit <- compareML(m_full, m_no_word, print.output=F)$table$p.value[2]
    m_no_syll_summary <- summary(m_no_syll)
    m_no_syll_p_better_fit <- compareML(m_full, m_no_syll, print.output=F)$table$p.value[2]
    m_no_mods_summary <- summary(m_no_mods)
    m_no_mods_p_better_fit <- compareML(m_full, m_no_mods, print.output=F)$table$p.value[2]
    
    # Append the results to the data frame
    results_df <- rbind(results_df, data.frame(
      model = model_col,
      dataset = name,
      full_r_sq = m_full_summary$r.sq,
      token_ab_r_sq = m_no_token_summary$r.sq,
      token_ab_p_better_fit = m_no_token_p_better_fit,
      word_ab_r_sq = m_no_word_summary$r.sq,
      word_ab_p_better_fit = m_no_word_p_better_fit,
      syll_ab_r_sq = m_no_syll_summary$r.sq,
      syll_ab_p_better_fit = m_no_syll_p_better_fit,
      mods_ab_r_sq = m_no_mods_summary$r.sq,
      mods_ab_p_better_fit = m_no_mods_p_better_fit,
      stringsAsFactors = FALSE
    ))
    
    print(glue("Full model R-Sq.: {m_full_summary$r.sq}"))
    print(glue("Token Length Ablated: {m_no_token_summary$r.sq} || p_better_fit: {m_no_token_p_better_fit}"))
    print(glue("Word Length Ablated: {m_no_word_summary$r.sq} || p_better_fit: {m_no_word_p_better_fit}"))
    print(glue("Syll Length Ablated: {m_no_syll_summary$r.sq} || p_better_fit: {m_no_syll_p_better_fit}"))
    print(glue("Modifiers Length Ablated: {m_no_mods_summary$r.sq} || p_better_fit: {m_no_mods_p_better_fit}"))
    print("\n")
  }
}

# View or save the resulting data frame
print(results_df)
results_df %>% write_csv("modelling_ablation_results_NEW.csv")

results_df <- read_csv("modelling_ablation_results_NEW.csv")



# Human correlations:

# Initialize an empty data frame
cor_results <- data.frame(
  dataset = character(),
  model = character(),
  spearman_cor = numeric(),
  stringsAsFactors = FALSE
)

for (var in c("hnps", "mpp", "da", "pm")) {
  human_data <- read_csv(glue("final_data/processed_data/{var}_human.csv"))
  human_data$numerized = lapply(strsplit(gsub('\\[|\\]', '', human_data$raw_responses), ","), as.numeric)
  human_data <- human_data %>%
    mutate(
      verb = as.factor(verb),
      human_response_sd = sapply(numerized, sd, na.rm = TRUE)  # Compute per-row SD
    ) %>%
    filter(syll_ratio > 0, human_response_sd<=1.5)
  
  for (model in model_columns) {
    cor_value <- cor(human_data$mean_human_response, human_data[[glue("{model}_score")]], method = "spearman")
    
    # Append the result as a new row
    cor_results <- rbind(cor_results, data.frame(
      dataset = var,
      model = model,
      spearman_cor = cor_value,
      stringsAsFactors = FALSE
    ))
  }
}

print(cor_results)
write_csv(cor_results, "correlation_results.csv")


