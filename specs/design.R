rm(list=ls())
library(tidyverse)
library(here)
stim <- here("specs","all_stim.csv") %>%
  read_csv()

order <- c("dhw","dwh","wdh","whd","hwd","hdw")
distance <- c(35,20)      
config <- c(1,2,3,4)
diag <- c("lower","upper")
crit_init <- expand_grid(order,distance,config,diag)
crit_trials_1 <- bind_rows(
  filter(crit_init,config==2) %>%
    mutate(config=2.1),
  filter(crit_init,config==2) %>%
    mutate(config=2.1), # THIS WAS A MISTAKE SHOULD HAVE BEEN 2.2
  filter(crit_init, config!=2)
) %>%
  mutate(effect="critical") %>%
  relocate(effect,.before=everything()) %>%
  mutate(h_1=numeric(nrow(.)),
         w_1=numeric(nrow(.)),
         h_2=numeric(nrow(.)),
         w_2=numeric(nrow(.)),
         h_3=numeric(nrow(.)),
         w_3=numeric(nrow(.)))


for(i in 1:nrow(crit_trials_1)){
  cat(paste0("\n",i,"/",nrow(crit_trials_1),"\n"))
  crit_tmp <- crit_trials_1[i,]
  stim_tmp <- filter(stim, (distance==crit_tmp$distance|is.na(distance)) & diag==crit_tmp$diag)
  s_1 <- str_sub(crit_tmp$order,1,1)
  s_2 <- str_sub(crit_tmp$order,2,2)
  s_3 <- str_sub(crit_tmp$order,3,3)
  crit_trials_1$h_1[i] <- filter(stim_tmp, name==s_1)$h
  crit_trials_1$w_1[i] <- filter(stim_tmp, name==s_1)$w
  crit_trials_1$h_2[i] <- filter(stim_tmp, name==s_2)$h
  crit_trials_1$w_2[i] <- filter(stim_tmp, name==s_2)$w
  crit_trials_1$h_3[i] <- filter(stim_tmp, name==s_3)$h
  crit_trials_1$w_3[i] <- filter(stim_tmp, name==s_3)$w
}

all_trials <- bind_rows(
  crit_trials_1,
  tibble(effect=rep("catch",10)),
  tibble(effect=rep("filler_random",40)),
  tibble(effect=rep("filler_square",40))
)

write_csv(all_trials,file=here("specs","trials.csv"))
write_csv(all_trials,file=here("experiment_code","trials.csv"))


check <- all_trials %>%
  filter(effect=="critical") %>%
  mutate(a_1=h_1*w_1,
         a_2=h_2*w_2,
         a_3=h_3*w_3) %>%
  rowwise() %>%
  mutate(which_d=case_when(
    h_1==w_1~1,
    h_2==w_2~2,
    h_3==w_3~3
  )) %>%
  mutate(check=case_when(
    which_d==1 ~ (a_1 < a_2) & (a_1 < a_3),
    which_d==2 ~ (a_2 < a_1) & (a_2 < a_3),
    which_d==3 ~ (a_3 < a_1) & (a_3 < a_2)
  )) %>%
  ungroup()
print(unique(check$check))
