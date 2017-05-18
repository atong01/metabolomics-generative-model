function soft_evidence = metfrag2soft_evidence(model, evidence)
% model is bnet model wrapper containing N, Npathways
% evidence is a cell array for each piece of unconfirmed observed
%
soft_evidence = [cell(1, model.Npaths) evidence cell(1, 2 * model.Nmets)];
   
