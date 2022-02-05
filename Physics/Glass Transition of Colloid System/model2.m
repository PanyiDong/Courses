room=zeros(200,200,200);
fai=0.68;
for i=1:200
    for j=1:200
        for k=1:200
            im=unifrnd (0,1);
            if im<fai
                room(i,j,k)=1;
            end
        end
    end
end

    
    originx=unidrnd(200);
    positionx=originx;
    originy=unidrnd(200);
    positiony=originy;
    originz=unidrnd(200);
    positionz=originz;
    for t=1:1000
        ts(t)=t;
        in=unifrnd (0,6);
        if in<=1 
            if positionz+1<=200
                if room(positionx,positiony,positionz+1)==0
                    positionz=positionz+1;
                end
            end
        elseif in<=2 
            if positionz-1>0
                if room(positionx,positiony,positionz-1)==0
                    positionz=positionz-1;
                end
            end
        elseif in<=3 
            if positiony+1<=200
                if room(positionx,positiony+1,positionz)==0
                    positionz=positiony+1;
                end
            end
        elseif in<=4 
            if positiony-1>0
                if room(positionx,positiony-1,positionz)==0
                    positionz=positiony-1;
                end
            end
        elseif in<=5 
            if positionx+1<=200
                if room(positionx+1,positiony,positionz)==0
                    positionz=positionx+1;
                end
            end
        elseif in<=6 
            if positionx-1>0
                if room(positionx-1,positiony,positionz)==0
                    positionz=positionx-1;
                end
            end
        end
    MSD(t)=(originx-positionx)^2+(originy-positiony)^2+(originz-positionz)^2;
    end
plot(ts,MSD)
    
        
