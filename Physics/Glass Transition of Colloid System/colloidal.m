phi = 0.68;                                     %�����й��������������
scale = 40;
particle = rand(scale,scale,scale);            %�������������ڽ����еķֲ�
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