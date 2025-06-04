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
    choice_name=factor(choice_name,levels=c("h","w","d"))) %>%
  mutate(order2=case_when(
    order %in% c("dwh","wdh")~"wd",
    order %in% c("dhw","hdw")~"hd",
    order %in% c("whd","hwd")~"wh",
  ))
props <- d %>%
  group_by(participant,config,order2,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,config,order2) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup() %>%
  select(-n)
prop_diffs <- props %>%
  pivot_wider(names_from = config, values_from = prop, values_fill = 0) %>%
  mutate(`none - all`=none-all,
         `two - all`=two-all,
         `two - none`=two-none) %>%
  select(-c(none,all,two,triangle)) %>%
  pivot_longer(contains("-"),
               names_to = "comparison",
               values_to = "diff")
prop_m_diffs <- prop_diffs %>%
  group_by(order2,choice_name,comparison) %>%
  summarise(m=mean(diff),
            se=sd(diff)/sqrt(n()),
            l=m-se,
            u=m+se) %>%
  ungroup()
prop_m_diffs %>%
  ggplot(aes(order2,m,fill=choice_name))+
  geom_col(position="dodge",width=1/3)+
  geom_errorbar(aes(ymin=l,ymax=u),position=position_dodge(width=1/3),width=.01)+
  geom_hline(yintercept=0,linetype="dashed",alpha=.6)+
  facet_grid(comparison~.)+
  ggsci::scale_fill_startrek(name="choice")+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","tmp1.jpeg"),width=8,height=8)
props %>%
  group_by(config,order2,choice_name) %>%
  summarise(m=mean(prop),
            se=sd(prop)/sqrt(n()),
            l=m-se,
            u=m+se) %>%
  ungroup() %>%
  ggplot(aes(order2,m,fill=choice_name))+
  geom_col(position="dodge",width=1/3)+
  geom_errorbar(aes(ymin=l,ymax=u),position=position_dodge(width=1/3),width=.01)+
  geom_hline(yintercept=0,linetype="dashed",alpha=.6)+
  facet_grid(config~.)+
  ggsci::scale_fill_startrek(name="choice")+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","tmp2.jpeg"),width=8,height=8)

prop_diffs <- props %>%
  pivot_wider(names_from = config, values_from = prop, values_fill = 0) %>%
  mutate(choice_align=case_when(
    (choice_name=="h" & order2=="hd") | (choice_name=="w" & order2=="wd") ~ "aligned",
    (choice_name=="h" & order2=="wd") | (choice_name=="w" & order2=="hd") ~ "non-aligned",
  )) %>%
  filter(!is.na(choice_align)) %>%
  mutate(`none - all`=none-all,
         `two - all`=two-all,
         `two - none`=two-none) %>%
  select(-c(none,all,two,triangle)) %>%
  pivot_longer(contains("-"),
               names_to = "comparison",
               values_to = "diff")
prop_m_diffs <- prop_diffs %>%
  group_by(choice_align,comparison) %>%
  summarise(m=mean(diff),
            se=sd(diff)/sqrt(n()),
            l=m-se,
            u=m+se) %>%
  ungroup()
prop_m_diffs %>%
  filter(!is.na(choice_align)) %>%
  ggplot(aes(choice_align,m))+
  geom_col(position="dodge",width=1/3)+
  geom_errorbar(aes(ymin=l,ymax=u),position=position_dodge(width=1/3),width=.01)+
  geom_hline(yintercept=0,linetype="dashed",alpha=.6)+
  facet_grid(comparison~.)+
  ggsci::scale_fill_startrek(name="choice")+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","tmp3.jpeg"),width=8,height=8)
