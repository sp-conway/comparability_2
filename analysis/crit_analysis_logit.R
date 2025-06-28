rm(list=ls())
library(tidyverse)
library(here)
library(fs)
library(glue)
library(rstanarm)
library(bayesplot)
library(latex2exp)
library(lmerTest)

# stan sampler settings ===============================================================
n_chain <- n_core <- 4
n_iter <- 2000
n_warm <- 500

# read in and set up data ======================================================================
d <- here("data","clean","data.csv") %>%
  read_csv() %>%
  filter(str_detect(effect,"critical") & choice_name!="d") %>%
  mutate(
  participant=as.factor(participant),
  middle_option=str_sub(order,2,2),
    config=case_when(
      config_1==1~"all aligned",
      config_1==2.1~"two aligned",
      config_1==3~"none aligned",
      config_1==4~"triangle"),
      order=factor(order,
                   levels=c("dhw","hdw",
                            "dwh","wdh",
                            "hwd","whd")),
      choice_name=factor(choice_name,levels=c("h","w"))) %>%
    filter(config!="triangle") %>%
    mutate(
    config=factor(config,levels=c("none aligned","two aligned","all aligned")),
    aligned=str_sub(order,1,2),
    aligned2=case_when(
      aligned %in% c("wh","hw") ~ "w aligned with h",
      aligned %in% c("wd","dw") ~ "w aligned with d",
      aligned %in% c("dh","hd") ~ "h aligned with d",
    )) %>%
  filter(aligned2!="w aligned with h") %>%
  mutate(choose_target=case_when(
    aligned2=="w aligned with d" & choice_name=="w"~1,
    aligned2=="h aligned with d" & choice_name=="h"~1,
    T~0
  ),
  target_middle=case_when(aligned2=="w aligned with d" & middle_option=="w"~1,
                          aligned2=="h aligned with d" & middle_option=="h"~1,
                          T~0))

# glmer model 1 - ========================================================================
# m1_glmer <- glmer(choose_target~config+target_middle+(1|participant), 
#                   data=d,
#                   family=binomial,verbose = T)
# summary(m1_glmer)

# stan glmer model 1 - ========================================================================
m1_file <- here("analysis/bayes/m1/m1_fit.RData")
m1_summary_file <- here("analysis/bayes/m1/m1_fit_summary.RData")
if(!file_exists(m1_file)){
  m1 <- stan_glmer(choose_target~config+target_middle+(1|participant), 
                    data=d,cores=n_core,iter=n_iter,
                    family=binomial)
  save(m1,file=m1_file)
  m1_summary <- summary(m1,probs=c(.025,.975),digits=5)
  save(m1_summary,file=m1_summary_file)
}else{
  load(m1_file)
  load(m1_summary_file)
}
m1_summary[1:4,c("mean","sd","2.5%","97.5%")]
mcmc_trace(m1,"(Intercept)")
lp <- log_posterior(m1)
mcmc_trace(lp,"Value")
mcmc_hist(m1,"configtwo aligned")+
  labs(x=TeX("$\\beta_{two\\;aligned}$"))

b_two_aligned <- as.matrix(m1)[,"configtwo aligned"]
HDInterval::hdi(b_two_aligned)
mean(b_two_aligned<0)

# mean target choice in none aligned
plogis(-0.18365)
# mean target choice in two aligned
plogis(-0.18365-.03)
