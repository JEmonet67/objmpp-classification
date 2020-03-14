function varcond=estim(ordre1,ordre2,nombre,est)


if est == 1
argmax = 1; max = nombre(1);
 
for x = 2 : 256 
   if (max <nombre(x)) 
    max = nombre(x); 
   argmax = x; 
 end
 end
 
 x = argmax;
 if (nombre(x) ~= 0)
 varcond = ordre2(x)/nombre(x) - (ordre1(x)*ordre1(x))/(nombre(x)*nombre(x)) ;
 else varcond = 0;
 end
else
 varcond = 0;
 somme = 0;

  for x = 2 : 256
     
    if (nombre(x) ~= 0)

        varcond = varcond + ordre2(x) - (ordre1(x)*ordre1(x))/nombre(x);
        somme = somme + nombre(x);
    end
   end
  varcond = varcond/somme;
end
