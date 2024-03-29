clc,clear,close;

% g_finaldata.txt  經緯度、時間
lat_data = importdata('g_latdata.txt');   %
lng_data = importdata('g_lngdata.txt');   %
time_data = importdata('g_timedata.txt');   %

% [m17,n17] = size(lat_data);
% for row = 1:m17
%     data17_sort(row,1) = str2double(sprintf('%.7f',lat_data(row,1))); %是數字
%     data18_sort(row,1) = str2double(sprintf('%.7f',lng_data(row,1)));
% end

lat_data_str = num2str(lat_data,"%.7f");
lng_data_str = num2str(lng_data,"%.7f");

% time_data資料處理
% time_data為struct(double+cell),要轉換為matrix
% time_data.data是數字
[mt,nt] = size(time_data.data); 
for l = 1:mt
time_data_date_n_hour(l,1) = time_data.rowheaders(l,:); %是字串
end
m_time_data_date_n_hour = cell2mat(time_data_date_n_hour);
s_time_data.data = string(time_data.data);
for k = 1:mt
    time_data_sort(k,1) = strcat(m_time_data_date_n_hour(k,:),":",s_time_data.data(k,1),":",s_time_data.data(k,2)); 
end

total_data4 = horzcat(lat_data_str, lng_data_str,time_data_sort);
gpstitle = ["Latitude","Longitude","Time"];
data_with_title4 = vertcat(gpstitle,total_data4);

% 若comdinated.txt存在,刪除combinated.txt
if exist('g_finaldata.txt','file')
    delete('g_finaldata.txt');
end

% 創建檔案
filename = fopen('g_finaldata.txt','w');

% 檢查是否打開成功 '=='為判定
if filename == -1
    error('無法打開文件%s','g_finaldata.txt');
end
for j = 1:mt+1
    fprintf(filename,'%-14s %-14s %-14s\n',data_with_title4(j,1),data_with_title4(j,2),data_with_title4(j,3));
end
% 關閉檔案
fclose(filename);

%---------------------------------------------------------
% 局部地圖
% 下載桃園區的行政邊界數據（Shapefile 格式）

% 將數據導入 MATLAB
taoyuan_city = shaperead('TOWN_MOI_1120317.shp', 'UseGeoCoords', true);

% 創建地圖圖形並設置地圖投影
figure;
ax = axesm('MapProjection', 'mercator');

% 中央大學經緯度座標
lat_ncu = 24.968972;
lon_ncu = 121.1946;

% 設置坐標軸
lonlim = [min(lon_ncu)-0.08,max(lon_ncu)+0.08];
latlim = [min(lat_ncu)-0.08,max(lat_ncu)+0.08];
worldmap(latlim,lonlim);

% 繪製桃園區區域邊界
geoshow(ax, taoyuan_city, 'FaceColor', 'yellow', 'EdgeColor', 'black');

% 設定座標軸範圍
setm(ax,'MapLatLimit',latlim,'MapLonLimit',lonlim);

% 添加座標軸
framem('Grid','on');
mlabel('on');

% 標記中央大學
scatterm(lat_ncu, lon_ncu, 'r', 'filled');
textm(lat_ncu, lon_ncu, 'NCU', 'Color', 'black', 'FontSize', 10, 'FontWeight', 'bold','HorizontalAlignment', 'right');

% 將GPS點數據進行連接
% 找到非零的 GPS 數據的索引
non_zero_indices = ~(lat_data(:, 1) == 0 & lng_data(:, 1) == 0);

% 過濾掉數值為 0.0 的數據
non_zero_lat_data = lat_data(non_zero_indices, :);
non_zero_lng_data = lng_data(non_zero_indices, :);
plotm(non_zero_lat_data(:,1), non_zero_lng_data(:,1), '-r');

% 要標記的點的經緯度坐標
% 在地圖上繪製點
plotm(non_zero_lat_data(:,1), non_zero_lng_data(:,1), 'r');

% 添加標題
title('Taoyuan');

% 判斷就有png檔是否存在
% 檢查是否存在
if exist('taoyuan_city_map.png','file')
    delete('taoyuan_city_map.png');
end

% 保存地圖為圖片
saveas(gcf, 'taoyuan_city_map.png');


