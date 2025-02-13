# create stimuli for comparability exp
# UPDATED TO BE HARDER
# RATHER THAN 35 and 20, DISTANCE = 35 & 20
# catch & fillers are created on the fly during experiment
# winter 2025
# setup ======================================================================
# clear environment
rm(list=ls())

# libraries
library(tidyverse)
library(here)

# necessary functions
distance <- function(a,b) sqrt( (a[1]-b[1])^2 + (a[2]-b[2])^2  )
compute_tdd <- function(stim,area) round((1-prod(stim)/area),digits=2)*100

# make stim ======================================================================

# three diagonals
h_upper <- c(125,200)
w_upper <- rev(h_upper)

h_lower <- c(57,133)
w_lower <- rev(h_lower)

# distances are approximately the same across diagonals9
distance(h_lower,w_lower)
distance(h_upper,w_upper)

# areas of each diagonal
area_lower <- prod(h_lower)
area_upper <- prod(h_upper)

# decoy areas - lower diagonal
area_lower_35 <- area_lower*.65
area_lower_20 <- area_lower*.80

# make decoys - lower diagonal
d_lower_35 <- round(rep(sqrt(area_lower_35),2))
d_lower_20 <- round(rep(sqrt(area_lower_20),2))

# tdd check
compute_tdd(d_lower_35, area_lower)
compute_tdd(d_lower_20, area_lower)

# decoy areas - upper diagonal
area_upper_35 <- area_upper*.65
area_upper_20 <- area_upper*.80

# make decoys - upper diagonal
d_upper_35 <- round(rep(sqrt(area_upper_35),2))
d_upper_20 <- round(rep(sqrt(area_upper_20),2))

# tdd check
compute_tdd(d_upper_35, area_upper)
compute_tdd(d_upper_20, area_upper)

# combine stim ======================================================================
# combine all stim in tmp matrix
stim_tmp <- rbind(
  "h_lower_0"=h_lower,
  "w_lower_0"=w_lower,
  "d_lower_35"=d_lower_35,
  "d_lower_20"=d_lower_20,
  "h_upper_0"=h_upper,
  "w_upper_0"=w_upper,
  "d_upper_35"=d_upper_35,
  "d_upper_20"=d_upper_20
)

# combine into nice df
all_stim <- tibble(
  name=rownames(stim_tmp),
  w=unname(stim_tmp[,1]),
  h=unname(stim_tmp[,2])
) %>%
  separate(name,into=c("name","diag","distance")) %>%
  mutate(distance=as.numeric(distance),
         distance=na_if(distance,0),
         area=h*w)

# plotting ======================================================================
p <- all_stim %>%
  mutate(name=toupper(name)) %>%
  ggplot(aes(w,h,col=name))+
  geom_point(size=2.5,alpha=.5)+
  labs(x="Width",y="Height")+
  scale_color_discrete(name="Stimulus")+
  scale_x_continuous(breaks=c(0,150,300))+
  scale_y_continuous(breaks=c(0,150,300))+
  coord_fixed(xlim=c(0,300),ylim=c(0,300))+
  ggthemes::theme_few()
p

# saving stim ======================================================================
p
ggsave(filename=here("specs","stim.jpg"),width=4,height=4)
write_csv(all_stim,file=here("specs","all_stim.csv"))

# catch stim ========================================================================
dlower_w <- seq(h_lower[1],w_lower[1])
dlower_h <- lm(h_lower~w_lower)$coefficients["(Intercept)"]-dlower_w

dupper_w <- seq(h_upper[1],w_upper[1])
dupper_h <- lm(h_upper~w_upper)$coefficients["(Intercept)"]-dupper_w

par(pty='s')
plot(NA,NA,xlim=c(0,300),ylim=c(0,300),xlab="w",ylab="h")
points(dlower_w,dlower_h,pch=".")
points(dupper_w,dupper_h,pch=".")

# catch stim ========================================================================
min(all_stim$w)
max(all_stim$w)
min(all_stim$h)
max(all_stim$h)

w <- runif(10000, 57, 200)
h <- runif(10000, 57, 200)
par(pty='s')
plot(NA,NA,xlim=c(0,300),ylim=c(0,300),xlab="w",ylab="h")
points(w,h,pch=".")
a <- w*h
hist(a)
