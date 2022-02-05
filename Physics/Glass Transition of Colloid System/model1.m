
for nmuber=1:1000
fai=0.58;
position(1)=0;
t=1;
for time=1:1000
    t(time+1)=time+1;
    imove=unifrnd (0,1);
    if imove>0.5
        position(time+1)=position(time)+1;
        im=unifrnd (0,1);
        if im<fai
            position(time+1)=position(time)-1;
        end
    else
        position(time+1)=position(time)-1;
        im=unifrnd (0,1);
        if im<fai
            position(time+1)=position(time)+1;
        end
    end
end
plot(t,position)
axis([0 1000 -100 100])
hold on
end
        