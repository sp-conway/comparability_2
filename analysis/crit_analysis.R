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
    config_1==1~"all aligned",
    config_1==2.1~"two aligned",
    config_1==3~"none aligned",
    config_1==4~"triangle"),
    across(c(config,choice_name),as.factor),
         order=factor(order,
                            levels=c("dhw","hdw",
                                     "dwh","wdh",
                                     "hwd","whd")),
    choice_name=factor(choice_name,levels=c("h","w","d")))

# functions ============================================================================================================
compute_props <- function(d,...){
  dd <- d %>%
    group_by(participant,...,choice_name) %>%
    summarise(n=n()) %>%
    group_by(participant,...) %>%
    mutate(prop=n/sum(n)) %>%
    ungroup()
  return(dd)
}


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
  geom_point(data=prop_corr,aes(config,pcorr),alpha=.2)+
  geom_errorbar(aes(ymin=lower,ymax=upper),width=.2)+
  labs(x="configuration",y="mean prop. correct")+
  scale_y_continuous(limits=c(0,1))+
  ggthemes::theme_few()+
  theme(text=element_text(size=16))
ggsave(filename=here("analysis","plots","crit_prop_corr_means.jpeg"),
       width=6,height=6)

# choices by config and order (this is too complicated) ==========================================================================================
mprop_by_config_order <- d %>%
  compute_props(config,order) %>%
  group_by(config, order, choice_name) %>%
  summarise(m=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=m-se,
            upper=m+se) %>%
  ungroup()

mprop_by_config_order %>%
  ggplot(aes(config,m,fill=choice_name))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.2)+
  labs(y="mean choice prop.",x="configuration")+
  ggsci::scale_fill_tron(name="choice")+
  facet_grid(order~.)+
  ggthemes::theme_few()
ggsave(filename=here("analysis","plots","mean_choices_all.jpeg"),width=6,height=5)

# choices by configuration, td distance, collapsing across alignment ==============================================================
# mainly want to make sure decoy is chosen enough
d %>%
  compute_props(config, distance) %>%
  group_by(config, distance, choice_name) %>%
  summarise(m=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=m-se,
            upper=m+se) %>%
  ungroup() %>%
  rename(tdd=distance) %>%
  ggplot(aes(config, m, fill=choice_name))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
  scale_y_continuous(limits=c(0,.6),breaks = seq(0,.6,.1))+
  facet_grid(tdd~.,labeller = label_both)+
  ggsci::scale_fill_startrek(name="choice")+
  labs(y="mean choice prop.",x="configuration")+
  ggthemes::theme_few()+
  theme(text=element_text(size=10))
ggsave(filename=here("analysis","plots","crit_mean_choice_by_config_distance.jpeg"),
       width=5,height=4)

# new new analysis ===============================================================
# 2.1 - 1&2 easily compared
# 2.11 
# 
# XX
#   X
# 
# 2.12
#    X
# XX

d_align <- d %>%
  mutate(aligned=str_sub(order,1,2)) %>%
  filter(config!="triangle") %>%
  mutate(aligned2=case_when(
    aligned %in% c("wh","hw") ~ "w aligned with h",
    aligned %in% c("wd","dw") ~ "w aligned with d",
    aligned %in% c("dh","hd") ~ "h aligned with d",
  )) %>%
  filter(aligned2!="w aligned with h") 

d_align %>%
  group_by(participant,config,aligned2,choice_name) %>%
  summarise(N=n()) %>%
  group_by(participant,config,aligned2) %>%
  mutate(prop=N/sum(N)) %>%
  ungroup() %>%
  group_by(config,aligned2,choice_name) %>%
  summarise(m=mean(prop),
            se=sd(prop)/sqrt(n()),
            lower=m-se,
            upper=m+se) %>%
  ungroup() %>%
  ggplot(aes(aligned2,m,fill=choice_name))+
  geom_col(position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
  facet_grid(config~.)+
  ggsci::scale_fill_startrek(name="choice")+
  labs(y="mean choice prop.",x="configuration")+
  # labs(y="mean p(h)-p(w)")+
  ggthemes::theme_few()+
  theme(text=element_text(size=18))
ggsave(filename=here("analysis","plots","crit_mean_hdw_choice_by_config_align.jpeg"),
       width=8,height=6)

d_align_m_choice <- d_align %>%
  mutate(choice_1=case_when(
    aligned2=="w aligned with d" & choice_name=="w"~1,
    aligned2=="h aligned with d" & choice_name=="h"~1,
    T~0
  )) %>%
  filter(choice_name!="d") %>%
  group_by(participant, config) %>%
  summarise(p=mean(choose_target)) %>%
  group_by(config) %>%
  summarise(m=mean(p),
            se=sd(p)/sqrt(n()),
            lower=m-se,
            upper=m+se) %>%
  ungroup()

d_align_m_choice %>%
  ggplot(aes(config,m))+
  geom_col(fill="lightblue",position="dodge",width=.5)+
  geom_errorbar(aes(ymin=lower,ymax=upper),position=position_dodge(width=.5),width=.1)+
  labs(y="mean target choice",x="configuration")+
  ggthemes::theme_few()
ggsave(filename=here("analysis/plots/crit_target_choice_by_config.jpeg"),width=4,height=4)

# OLD ==============================================================================
# 
# d_align_choice <- d_align %>%
#   mutate(choice_align=case_when(
#     choice_name=="h" & aligned2=="h aligned with d"~"aligned option",
#     choice_name=="w" & aligned2=="h aligned with d"~"non-aligned option",
#     choice_name=="h" & aligned2=="w aligned with d"~"non-aligned option",
#     choice_name=="w" & aligned2=="w aligned with d"~"aligned option",
#     choice_name %in% c("h","w") & aligned2=="w aligned with h"~"aligned option",
#     choice_name=="d"~"decoy"
#   )) 
# d_align_choice %>%
#   filter(aligned2!="w aligned with h") %>%
#   group_by(participant, config, choice_align) %>%
#   summarise(N=n()) %>%
#   group_by(participant,config) %>%
#   mutate(prop=N/sum(N)) %>%
#   group_by(config,choice_align) %>%
#   summarise(m=mean(prop),
#           se=sd(prop)/sqrt(n()),
#           lower=m-se,
#           upper=m+se) %>%
#   ungroup() %>%
#   ggplot(aes(config,m,fill=choice_align))+
#   geom_col(position="dodge",width=.5)+
#   geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
#   ggsci::scale_fill_startrek(name="choice")+
#   labs(y="mean choice prop.",x="configuration")+
#   # labs(y="mean p(h)-p(w)")+
#   ggthemes::theme_few()+
#   theme(text=element_text(size=18))
# ggsave(filename=here("analysis","plots","crit_mean_alignment_choice.jpeg"),width=8,height=7)
# 
# d_align_diff <- d_align_choice %>%
#   filter(aligned2!="w aligned with h") %>%
#   group_by(participant, config, choice_align) %>%
#   summarise(N=n()) %>%
#   group_by(participant,config) %>%
#   mutate(prop=N/sum(N)) %>%
#   ungroup() %>%
#   filter(choice_align!="decoy") %>%
#   select(-N) %>%
#   pivot_wider(names_from = choice_align, values_from = prop) %>%
#   mutate(align_diff=`aligned option`-`non-aligned option`)
#   
# d_align_diff %>%
#   group_by(config) %>%
#   summarise(m=mean(align_diff),
#             se=sd(align_diff)/sqrt(n()),
#             lower=m-se,
#             upper=m+se) %>%
#   ungroup() %>%
#   ggplot(aes(config,m))+
#   geom_col(position="dodge",fill="lightblue",width=.5)+
#   geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
#   # labs(y="mean choice prop.",x="alignment")+
#   labs(y="mean p(align)-p(non-aligned)",x="configuration")+
#   ggthemes::theme_few()
# ggsave(filename=here("analysis","plots","mean_align_diff_by_config.jpeg"),width=6,height=5)
# 
# d_align_diff %>%
#   filter(config=="two aligned") %>%
#   ggplot(aes(align_diff))+
#   geom_histogram(fill="lightblue")+
#   labs(x="mean p(align)-p(non-aligned)",title="two aligned trials")+
#   ggthemes::theme_few()+
#   theme(text=element_text(size=18),
#         plot.title = element_text(hjust=0.5))
# ggsave(filename=here("analysis","plots","hist_align_diff_two_aligned.jpeg"),width=7,height=5)
# 
# d_align_diff_two_aligned <- filter(d_align_diff,config=="two aligned")
# t.test(d_align_diff_two_aligned$`aligned option`, d_align_diff_two_aligned$`non-aligned option`,paired=T,mu=0)
# tbf <- ttestBF(d_align_diff_two_aligned$`aligned option`, d_align_diff_two_aligned$`non-aligned option`,paired=T,mu=0)
# post <- posterior(tbf,iterations=50000) %>%
#   as_tibble()
# post_hdi <- HDInterval::hdi(post$mu)
# post_plot <- ggplot(post, aes(mu))+
#   geom_histogram(binwidth = .005,col="white",fill="lightblue")+
#   geom_vline(xintercept = mean(post$mu),linewidth=1)+
#   geom_vline(xintercept = post_hdi[1],linewidth=1,col="red",linetype="dashed")+
#   geom_vline(xintercept = post_hdi[2],linewidth=1,col="red",linetype="dashed")+
#   labs(x="mean p(aligned) - p(not aligned)",y="count",
#        caption=TeX(paste0("$BF_{10}$=",round(exp(tbf@bayesFactor$bf),digits=4))))+
#   ggthemes::theme_few()+
#   theme(plot.title=element_text(hjust=0.5),
#         plot.caption=element_text(hjust=0),
#         text = element_text(size=16))
# post_plot
# ggsave(filename=here("analysis","plots","mu_align_diff_two_aligned_posterior.jpeg"),width=7,height=5)
# 
# 
# d %>%
#   mutate(aligned=str_sub(order,1,2)) %>%
#   filter(config!="triangle") %>%
#   mutate(aligned2=case_when(
#     aligned %in% c("wh","hw") ~ "w aligned with h",
#     aligned %in% c("wd","dw") ~ "w aligned with d",
#     aligned %in% c("dh","hd") ~ "h aligned with d",
#   )) %>%
#   mutate(choice_align=case_when(
#     choice_name=="h" & aligned2=="h aligned with d"~"aligned option",
#     choice_name=="w" & aligned2=="h aligned with d"~"non-aligned option",
#     choice_name=="h" & aligned2=="w aligned with d"~"non-aligned option",
#     choice_name=="w" & aligned2=="w aligned with d"~"aligned option",
#     choice_name %in% c("h","w") & aligned2=="w aligned with h"~"aligned option",
#     choice_name=="d"~"decoy"
#   )) %>%
#   select(participant,config,aligned2,choice_name, choice_align) %>%
#   filter(aligned2!="w aligned with h") %>%
#   group_by(participant, config, choice_align) %>%
#   summarise(N=n()) %>%
#   group_by(participant,config) %>%
#   mutate(prop=N/sum(N)) %>%
#   ungroup() %>%
#   select(-N) %>%
#   pivot_wider(names_from = choice_align, values_from = prop) %>%
#   mutate(diff=`aligned option`-`non-aligned option`) %>%
#   select(-c(`aligned option`,decoy,`non-aligned option`)) %>%
#   pivot_wider(names_from = config, values_from = diff) %>%
#   mutate(diff_two_none=`two aligned`-`none aligned`,
#          diff_two_all=`two aligned`-`all aligned`) %>%
#   select(c(participant,diff_two_none,diff_two_all)) %>%
#   pivot_longer(contains("diff")) %>%
#   group_by(name) %>%
#   summarise(m=mean(value),
#             se=sd(value)/sqrt(n()),
#             lower=m-se,
#             upper=m+se) %>%
#   ungroup() %>%
#   ggplot(aes(name,m))+
#   geom_col(position="dodge",fill="lightblue",width=.5)+
#   geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
#   labs(y="mean choice prop.",x="alignment")+
#   labs(y="mean p(align)-p(non-aligned)",x="configuration")+
#   ggthemes::theme_few()
# 
# d %>%
#   mutate(aligned=str_sub(order,1,2)) %>%
#   filter(config!="triangle") %>%
#   mutate(aligned2=case_when(
#     aligned %in% c("wh","hw") ~ "w aligned with h",
#     aligned %in% c("wd","dw") ~ "w aligned with d",
#     aligned %in% c("dh","hd") ~ "h aligned with d",
#   )) %>%
#   select(participant,config,aligned2,choice_name) %>%
#   filter(aligned2!="w aligned with h") %>%
#   group_by(participant, config, aligned2, choice_name) %>%
#   summarise(N=n()) %>%
#   group_by(participant, config, aligned2) %>%
#   mutate(prop=N/sum(N)) %>%
#   select(-N) %>%
#   pivot_wider(names_from = config,
#               values_from = prop, values_fill = 0) %>%
#   mutate(diff_two_all=`two aligned`-`all aligned`,
#          diff_two_none=`two aligned`-`none aligned`) %>%
#   select(-c(aligned2, `all aligned`, `none aligned`, `two aligned`)) %>%
#   pivot_longer(c(diff_two_all,diff_two_none),names_to = "name", values_to = "diff") %>%
#   group_by(choice_name, name) %>%
#   summarise(m=mean(diff),
#             se=sd(diff)/sqrt(n()),
#             lower=m-se,
#             upper=m+se) %>%
#   ungroup() %>%
#   ggplot(aes(choice_name,m,fill=name))+
#   geom_col(position="dodge",width=.5)+
#   geom_errorbar(aes(ymin=lower,ymax=upper),position = position_dodge(.5),width=.2)+
#   # labs(y="mean choice prop.",x="alignment")+
#   labs(y="mean p(align)-p(non-aligned)",x="configuration")+
#   ggthemes::theme_few()
# 

