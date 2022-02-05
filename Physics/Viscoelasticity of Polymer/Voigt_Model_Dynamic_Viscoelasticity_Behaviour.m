%Voigt Model Dynamic Viscoelasticity Behaviour

clear

tau = 1;
D = 1;

for i = 1:10^6
    t(i) = i/1000;
    D1(i) = D/(1+(t(i)*tau)^2);
    D2(i) = D*t(i)*tau/(1+(t(i)*tau)^2);
    tandelta(i) = t(i)*tau;
end

plot(log(t),D1);
hold on
plot(log(t),D2);
hold on
plot(log(t),log(tandelta));
axis([-4 4 0 4]);