%Voigt Model Creep
clear

tau = 20;

for i =1:2*10^4
    t(i) = i/100;
    epsilon(i) = 1-exp(-t(i)/tau);
end

plot(t,epsilon);