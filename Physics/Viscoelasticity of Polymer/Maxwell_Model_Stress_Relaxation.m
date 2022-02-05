%Maxwell Model Stress Relaxation
clear

E = 10^7;
eta = 5*10^7;
tau = 5;

for i = 1:2500
    t(i) = i/100;
    sigma(i) = exp(-t(i)/tau);
end

plot(t,sigma);

