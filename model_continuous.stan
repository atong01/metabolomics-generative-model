data {
  int<lower=0> P;
  int<lower=0> M;
  real<lower=0.0> detection_shape;
  real<lower=0.0> detection_rate;
  real<lower=0.0> activity_shape;
  real<lower=0.0> activity_rate;
  // metabolite_mask[m,p] = 1.0 if pathway p involves metabolite m
  matrix<lower=0.0,upper=1.0>[M,P] metabolite_mask;
  // y[m] is the peak height for metabolite M
  real<lower=0.0> y[M];
}
parameters {
  vector<lower=0.0>[P] k;
  vector<lower=0.0>[M] theta;
}
model {
  // prevalence of each metabolite (summed over pathways)
  k ~ gamma(activity_shape, activity_rate);
  // detection rate for each metabolite
  theta ~ gamma(metabolite_mask * rep_vector(detection_shape, P), detection_rate);
  // peak height for each metabolite
  y ~ gamma(metabolite_mask * k, 1.0 ./ theta);
}