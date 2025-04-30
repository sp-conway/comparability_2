rm(list=ls())
library(tidyverse)
library(here)
library(fs)

d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  mutate(config=case_when(
    config_1==1~"all aligned",
    config_1==2.1|config_1==2.2~"two aligned",
    config_1==3~"none aligned",
    config_1==4~"triangle"))

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
d_catch %>%
  group_by(participant) %>%
  summarise(correct=mean(correct)) %>%
  ungroup() %>%
  ggplot(aes(correct))+
  geom_histogram(fill="lightblue",col="black")+
  # scale_x_continuous(limits=c(.8,1.0))+
  labs(x="prop correct")+
  ggthemes::theme_few()+
  theme(text=element_text(size=18))
ggsave(filename=here("analysis","plots","catch_prop_correct.jpeg"),width=4,height=5)

# filler trials ============================================================
# two types of fillers - filler square and filler random
d_fill <- d %>%
  filter(str_detect(effect,"filler"))
d_fill %>%
  group_by(participant,effect) %>%
  summarise(p_corr=mean(correct)) %>%
  ungroup() %>%
  mutate(effect=str_replace(effect,"_"," ")) %>%
  ggplot(aes(p_corr))+
  geom_histogram(fill="lightblue",col="black")+
  facet_grid(effect~.)+
  labs(x="prop correct")+
  ggthemes::theme_few()+
  theme(text=element_text(size=18))
ggsave(filename=here("analysis","plots","fill_prop_correct.jpeg"),width=4,height=5)

d_fill %>%
  group_by(participant,effect,config) %>%
  summarise(p_corr=mean(correct)) %>%
  ungroup() %>%
  group_by(effect, config) %>%
  summarise(m_corr=mean(p_corr),
            se=sd(p_corr)/sqrt(n()),
            lower=m_corr-se,
            upper=m_corr+se) %>%
  ungroup() %>%
  mutate(effect=str_replace(effect,"_"," ")) %>%
  ggplot(aes(config,m_corr))+
  geom_col(position="dodge",width=.5,fill="lightblue")+
  geom_errorbar(aes(ymin=lower,ymax=upper),width=.2,position = position_dodge(width=.5))+
  labs(x="configuration",y="mean prop correct")+
  scale_y_continuous(limits=c(0,1))+
  facet_grid(effect~.)+
  ggthemes::theme_few()
ggsave(filename=here("analysis","plots","fill_mean_prop_correct.jpeg"),width=4,height=5)

