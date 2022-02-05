%Maxwell Model Dynamic Viscoelasticity Behaviour
clear

tau = 1;
E = 1;

for i = 1:10^6
    t(i) = i/1000;
    E1(i) = E*(t(i)*tau)^2/(1+(t(i)*tau)^2);
    E2(i) = E*t(i)*tau/(1+(t(i)*tau)^2);
    tandelta(i) = 1/(t(i)*tau);
end

plot(log(t),E1);
hold on
plot(log(t),E2);
hold on
plot(log(t),log(tandelta));
axis([-4 4 0 2]);