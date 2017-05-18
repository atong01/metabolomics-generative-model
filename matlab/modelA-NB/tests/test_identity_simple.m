G = [1 0 0;
     0 1 0;
     0 0 1];
unconfirmed = 1;

model = mk_model(G, unconfirmed);

se = [0.3 0.7 0];

marginal(model, se)