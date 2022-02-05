clear;

sigma = 10^8;
E1 = 5*10^8;
E2 = 10^8;
eta2 = 10^8;
tau2 = eta2/E2;     %tau2 = 1;
eta3 = 5*10^10;

for i = 1:1000
    t(i) = i/100;
    epsilon(i) = sigma/E1 + (sigma/E2)*(1-exp(-t(i)/tau2)) + (sigma/eta3)*t(i);
end

epsilon(1000) = (sigma/E2)*(1-exp(-10/tau2)) + (sigma/eta3)*10;

for i = 1001:2000
    t(i) = i/100;
    epsilon(i) = (sigma/E2)*(1-exp(-(10)/tau2))*exp(-(t(i)-10)/tau2) + (sigma/eta3)*(10);
end

plot(t,epsilon);