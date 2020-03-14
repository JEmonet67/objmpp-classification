function tempe=VarCond(dep,taille,est)


% Written by Xavier Descombes, INRIA


dim    = size(dep);
offset = (taille-1)/2;

% Intialisation

tempe = zeros(dim(1),dim(2));
voisin = zeros(dim(1),dim(2));
carre = double(dep).*double(dep);
moy = zeros(256,1);
var = zeros(256,1);
num = zeros(256,1);

% Calcul de la moyenne des voisins en chaque point

dep = double(dep);

for i = 2 : dim(1)-1
 for j = 2 : dim(2)-1
   voisin(i,j) = 1 + (dep(i-1,j)+dep(i+1,j)+dep(i,j-1)+dep(i,j+1))/4.; 
                                                  % + 1 pour passer de [0,255] a [1,256]
 end
end

voisin(1,1) = 1 + (dep(2,1)+dep(1,2))/2.;
for j=2:dim(2)-1
    voisin(1,j) = 1 + (dep(1,j-1)+dep(1,j+1)+dep(i+1,j))/3.;
end
voisin(1,dim(2)) = 1 + (dep(1,dim(2)-1)+dep(2,dim(2)))/2.;
for i=2:dim(1)-1
    voisin(i,1) = 1 + (dep(i-1,1)+dep(i+1,1)+dep(i,2))/3.;
    voisin(i,dim(2)) = 1 + (dep(i-1,dim(2))+dep(i+1,dim(2)) + dep(i,dim(2)-1))/3.;
end
voisin(dim(1),1) = 1 + (dep(dim(1)-1)+dep(dim(1),2))/2.;
for j = 2:dim(2)-1
    voisin(dim(1),j) = 1 + (dep(dim(1),j-1)+dep(dim(1),j+1)+dep(dim(1)-1,j))/3.;
end
voisin(dim(1),dim(2)) = 1 + (dep(dim(1),dim(2)-1)+ dep(dim(1)-1,dim(2)-1))/2.;


for i=1:dim(1)
    for j=1:dim(2)
        voisin(i,j) = floor(voisin(i,j));
    end
end

% procedure de la fenetre glissante

  % initialisation

for i = 1 : taille 
 for j = 1 : taille
   num(voisin(i,j))  = num(voisin(i,j)) + 1;
   moy(voisin(i,j))  = moy(voisin(i,j)) + double(dep(i,j));
   var(voisin(i,j))  = var(voisin(i,j)) + double(carre(i,j));
 end
end

tempe(offset+1,offset+1) = estim(moy,var,num,est);

for i = offset+1 : 2 : dim(1)-offset 
  
  for j = offset+2 : dim(2)-offset
    for k = (-offset) : offset
      
     di = i+k; dj = j-offset-1;
     num(voisin(di,dj))  = num(voisin(di,dj)) - 1.; 
     moy(voisin(di,dj)) = moy(voisin(di,dj)) - double(dep(di,dj)); 
     var(voisin(di,dj)) = var(voisin(di,dj)) - double(carre(di,dj)); 
     dj = j+offset;
     num(voisin(di,dj)) = num(voisin(di,dj)) + 1.; 
     moy(voisin(di,dj)) = moy(voisin(di,dj)) + double(dep(di,dj)); 
     var(voisin(di,dj)) = var(voisin(di,dj)) + double(carre(di,dj)); 

    end
    tempe(i,j) = estim(moy,var,num,est);
    
  end

  % changement de ligne 
  
    for k = (-offset) : offset 
     
     di = i-offset; dj = dim(2)-offset+k;
     num(voisin(di,dj)) = num(voisin(di,dj)) - 1.; 
     moy(voisin(di,dj)) = moy(voisin(di,dj)) - double(dep(di,dj)); 
     var(voisin(di,dj)) =  var(voisin(di,dj)) - double(carre(di,dj)); 
     di = i+1+offset;
     num(voisin(di,dj)) = num(voisin(di,dj)) + 1.; 
     moy(voisin(di,dj)) =  moy(voisin(di,dj)) + double(dep(di,dj)); 
     var(voisin(di,dj)) = var(voisin(di,dj)) + double(carre(di,dj)); 
    end
    
    tempe(i+1,dim(2)-offset) = estim(moy,var,num,est);

%  ligne i+1 : de droite a gauche 

  for  j = dim(2)-offset-1 : -1 : offset+1 
    
    for k= (-offset) : offset 
      
     di = i+1+k; dj = j+offset+1;
     num(voisin(di,dj)) = num(voisin(di,dj)) - 1.; 
     moy(voisin(di,dj)) = moy(voisin(di,dj)) - double(dep(di,dj)); 
     var(voisin(di,dj)) = var(voisin(di,dj)) - double(carre(di,dj)); 
     dj = j-offset;
     num(voisin(di,dj)) = num(voisin(di,dj)) + 1.; 
     moy(voisin(di,dj)) = moy(voisin(di,dj)) + double(dep(di,dj)); 
     var(voisin(di,dj)) = var(voisin(di,dj)) + double(carre(di,dj)); 
   end
  tempe(i+1,j) = estim(moy,var,num,est);
  
  end

%  changement de ligne 

  if (i~=dim(1)-offset-1)
    
   for k=(-offset) : offset 
      di = i+1-offset; dj = offset+1+k;
      num(voisin(di,dj)) =  num(voisin(di,dj)) - 1.; 
      moy(voisin(di,dj)) = moy(voisin(di,dj)) - double(dep(di,dj)); 
      var(voisin(di,dj)) =  var(voisin(di,dj)) - double(carre(di,dj)); 
      di = i+2+offset;
      num(voisin(di,dj)) = num(voisin(di,dj)) + 1.; 
      moy(voisin(di,dj)) = moy(voisin(di,dj)) + double(dep(di,dj)); 
      var(voisin(di,dj)) = var(voisin(di,dj)) + double(carre(di,dj)); 
   end
   tempe(i+2,offset+1) = estim(moy,var,num,est);
   
  end  
end

% Affichage du parametre de texture

%imagesc(max(tempe./(double(dep)+0.1),0));



