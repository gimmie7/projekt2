function main_GUI
global Diagram

Diagram.figure = figure('Name','Diagramm','NumberTitle','off','MenuBar','none','units','normalized','Position',[.2 .1 .6 .8]);
Diagram.axis1=axes('parent',Diagram.figure ,'units','normalized','position',[.1 .17 .75 .75],'NextPlot','replace');
grid(Diagram.axis1,'on')
Diagram.axis1.Title.String='"Verbraucher"';
Diagram.axis1.XLabel.String = 'X Axis';
Diagram.axis1.YLabel.String = 'Y Axis';
p=line('Parent',Diagram.axis1,'XData',[],'YData',[],'LineStyle','-','marker','.','color','b','LineWidth',2);
q=line('Parent',Diagram.axis1,'XData',[],'YData',[],'LineStyle','-','marker','.','color','g','LineWidth',2);
s=line('Parent',Diagram.axis1,'XData',[],'YData',[],'LineStyle','-','marker','.','color','r','LineWidth',2);

grid on
axis([0 180 0 2000]);
%axis([-150 700 -250 250]);
xlabel ('Zeit [s]');
ylabel ('Leistung');

Array=csvread('test.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
col3 = Array(:, 3);
col4 = Array(:, 4);

p.XData=col1;
p.YData=col2;

q.XData=col1;
q.YData=col3;

s.XData=col1;
s.YData=col4;

drawnow
pause(0.2)




