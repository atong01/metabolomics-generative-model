function marginal = marginal(model, metfrag)
engine = smoother_engine(jtree_2TBN_inf_engine(model.bnet));
%engine = jtree_dbn_inf_engine(model.bnet);
%engine = jtree_inf_engine(model.bnet);

N = model.N;
engine
model.bnet
T = 1;
X = 3;
evidence = cell(N,T);
for i=1:T
   evidence{1,i} = 2;
   % evidence{5,i} = 2;
end
evidence
%soft_evidence = metfrag2soft_evidence(model, metfrag);

%[engine, loglik] = enter_evidence(engine, evidence, 'soft', soft_evidence);
[engine, loglik] = enter_evidence(engine, evidence);

post = zeros(1, N);
for i=1:N
  m = marginal_nodes(engine, i,T);
  m.T
  if (numel(m.T) == 2)
    post(i) = m.T(2);
  else
    post(i) = -1;
  end
end
marginal = post;