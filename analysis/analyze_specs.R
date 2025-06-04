rm(list=ls())
library(tidyverse)
library(here)
d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  filter(participant==60)
crit <- d %>%
  filter(effect=="critical")

crit %>%
  mutate(config=case_when(
    config_1==1~"all",
    config_1==2.1~"two",
    config_1==3~"none",
    config_1==4~"triangle")) %>%
  group_by(diag, distance, effect, config, order,block) %>%
  summarise(N=n()) %>%
  ungroup() %>%
  arrange(desc(N))

non_crit <- d %>%
  filter(effect!="critical")
non_crit %>%
  count(effect)
