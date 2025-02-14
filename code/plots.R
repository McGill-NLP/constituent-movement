library(tidyverse)
library(glue)

HNPS <- read_csv("final_data/processed_data/hnps_synth.csv")
PM <- read_csv("final_data/processed_data/pm_synth.csv")
DA <- read_csv("final_data/processed_data/da_synth.csv")
MPP <- read_csv("final_data/processed_data/mpp_synth.csv")
HNPS <- HNPS %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
PM <- PM %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
MPP <- MPP %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)
DA <- DA %>% mutate(verb = as.factor(verb)) %>% filter(syll_ratio > 0)


HNPS_mined <- read_csv("final_data/processed_data/hnps_mined.csv") 
PM_mined <- read_csv("final_data/processed_data/pm_mined.csv")
DA_mined <- read_csv("final_data/processed_data/da_mined.csv")
MPP_mined <- read_csv("final_data/processed_data/mpp_mined.csv")
HNPS_mined <- HNPS_mined %>% filter(syll_ratio > 0)
PM_mined <- PM_mined %>% filter(syll_ratio > 0)
MPP_mined <- MPP_mined %>% filter(syll_ratio > 0)
DA_mined <- DA_mined %>% filter(syll_ratio > 0)


### Make some plots...

synth_data_all_models <- function(df, data_name, 
                                  x_label = "Ratio", 
                                  y_label = "Mean Score", 
                                  legend_title = "Ratio Type",
                                  legend_labels = c("wordlength_ratio" = "Word Length Ratio", 
                                                    "syll_ratio" = "Syllable Weight Ratio", 
                                                    "mods_ratio" = "Modifier Weight Ratio",
                                                    "token_ratio" = "Token Length Ratio")) {
  df %>% 
    pivot_longer(
      cols = c("gpt2_score", "gpt2_med_score", "gpt2_large_score", "gpt2_xl_score", 
               "llama_3_score", "llama_3_chat_score", "babyopt_score", "babyllama_score", 
               "mistral_0.3_score", "mistral_0.3_chat_score", "olmo_score", "olmo_chat_score"), 
      names_to = "source", 
      values_to = "score"
    ) %>%
    mutate(
      token_ratio = case_when(
        source == "gpt2_score" ~ gpt2_token_ratio,
        source == "gpt2_med_score" ~ gpt2_med_token_ratio,
        source == "gpt2_large_score" ~ gpt2_large_token_ratio,
        source == "gpt2_xl_score" ~ gpt2_xl_token_ratio,
        source == "llama_3_score" ~ llama_3_token_ratio,
        source == "llama_3_chat_score" ~ llama_3_chat_token_ratio,
        source == "babyopt_score" ~ babyopt_token_ratio,
        source == "babyllama_score" ~ babyllama_token_ratio,
        source == "mistral_0.3_score" ~ mistral_0.3_token_ratio,
        source == "mistral_0.3_chat_score" ~ mistral_0.3_chat_token_ratio,
        source == "olmo_score" ~ olmo_token_ratio,
        source == "olmo_chat_score" ~ olmo_chat_token_ratio,
        TRUE ~ NA_real_
      )
    ) %>%
    pivot_longer(
      cols = c("wordlength_ratio", "syll_ratio", "mods_ratio", "token_ratio"), 
      names_to = "ratio_type", 
      values_to = "ratio"
    ) %>%
    dplyr::select(score, source, ratio, ratio_type) %>%
    group_by(ratio_type, ratio, source) %>%
    summarise(mean_score = mean(score), .groups = "drop") %>%
    ggplot(aes(x = ratio, y = mean_score, color = ratio_type)) +
    geom_line() +
    facet_wrap(~source) +
    scale_color_manual(
      name = legend_title,
      values = c(
        "wordlength_ratio" = "black", 
        "syll_ratio" = "#0072B2", 
        "mods_ratio" = "#D55E00",
        "token_ratio" = "orange"
      ),
      labels = legend_labels
    ) +
    ggtitle(data_name) +
    xlab(x_label) +
    ylab(y_label)
}


mined_data_all_models <- function(df, data_name, 
                                  x_label = "Ratio", 
                                  y_label = "Mean Score", 
                                  legend_title = "Ratio Type",
                                  legend_labels = c("wordlength_ratio" = "Word Length Ratio", 
                                                    "syll_ratio" = "Syllable Weight Ratio", 
                                                    "token_ratio" = "Token Length Ratio")) {
  df %>% 
    pivot_longer(
      cols = c("gpt2_score", "gpt2_med_score", "gpt2_large_score", "gpt2_xl_score", 
               "llama_3_score", "llama_3_chat_score", "babyopt_score", "babyllama_score", 
               "mistral_0.3_score", "mistral_0.3_chat_score", "olmo_score", "olmo_chat_score"), 
      names_to = "source", 
      values_to = "score"
    ) %>%
    mutate(
      token_ratio = case_when(
        source == "gpt2_score" ~ gpt2_token_ratio,
        source == "gpt2_med_score" ~ gpt2_med_token_ratio,
        source == "gpt2_large_score" ~ gpt2_large_token_ratio,
        source == "gpt2_xl_score" ~ gpt2_xl_token_ratio,
        source == "llama_3_score" ~ llama_3_token_ratio,
        source == "llama_3_chat_score" ~ llama_3_chat_token_ratio,
        source == "babyopt_score" ~ babyopt_token_ratio,
        source == "babyllama_score" ~ babyllama_token_ratio,
        source == "mistral_0.3_score" ~ mistral_0.3_token_ratio,
        source == "mistral_0.3_chat_score" ~ mistral_0.3_chat_token_ratio,
        source == "olmo_score" ~ olmo_token_ratio,
        source == "olmo_chat_score" ~ olmo_chat_token_ratio,
        TRUE ~ NA_real_
      )
    ) %>%
    pivot_longer(
      cols = c("wordlength_ratio", "syll_ratio", "token_ratio"), 
      names_to = "ratio_type", 
      values_to = "ratio"
    ) %>%
    dplyr::select(score, source, ratio, ratio_type) %>%
    group_by(ratio_type, ratio, source) %>%
    summarise(mean_score = mean(score), .groups = "drop") %>%
    ggplot(aes(x = ratio, y = mean_score, color = ratio_type)) +
    geom_line() +
    facet_wrap(~source) +
    scale_color_manual(
      name = legend_title,
      values = c(
        "wordlength_ratio" = "black", 
        "syll_ratio" = "#0072B2", 
        "token_ratio" = "orange"
      ),
      labels = legend_labels
    ) +
    ggtitle(data_name) +
    xlab(x_label) +
    ylab(y_label)
}


synth_data_one_model <- function(df, model_name, data_name,
                                  x_label = "Ratio", 
                                  y_label = "Mean Score", 
                                  legend_title = "Ratio Type",
                                  legend_labels = c("wordlength_ratio" = "Word Length Ratio", 
                                                    "syll_ratio" = "Syllable Weight Ratio", 
                                                    "mods_ratio" = "Modifier Weight Ratio",
                                                    "token_ratio" = "Token Length Ratio")) {
  df %>% 
    pivot_longer(
      cols = c("gpt2_score", "gpt2_med_score", "gpt2_large_score", "gpt2_xl_score", 
               "llama_3_score", "llama_3_chat_score", "babyopt_score", "babyllama_score", 
               "mistral_0.3_score", "mistral_0.3_chat_score", "olmo_score", "olmo_chat_score"), 
      names_to = "source", 
      values_to = "score"
    ) %>%
    mutate(
      token_ratio = case_when(
        source == "gpt2_score" ~ gpt2_token_ratio,
        source == "gpt2_med_score" ~ gpt2_med_token_ratio,
        source == "gpt2_large_score" ~ gpt2_large_token_ratio,
        source == "gpt2_xl_score" ~ gpt2_xl_token_ratio,
        source == "llama_3_score" ~ llama_3_token_ratio,
        source == "llama_3_chat_score" ~ llama_3_chat_token_ratio,
        source == "babyopt_score" ~ babyopt_token_ratio,
        source == "babyllama_score" ~ babyllama_token_ratio,
        source == "mistral_0.3_score" ~ mistral_0.3_token_ratio,
        source == "mistral_0.3_chat_score" ~ mistral_0.3_chat_token_ratio,
        source == "olmo_score" ~ olmo_token_ratio,
        source == "olmo_chat_score" ~ olmo_chat_token_ratio,
        TRUE ~ NA_real_
      )
    ) %>%
    pivot_longer(
      cols = c("wordlength_ratio", "syll_ratio", "mods_ratio", "token_ratio"), 
      names_to = "ratio_type", 
      values_to = "ratio"
    ) %>%
    dplyr::select(score, source, ratio, ratio_type) %>%
    group_by(ratio_type, ratio, source) %>%
    summarise(mean_score = mean(score), .groups = "drop") %>%
    filter(source==glue("{model_name}_score")) %>% 
    ggplot(aes(x = ratio, y = mean_score, color = ratio_type)) +
    geom_line() +
    facet_wrap(~source) +
    scale_color_manual(
      name = legend_title,
      values = c(
        "wordlength_ratio" = "black", 
        "syll_ratio" = "#0072B2", 
        "mods_ratio" = "#D55E00",
        "token_ratio" = "orange"
      ),
      labels = legend_labels
    ) +
    ggtitle(data_name) +
    xlab(x_label) +
    ylab(y_label)
}



########## Look across models: ##########
# HNPS Synthetic Data
synth_data_all_models(HNPS, "Model Preference Scores on Heavy NP Shift")
# HNPS Mined Data
mined_data_all_models(HNPS_mined, "Model Preference Scores on Heavy NP Shift")

# PM Synthetic Data
synth_data_all_models(PM, "Model Preference Scores on Particle Movement")
# PM Mined Data
mined_data_all_models(PM_mined, "Model Preference Scores on Particle Movement")

# MPP Synthetic Data
synth_data_all_models(MPP, "Model Preference Scores on Multiple PPs")
# MPP Mined Data
mined_data_all_models(MPP_mined, "Model Preference Scores on Multiple PPs")

# DA Synthetic Data
synth_data_all_models(DA, "Model Preference Scores on Multiple PPs")
# DA Mined Data
mined_data_all_models(DA_mined, "Model Preference Scores on Multiple PPs")


########## Look at a single model: ##########

synth_data_one_model(HNPS, "olmo", "OLMo Preference Scores on Heavy NP Shift")



########## Human correlations: ##########

var <- "hnps"
human_data <- read_csv(glue("final_data/processed_data/{var}_human.csv"))
human_data$numerized = lapply(strsplit(gsub('\\[|\\]', '', human_data$raw_responses), ","), as.numeric)
human_data <- human_data %>%
  mutate(
    verb = as.factor(verb),
    human_response_sd = sapply(numerized, sd, na.rm = TRUE)  # Compute per-row SD
  ) %>%
  filter(syll_ratio > 0, human_response_sd<=1.5)


human_data %>%
  ggplot(aes(x = mean_human_response, y = llama_3_score)) +
  geom_point() +
  geom_smooth(method = "lm", color = "blue", se = TRUE) + # Regression line
  labs(x = "Custom X Label", y = "Custom Y Label", title = "Scatter Plot with Regression Line") 


