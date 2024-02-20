%{
x1 = 50/220:50/220:50;
x2 = 50/41184-3:53/41184:50;
plot(x1,accz(1:220)*0.9333,'r')
hold on
plot(x2,accY,'b')
hold off

plot(Rx)
hold on
plot(Ry)
hold on
plot(Rz)
legend({ 'Rx','Ry','Rz' }, 'Location' , 'northeast' )
hold off

x1 = 72/340:72/340:72;
x2 = 72/60023:72/60023:72;
plot(x1,gyroy(57:396)+43,'r')
hold on
plot(x2,gyro/pi*180,'b')
hold off
%}

x1 = 72/340:72/340:72;
x2 = 72/60023:72/60023:72;
plot(x1,gyroz(57:396),'r')
hold on
plot(x2,gyro/pi*180,'b')
hold off

