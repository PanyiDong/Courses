
%规定常数
sigma=0.1;
meanR=1;
Number=15422;
length=50;
dlumda=0.02;
x=zeros(100,Number);
y=zeros(100,Number);
z=zeros(100,Number);
cell0=zeros(1,Number);
R=zeros(1,Number);

%生成满足正态分布的粒子半径并去除不需要的部分
i=1;
while i<=Number
R(i) = normrnd(meanR,sigma);
if abs(R(i)-1)-3*sigma>0
    i=i-1;
end
i=i+1;
end

%算出粒子的体积分数
V=0;
for i=1:Number
    V=V+4/3*pi*R(i)^3;
end
Phi=V/length^3;
fprintf('粒子的体积分数为%.2f',Phi);

%随机生成粒子位置并列入list中
x(1,1)=unifrnd (0,length);
y(1,1)=unifrnd (0,length);
z(1,1)=unifrnd (0,length);
cell0(1)=cellist(x(1,1),y(1,1),z(1,1));
i=2;
while i<=Number
    x(1,i)=unifrnd (0,length);
    y(1,i)=unifrnd (0,length);
    z(1,i)=unifrnd (0,length);
    cell0(i)=cellist(x(1,i),y(1,i),z(1,i));
    for j=1:i-1
        if (x(1,i)-x(1,j))^2+(y(1,i)-y(1,j))^2+(z(1,i)-z(1,j))^2-(R(i)+R(j))^2<0
            i=i-1;
            break
        end
    end
    i=i+1;
end
MSD(1)=0;

%随机粒子的运动过程
for t=2:100
    for i=1:Number
        x(t,i)=x(t-1,i);
        y(t,i)=y(t-1,i);
        z(t,i)=z(t-1,i);
    end
MSD(t)=MSD(t-1);
for ts=1:1000
    N(ts)=unidrnd(Number);
    dx(ts)=unifrnd (-dlumda,dlumda);
    dy(ts)=unifrnd (-dlumda,dlumda);
    dz(ts)=unifrnd (-dlumda,dlumda);
    if x(t,N(ts))+dx(ts)>=0 && x(t,N(ts))+dx(ts)<=length && y(t,N(ts))+dy(ts)>=0 && y(t,N(ts))+dy(ts)<=length && z(t,N(ts))+dz(ts)>=0 && z(t,N(ts))+dz(ts)<=length
    x(t,N(ts))=x(t,N(ts))+dx(ts);
    y(t,N(ts))=y(t,N(ts))+dy(ts);
    z(t,N(ts))=z(t,N(ts))+dz(ts);
    for j=1:Number
        if abs(cell0(j)-cell0(N(ts)))<1 && abs(j-N(ts))>0
            if (x(t,N(ts))-x(t,j))^2+(y(t,N(ts))-y(t,j))^2+(z(t,N(ts))-z(t,j))^2-(R(N(ts))+R(j))^2<0
                x(t,N(ts))=x(t,N(ts))-dx(ts);
                y(t,N(ts))=y(t,N(ts))-dy(ts);
                z(t,N(ts))=z(t,N(ts))-dz(ts);
                break
            end
        end
    end
    cell0(N(ts))=cellist(x(t,N(ts)),y(t,N(ts)),z(t,N(ts)));
    end
end

%算出MSD随时间的变化过程
for i=1:Number
    MSD(t)=MSD(t)+(x(t,i)-x(1,i))^2+(y(t,i)-y(1,i))^2+(z(t,i)-z(1,i))^2;
end
end

%绘制MSD的时间变化图像

for t=1:100
time(t)=t;
end

plot(log10(time),log10(MSD));
    
