clear

% define constants of E and tau
E1 = 3 * 10^10;
E2 = 5 * 10^6;
tau1 = 1;
tau2 = 10^3;

%define the range of t
for i = 1:10^6
    t(i) = i / 100;
end

%calculate the modulus function
for i = 1:10^6
    E(i) = E1 * exp(-t(i)/tau1) + E2 * exp(-t(i)/tau2);
end

%draw the logt-logE diagram
plot(log(t),log(E));

