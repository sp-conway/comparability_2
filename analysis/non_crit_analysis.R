rm(list=ls())
library(tidyverse)
library(here)
library(fs)

d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  mutate(config=case_when(
    config_1==1~"all-aligned",
    config_1==2.1|config_1==2.2~"two-aligned",
    config_1==3~"none-aligned",
    config_1==4~"triangle"),
    effect=str_replace_all(effect,"_","-"))

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

# non-critical trials ============================================================
# two types of fillers - filler square and filler random + catch trials
d_non_crit <- d %>%
  filter(str_detect(effect,"critical",negate=T))

d_non_crit_corr <- d_non_crit %>%
  group_by(participant,effect,config) %>%
  summarise(p_corr=mean(correct)) %>%
  ungroup() 
d_non_crit_corr %>%
  ggplot(aes(p_corr))+
  geom_histogram(fill="lightblue",col="black")+
  facet_grid(effect~.)+
  labs(x="prop correct")+
  ggthemes::theme_few()+
  theme(text=element_text(size=18))
ggsave(filename=here("analysis","plots","non_crit_prop_correct.jpeg"),width=4,height=5)

d_non_crit_corr %>%
  group_by(effect, config) %>%
  summarise(m_corr=mean(p_corr),
            se=sd(p_corr)/sqrt(n()),
            lower=m_corr-se,
            upper=m_corr+se) %>%
  ungroup() %>%
  ggplot(aes(config,m_corr))+
  geom_col(position="dodge",width=.5,fill="lightblue")+
  geom_point(data=d_non_crit_corr,aes(config,p_corr),alpha=.2,pch=".")+
  geom_errorbar(aes(ymin=lower,ymax=upper),width=.1,position = position_dodge(width=.5))+
  labs(x="configuration",y="mean prop correct")+
  scale_y_continuous(limits=c(0,1))+
  facet_grid(effect~.)+
  ggthemes::theme_few()
ggsave(filename=here("analysis","plots","non_crit_mean_prop_correct.jpeg"),width=4,height=5)

# just fillers ======================================================================
d_fill <- d %>%
  filter(str_detect(effect,"filler"))
d_fill %>%
  group_by(participant) %>%
  summarise(m=mean(choice==3)) %>%
  ungroup() %>%
  ggplot(aes(m))+
  geom_histogram(fill="lightblue")+
  ggthemes::theme_few()

d_fill %>%
  group_by(participant,choice) %>%
  summarise(N=n()) %>%
  group_by(participant) %>%
  mutate(prop=N/sum(N)) %>%
  ungroup() %>%
  group_by(choice) %>%
  summarise(mm=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=mm-se,
            upper=mm+se) %>%
  ungroup() %>%
  mutate(choice=case_match(choice,1~"left",2~"middle",3~"right")) %>%
  ggplot(aes(choice,mm))+
  geom_col(position="dodge",width=.5,fill="lightblue")+
  geom_errorbar(aes(ymin=lower,ymax=upper),width=.2,position = position_dodge(width=.5))+
  labs(x="choice",y="mean choice prop")+
  scale_y_continuous(limits=c(0,.4))+
  ggthemes::theme_few()
ggsave(filename=here("analysis","plots","filler_position_bias.jpeg"),width=4,height=4)

# checking to make sure pos randomly assigned right
a1 <- d_fill$w_1*d_fill$h_1
a2 <- d_fill$w_2*d_fill$h_2
a3 <- d_fill$w_3*d_fill$h_3
a <- cbind(a1,a2,a3)
m <- apply(a, 1, which.max)
table(m)/length(m)
