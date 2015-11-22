
close all;
clear all;
clc;

q = 0 : 0.01 : 1;

sigma = 1./q - 1;

figure;
hold on;

plot(q, sigma, 'linewidth', 3, 'color', 'r');

set(gca, 'linewidth', 2, 'fontsize', 12);
xlabel('Q');
ylabel('Sigma');
title('Illustration of clasterization factor');
xlim([0; 1]);
% ylim([0; 1]);
grid on;

hold off;
