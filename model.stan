data {
  int<lower=0> P;
  int<lower=0> M;
  real<lower=0.0> rate_prior;
  // metabolite_mask[p,m] = 1.0 if pathway p involves metabolite m
  matrix<lower=0.0,upper=1.0>[P,M] metabolite_mask;
  // y[m] = 1 if metabolite m has been observed
  int<lower=0,upper=1> y[M];
}
parameters {
  real<lower=0.0,upper=1.0> eps;
  vector<lower=0.0>[P] a;
  matrix<lower=0.0>[P,M] b;
}
transformed parameters {
  row_vector<lower=0.0>[M] beta;
  beta <- rep_row_vector(1.0, P) * (b .* metabolite_mask);
}
model {
  // base probability of detection
  eps ~ beta(0.01, 1.0);
  // activity rate for each pathway
  a ~ gamma(rate_prior, 1.0);
  for (m in 1:M)
    // per-pathway activity rate for metabolite m
    b[:,m] ~ gamma(a, 1.0);
  for (m in 1:M)
    if (y[m]==1)
      // log probability of detection
      target += log(eps) - 0.5*beta[m] + log(1-exp(-beta[m]));
    else 
      // log probability of detection failure
      target += log((1-eps) + eps*exp(-beta[m]));
}