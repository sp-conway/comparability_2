rm(list=ls())
library(tidyverse)
library(here)
library(fs)
library(glue)
library(latex2exp)
library(BayesFactor)

d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  filter(str_detect(effect,"critical")) %>%
  mutate(config=case_when(
    config_1==1~"all",
    config_1==2.1~"two",
    config_1==3~"none",
    config_1==4~"triangle"),
    across(c(config,choice_name),as.factor),
    order=factor(order,
                 levels=c("dhw","hdw",
                          "dwh","wdh",
                          "hwd","whd")),
    choice_name=factor(choice_name,levels=c("h","w","d"))) %>%
  mutate(aligned=str_sub(order,1,2)) %>%
  mutate(aligned2=case_when(
    aligned %in% c("wh","hw") ~ "wh",
    aligned %in% c("wd","dw") ~ "wd",
    aligned %in% c("dh","hd") ~ "hd",
  )) %>%
  mutate(choice_align=case_when(
    choice_name=="h" & aligned2=="hd"~"aligned",
    choice_name=="w" & aligned2=="hd"~"non-aligned",
    choice_name=="h" & aligned2=="wd"~"non-aligned",
    choice_name=="w" & aligned2=="wd"~"aligned",
    choice_name %in% c("h","w") & aligned2=="wh"~"aligned",
    choice_name=="d"~"decoy"
  )) %>%
  select(-c(config_1,config_2))

m_diff <- d %>%
  filter(config!="triangle" & aligned2!="wh") %>%
  group_by(participant,config,aligned2,choice_name) %>%
  summarise(N=n()) %>%
  group_by(participant,config,aligned2) %>%
  mutate(prop=N/sum(N)) %>%
  ungroup() %>%
  select(-N) %>%
  pivot_wider(names_from = c(config), values_from = prop, values_fill = 0,names_sep="_") %>%
  filter((aligned2=="hd" & choice_name=="h") | (aligned2=="wd" & choice_name=="w") ) %>%
  mutate(`p(x | two aligned)-p(x | none)`=two-none,
         `p(x | two aligned)-p(x | all)`=two-all,
         `p(x | none)-p(x | all)`=none-all) %>%
  select(-c(all,two,none)) %>%
  pivot_longer(-c(participant,aligned2,choice_name),names_to = "comparison", values_to = "diff") %>%
  group_by(aligned2, comparison) %>%
  summarise(m=mean(diff),
            ci=qt(.975,n()-1)*(sd(diff)/sqrt(n())),
            l=m-ci,
            u=m+ci) %>%
  ungroup() 

m_diff %>% 
  mutate(option=str_remove(aligned2,"d")) %>%
  ggplot(aes(comparison,m,fill=option))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=l,ymax=u),position=position_dodge(width=.5),width=.015)+
  geom_hline(yintercept=0,alpha=.8)+
  labs(y="mean")+
  ggthemes::theme_few()+
  theme(text=element_text(size=13))
ggsave(filename=here("analysis","plots","tmp.jpeg"),width=8,height=6)
