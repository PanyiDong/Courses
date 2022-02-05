time = 1000;
Number = 1000;                                  %粒子数
position = zeros(Number,3,time);               %粒子位置
for i = 1:1:time-1
    for j = 1:1:Number
        direction = 3*rand(1);                 %判断运动方向
        if direction < 1
            if rand(1) > 0.5
                if particle(mod(position(j,1,i)+1,scale)+1,mod(position(j,2,i),scale)+1,mod(position(j,3,i),scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i)+1;
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            else
                if particle(mod(position(j,1,i)-1,scale)+1,mod(position(j,2,i),scale)+1,mod(position(j,3,i),scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i)-1;
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            end
        elseif direction > 2
            if rand(1) > 0.5
                if particle(mod(position(j,1,i),scale)+1,mod(position(j,2,i)+1,scale)+1,mod(position(j,3,i),scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i)+1;
                    position(j,3,i+1) = position(j,3,i);
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            else
                if particle(mod(position(j,1,i),scale)+1,mod(position(j,2,i)-1,scale)+1,mod(position(j,3,i),scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i)-1;
                    position(j,3,i+1) = position(j,3,i);
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            end
        else
            if rand(1) > 0.5
                if particle(mod(position(j,1,i),scale)+1,mod(position(j,2,i),scale)+1,mod(position(j,3,i)+1,scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i)+1;
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            else
                if particle(mod(position(j,1,i),scale)+1,mod(position(j,2,i),scale)+1,mod(position(j,3,i)-1,scale)+1) == 0
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i)-1;
                else
                    position(j,1,i+1) = position(j,1,i);
                    position(j,2,i+1) = position(j,2,i);
                    position(j,3,i+1) = position(j,3,i);
                end
            end
        end
    end
end

msd = zeros(1,time);
for i = 1:1:time
    for j = 1:1:Number
        msd(i) = msd(i)+position(j,1,i)^2+position(j,2,i)^2+position(j,3,i)^2;
    end
    msd(i) = msd(i)/Number;
end

t = 1:1:time;
plot(t,msd);