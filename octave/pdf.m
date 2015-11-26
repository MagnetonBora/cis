
close all;
clear all;
clc;

m = 50;
sigma = 2;
K = 0.75;

x = 0 : 0.1 : 100;

y0 = K * (1/sigma*sqrt(2*pi)) * exp( -(x - m).^(2*1) / 2 * sigma * sigma );
y1 = K * (1/sigma*sqrt(2*pi)) * exp( -(x - m).^(2*2) / 2 * sigma * sigma );
y2 = K * (1/sigma*sqrt(2*pi)) * exp( -(x - m).^(2*3) / 2 * sigma * sigma );
y3 = K * (1/sigma*sqrt(2*pi)) * exp( -(x - m).^(2*4) / 2 * sigma * sigma );
y4 = K * (1/sigma*sqrt(2*pi)) * exp( -(x - m).^(0.01) / 2 * sigma * sigma );

figure;
hold on;

plot(x, y0, 'linewidth', 3, 'color', 'b');
plot(x, y1, 'linewidth', 3, 'color', 'r');
plot(x, y2, 'linewidth', 3, 'color', 'g');
plot(x, y3, 'linewidth', 3, 'color', 'y');
plot(x, y4, 'linewidth', 3, 'color', 'm');

set(gca, 'linewidth', 2, 'fontsize', 12);
xlabel('Ages');
ylabel('Probability');
title('Illustration of clasterization factor');
legend('Q=0.10', 'Q=0.25', 'Q=0.50', 'Q=0.75', 'Q=0.99');
xlim([45; 55]);
ylim([0; 1]);
grid on;

hold off;
