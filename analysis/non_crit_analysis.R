rm(list=ls())
library(tidyverse)
library(here)
library(fs)

d <- here("data","clean","data.csv") %>%
  read_csv()

# catch trials ============================================================
d_catch <- d %>%
  filter(str_detect(effect,"catch"))
d_catch %>%
  group_by(participant) %>%
  summarise(correct=mean(correct)) %>%
  ungroup() %>%
  reframe(mean=mean(correct),
          median=median(correct),
          s=sd(correct),
          max=max(correct),
          min=min(correct))

# filler trials ============================================================
# two types of fillers - filler square and filler random
d_fill <- d %>%
  filter(str_detect(effect,"filler"))
d_fill %>%
  group_by(participant,effect) %>%
  summarise(p_corr=mean(correct)) %>%
  ungroup() %>%
  ggplot(aes(p_corr))+
  geom_histogram(fill="lightblue",col="black")+
  facet_grid(effect~.)+
  labs(x="prop correct")+
  ggthemes::theme_few()+
  theme(text=element_text(size=18))
ggsave(filename=here("analysis","plots","catch_prop_correct.jpeg"),width=4,height=5)