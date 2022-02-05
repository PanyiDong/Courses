function cell=cellist(x,y,z)
length=50;
if x<=length/2 && y<=length/2 && z<=length/2
    cell=1;
elseif x>length/2 && x<=length && y<=length/2 && z<=length/2
    cell=2;
elseif x<=length/2 && y>length/2 && y<=length && z<=length/2
    cell=3;
elseif x>length/2 && x<=length && y>length/2 && y<=length && z<=length/2
    cell=4;
elseif x<=length/2 && y<=length/2 && z>length/2 && z<=length
    cell=5;
elseif x>length/2 && x<=length && y<=length/2 && z>length/2 && z<=length
    cell=6;
elseif x<=length/2 && y>length/2 && y<=length && z>length/2 && z<=length
    cell=7;
elseif x>length/2 && x<=length && y>length/2 && y<=length && z>length/2 && z<=length
    cell=8;
end