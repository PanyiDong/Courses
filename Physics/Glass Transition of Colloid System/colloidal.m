phi = 0.68;                                     %胶体中固体粒子体积分数
scale = 40;
particle = rand(scale,scale,scale);            %构建固体粒子在胶体中的分布
for i = 1:1:scale
    for j = 1:1:scale
        for k = 1:1:scale
            if particle(i,j,k) < phi
                particle(i,j,k) = 1;
            else
                particle(i,j,k) = 0;
            end
        end
    end
end