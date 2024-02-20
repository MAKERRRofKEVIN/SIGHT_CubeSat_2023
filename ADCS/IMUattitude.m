%clc,close,clear;

data10 = importdata('accx.txt');
data11 = importdata('accy.txt');
data12 = importdata('accz.txt');
data13 = importdata('gyrox.txt');
data14 = importdata('gyroy.txt');
data15 = importdata('gyroz.txt');
data16 = importdata('m_timedata.txt');

%Accler
for i = 1:length(data10)
    %向量
    A(i) = sqrt(data10(i,1)^2+data11(i,1)^2+data12(i,1)^2);%標準化
    Ax(i) = data10(i,1)/A(i);
    Ay(i) = data11(i,1)/A(i);
    Az(i) = data12(i,1)/A(i);
    %角度
    %Axr(i) = acos(data10(i,1)/A(i));
    %Ayr(i) = acos(data11(i,1)/A(i));
    %Azr(i) = acos(data12(i,1)/A(i));
end

%每筆數據間隔時間
for i = 1:length(data16.data)-1
    delt(i) = data16.data(i+1,1)*60 + data16.data(i+1,2) - data16.data(i,1)*60 - data16.data(i,2);
end

%扣除誤差
errx = mean(data13(1:150,1));
erry = mean(data14(1:150,1));
errz = mean(data15(1:150,1));
newdata13 = data13 - errx;
newdata14 = data14 - erry;
newdata15 = data15 - errz;

%初始值
Rx(1) = Ax(1);
Ry(1) = Ay(1);
Rz(1) = Az(1);
Gx(1) = 0;
Gy(1) = 0;
Gz(1) = 0;

%algorithm 2.0
for i = 1:length(data13)-1
    Ayz(i) = atan2(Ry(i),Rz(i))/pi*180;%Diameter to angle
    Axz(i) = atan2(Rx(i),Rz(i))/pi*180;
    Axy(i) = atan2(Rx(i),Ry(i))/pi*180;
    %Gyro
    RateAyzAvg = (newdata13(i+1,1) + newdata13(i,1))/2;%angle
    RateAxzAvg = (newdata14(i+1,1) + newdata14(i,1))/2;
    RateAxyAvg = (newdata15(i+1,1) + newdata15(i,1))/2;
    Ayz(i+1) =  Ayz(i) + RateAyzAvg * delt(i);
    Axz(i+1) =  Axz(i) + RateAxzAvg * delt(i);
    Axy(i+1) =  Axy(i) + RateAxyAvg * delt(i);
    %angle to victor
    Gx(i+1) = sind(Axz(i+1)) / sqrt(1+cosd(Axz(i+1))^2 * tand(Ayz(i+1))^2);
    Gy(i+1) = sind(Ayz(i+1)) / sqrt(1+cosd(Ayz(i+1))^2 * tand(Axz(i+1))^2);
    Gz(i+1) = cosd(Ayz(i+1)) / sqrt(1+sind(Ayz(i+1))^2 * tand(Axy(i+1))^2);
    Gzz(i+1) = sqrt(1-Gx(i+1)^2-Gy(i+1)^2);
    G = sqrt(Gx(i+1)^2+Gy(i+1)^2+Gz(i+1)^2);%standardization
    Gx(i+1) = Gx(i+1)/G;
    Gy(i+1) = Gy(i+1)/G;
    Gz(i+1) = Gz(i+1)/G;
    %weighted
    wGyro = 5;
    Rx(i+1) = (Ax(i+1) + Gx(i+1) * wGyro) / (1 + wGyro);
    Ry(i+1) = (Ay(i+1) + Gy(i+1) * wGyro) / (1 + wGyro);
    Rz(i+1) = (Az(i+1) + Gz(i+1) * wGyro) / (1 + wGyro);
    R = sqrt(Rx(i+1)^2+Ry(i+1)^2+Rz(i+1)^2);%standardization
    Rx(i+1) = Rx(i+1)/R;
    Ry(i+1) = Ry(i+1)/R;
    Rz(i+1) = Rz(i+1)/R;
end

%{
%algorithm 1.0
Ayz(1) = atan2(data11(1,1),data12(1,1))/pi*180;%徑度to角度
Axz(1) = atan2(data10(1,1),data12(1,1))/pi*180;
Axy(1) = atan2(data10(1,1),data11(1,1))/pi*180;
for i = 1:length(data13)-1
    RateAyzAvg(i) = (newdata13(i+1,1) + newdata13(i,1))/2;%角度
    RateAxzAvg(i) = (newdata14(i+1,1) + newdata14(i,1))/2;
    RateAxyAvg(i) = (newdata15(i+1,1) + newdata15(i,1))/2;
    Ayz(i+1) =  Ayz(i) + RateAyzAvg(i) * delt(i);
    Axz(i+1) =  Axz(i) + RateAxzAvg(i) * delt(i);
    Axy(i+1) =  Axy(i) + RateAxyAvg(i) * delt(i);
    Gx(i) = sind(Axz(i)) / sqrt(1+cosd(Axz(i))^2 * tand(Ayz(i))^2);
    Gy(i) = sind(Ayz(i)) / sqrt(1+cosd(Ayz(i))^2 * tand(Axz(i))^2);
    Gz(i) = cosd(Ayz(i)) / sqrt(1+sind(Ayz(i))^2 * tand(Axy(i))^2);
    Gzz(i) = sqrt(1-Gx(i)^2-Gy(i)^2);
end
%加權
wGyro = 5;
Rx = (Ax + Gx * wGyro) / (1 + wGyro);
Ry = (Ay + Gy * wGyro) / (1 + wGyro);
Rz = (Az + Gz * wGyro) / (1 + wGyro);
%}