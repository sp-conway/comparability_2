rm(list=ls())
library(tidyverse)
library(here)
library(fs)

d <- here("data","clean","data.csv") %>%
  read_csv()

# initial critical trial analysis ============================================================
d_crit <- d %>%
  filter(effect=="critical")
d_crit %>%
  mutate(choice_name=as.factor(choice_name),
         distance=as.factor(distance),
         order=as.factor(order)) %>%
  group_by(participant,order,distance,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,order,distance) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup() %>%
  group_by(order,distance,choice_name) %>%
  summarise(m=mean(prop)) %>%
  ungroup() %>%
  ggplot(aes(distance,m,fill=choice_name))+
  geom_col(position="dodge")+
  scale_y_continuous(breaks = seq(0,.6,.1))+
  facet_wrap(vars(order))+
  labs(y="mean choice prop")+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","tmp.jpeg"))
