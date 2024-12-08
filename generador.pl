% Reglas para determinar la altura de un punto según ruido 
altura(X, _Y, Perlin, Altura) :-  
    BaseAltura is Perlin * 10,
    (BaseAltura > 0 -> Altura is BaseAltura; Altura is 0),
    (X > -1, X < 1 -> Altura is 0; true).  % Río en el centro

% Colores basados en la altura
color(Altura, R, G, B) :-
    (Altura < 1 -> R = 139, G = 69, B = 19;      % Montañas (marrón)
    Altura < 3 -> R = 34, G = 139, B = 34;       % Hierba
    Altura < 5 -> R = 107, G = 142, B = 35;      % Bosque
    R = 0, G = 0, B is 255 - Altura * 20). %rio