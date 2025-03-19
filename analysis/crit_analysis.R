rm(list=ls())
library(tidyverse)
library(here)
library(fs)

d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  filter(str_detect(effect,"critical")) %>%
  mutate(config=case_when(
    config_1==1~"all aligned",
    config_1==2.1~"1 & 2 aligned",
    config_1==2.2~"2 & 3 aligned",
    config_1==3~"none aligned",
    config_1==4~"triangle"),
    across(c(config,choice_name),as.factor),
         order=factor(order,
                            levels=c("dhw","hdw",
                                     "dwh","wdh",
                                     "hwd","whd")))

# prop correct ========================================================================
prop_corr <- d %>%
  group_by(participant,config) %>%
  summarise(pcorr=mean(correct)) %>%
  ungroup()

prop_corr %>%
  ggplot(aes(pcorr))+
  geom_histogram(fill="lightblue",col="black")+
  facet_grid(config~.)+  
  labs(x="prop correct")+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","crit_prop_corr_hist.jpeg"),
       width=6,height=6)

prop_corr %>%
  group_by(config) %>%
  summarise(m=mean(pcorr),
            se=sd(pcorr)/sqrt(n()),
            lower=m-se,
            upper=m+se) %>%
  ungroup() %>%
  ggplot(aes(config,m))+
  geom_col(fill="lightblue")+
  geom_errorbar(aes(ymin=lower,ymax=upper),width=.2)+
  labs(x="prop correct")+
  scale_y_continuous(limits=c(0,1))+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","crit_prop_corr_means.jpeg"),
       width=6,height=6)

# choices ==========================================================================================
mprop <- d %>%
  group_by(participant,config,order,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,config,order) %>%
  mutate(prop=n/sum(n)) %>%
  group_by(config,order,choice_name) %>%
  summarise(mprop=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=mprop-se,
            upper=mprop+se) %>%
  ungroup()
ggsave(filename=here("tmp1.jpeg"))

mprop %>%
  ggplot(aes(order,mprop,fill=choice_name))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.2)+
  facet_grid(config~.)+
  ggthemes::theme_few()

mrsw <- d %>%
  group_by(participant,order,config,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,config,order) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup() %>%
  select(-n) %>%
  pivot_wider(names_from = choice_name,
              values_from = prop,values_fill = 0) %>%
  mutate(rsw=w/(w+h)) %>%
  group_by(order,config) %>%
  summarise(mrsw=mean(rsw),
            se=sd(rsw)/sqrt(n()),
            lower=mrsw-se,
            upper=mrsw+se) %>%
  ungroup()

mrsw %>%
  ggplot(aes(order,mrsw))+
  geom_col(position="dodge",width=.5,fill="lightblue")+
  geom_hline(yintercept=.5,linetype="dashed")+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.2)+
  labs(x="order",y="mean relative share of w")+
  facet_grid(config~.)+
  ggthemes::theme_few()

props <- d %>%
  group_by(participant,config,order,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,config,order) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup()

d %>%
  filter(config_1==2.1) %>%
  mutate(
    order1=case_when(
      order=="hdw"|order=="dhw"~"h aligned with decoy",
      order=="dwh"|order=="wdh"~"w aligned with decoy",
      order=="whd"|order=="hwd"~"w and h aligned",
    )
  ) %>% 
  group_by(participant,order1,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,order1) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup() %>%
  group_by(order1,choice_name) %>%
  summarise(mprop=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=mprop-se,
            upper=mprop+se) %>%
  ungroup() %>%
  ggplot(aes(choice_name, mprop,fill=order1))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.2)+
  ggsci::scale_fill_startrek(name="")+
  scale_y_continuous(limits=c(0,.6))+
  labs(x="choice",
       y="mean proportion")+
  ggthemes::theme_few()
ggsave(filename=here("tmp2.jpeg"))

deltas <- d %>%
  filter(config_1==2.1 & order!="whd" & order!="hwd") %>%
  mutate(
    order1=case_when(
      order %in% c("hdw","dhw") ~"dh_aligned",
      order %in% c("dwh","wdh") ~"dw_aligned"
    )
  ) %>%
  group_by(participant,order1,choice_name) %>%
  summarise(n=n()) %>%
  group_by(participant,order1) %>%
  mutate(prop=n/sum(n)) %>%
  ungroup() %>%
  filter(choice_name!="d") %>%
  select(-n) %>%
  pivot_wider(names_from = order1,
              values_from = prop,
              values_fill = 0) %>%
  mutate(align_diff=case_when(
    choice_name=="h"~dh_aligned-dw_aligned,
    choice_name=="w"~dw_aligned-dh_aligned
  ),
  comp=case_when(
    choice_name=="h"~"p(h | d & h aligned) - \np(h | d & h not aligned)",
    choice_name=="w"~"p(w | d & w aligned) - \np(h | d & w not aligned)",
  )) 

mdeltas <- deltas %>%
  group_by(comp) %>%
  summarise(mprop=mean(align_diff),
            se=sd(align_diff)/sqrt(n()),
            lower=mprop-se,
            upper=mprop+se) %>%
  ungroup()

mdeltas %>%
  ggplot(aes(comp, mprop))+
  geom_point(data=deltas,aes(comp,align_diff),alpha=.3)+
  geom_col(position="dodge",width=.5,fill="lightblue")+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.2)+
  ggsci::scale_fill_startrek(name="")+
  # scale_y_continuous(limits=c(0,.6))+
  labs(x="choice",
       y="mean proportion")+
  ggthemes::theme_few()
   

deltas  %>%
  ggplot(aes(comp, align_diff))+
  geom_boxplot()+
  ggsci::scale_fill_startrek(name="")+
  # scale_y_continuous(limits=c(0,.6))+
  labs(x="choice",
       y="mean proportion")+
  ggthemes::theme_few()


mean(deltas[deltas$choice_name=="h",]$align_diff<0)
mean(deltas[deltas$choice_name=="w",]$align_diff<0 &
     deltas[deltas$choice_name=="h",]$align_diff<0  )
