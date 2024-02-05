import sqlite3
import random

calendar = [
    [],
    ["league", 1, 1],
    ["league", 2, 2],
    ["EU", 1],
    ["league", 3, 3],
    ["cup", 1],
    ["league", 4, 4],
    ["EU", 2],
    ["league", 5, 5],
    ["league", False, 6],
    ["league", 6, 7],
    ["EU", 3],
    ["league", 7, 8],
    ["league", 8, 9],
    ["EU", 4],
    ["league", 9, 10],
    ["league", False, 11],
    ["league", 10, 12],
    ["EU", 5],
    ["league", 11, 13],
    ["cup", 2],
    ["league", 12, 14],
    ["EU", 6],
    ["league", 13, 15],
    ["league", False, 16],
    ["league", 14, 17],
    ["EU", 7],
    ["league", 15, 18],
    ["league", 16, 19],
    ["EU", 8],
    ["league", 17, 20],
    ["cup", 3],
    ["league", 18, 21],
    ["league", False, 22],
    ["league", 19, 23],
    ["EU", 9],
    ["league", 20, 24],
    ["EU", 10],
    ["league", 21, 25],
    ["league", 22, 26],
    ["cup", 4],
    ["league", 23, 27],
    ["EU", 11],
    ["league", 24, 28],
    ["league", False, 29],
    ["league", 25, 30],
    ["EU", 12],
    ["league", 26, 31],
    ["league", 27, 32],
    ["EU", 13],
    ["league", 28, 33],
    ["league", False, 34],
    ["league", 29, 35],
    ["cup", 5],
    ["league", 30, 36],
    ["EU", 14],
    ["league", 31, 37],
    ["league", 32, 38],
    ["league", False, 39],
    ["league", 33, 40],
    ["EU", 15],
    ["league", 34, 41],
    ["league", 35, 42],
    ["EU", 16],
    ["league", 36, 43],
    ["cup", 6],
    ["league", 37, 44],
    ["league", False, 45],
    ["league", 38, 46],
    ["league", False, 47],
    ["league", False, 48],
    ["cup", 7],
    ["league", False, 49],
    ["EU", 17],
    ["end", "of", "the season"]
]
ENG1 = [
    ("Manchester City", "4-2-4",88,83,86,87, 100, 100, 2,1,1,3,2,2,1, 1,1, 'ENG', 258, '#6CABDD', '#FFFFFF', 89),
    ("Liverpool", "4-2-4",89,84,82,84, 100, 100, 1,2,1,3,2,2,1, 1,1, 'ENG', 173.32, '#c8102E', '#FFFFFF', 88),
    ("Arsenal", "4-4-2",84,81,84,82, 100, 100, 2,2,1,3,1,1,2, 1,1, 'ENG', 222, '#EF0107', '#FFFFFF', 85),
    ("Manchester United", "4-3-3",85,80,83,82, 100, 100, 4,2,3,1,1,1,1, 1,1, 'ENG', 159.05, '#DA291C', '#FFFFFF', 83),
    ("Tottenham", "5-2-3",83,79,80,81, 100, 100, 3,3,1,1,2,2,1, 1,1, 'ENG', 150.96, '#FFFFFF', '#132257', 82),
    ("Newcastle", "3-4-3",84,82,81,79, 100, 100, 2,3,2,1,5,2,1, 1,1, 'ENG', 128.14, '#241F20', '#FFFFFF', 83),
    ("Aston Villa", "5-3-2",85,79,79,82, 100, 100, 4,2,3,1,2,1,2, 1,1, 'ENG', 127.7, '#95bfe5', '#670e36', 81),
    ("Chelsea", "3-4-3",79,78,81,77, 100, 100, 3,1,2,2,1,1,2, 1,1, 'ENG', 196.76, '#034694', '#FFFFFF', 80),
    ("West Ham", "4-5-1",79,78,79,78, 100, 100, 3,3,1,2,2,1,1, 1,1, 'ENG', 92.42, '#7A263A', '#F3D459', 79),
    ("Everton", "3-5-2",82,75,77,79, 100, 100, 5,1,2,2,2,1,2, 1,1, 'ENG', 67.38, '#003399', '#FFFFFF', 77),
    ("Brighton", "5-2-3",75,78,77,77, 100, 100,  4,1,3,1,2,1,2, 1,1, 'ENG', 97.62, '#0057B8', '#FFFFFF', 78),
    ("Fulham", "5-4-1",81,76,77,76, 100, 100, 4,2,2,1,2,1,1, 1,1, 'ENG', 62.9, '#FFFFFF', '#000000', 77),
    ("Nottingham Forest", "3-4-3",81,75,77,75, 100, 100, 3,2,2,3,2,1,2, 1,1, 'ENG', 79.29, '#DD0000', '#FFFFFF', 76),
    ("Wolverhampton", "4-2-4",79,76,77,75, 100, 100, 2,1,2,1,1,1,1, 1,1, 'ENG', 67.4, '#FDB913', '#231F20', 75),
    ("Brentford", "3-5-2",82,76,76,75, 100, 100, 5,3,1,1,1,1,1, 1,1, 'ENG', 79.02, '#e30613', '#FFFFFF', 76),
    ("Crystal Palace", "4-3-3",79,76,76,75, 100, 100, 3,2,1,2,2,2,2, 1,1, 'ENG', 73.54, '#1B458F', '#C4122E', 76),
    ("Bournemouth", "3-4-3",78,74,75,75, 100, 100, 2,1,2,2,1,1,1, 1,1, 'ENG', 67.02, '#B50E12', '#FFFFFF', 75),
    ("Burnley", "3-4-3",75,73,74,69, 100, 100, 4,1,3,1,1,1,1, 1,1, 'ENG', 50.53, '#6C1D45', '#FFFF00', 74),
    ("Sheffield United", "5-3-2",75,72,74,72, 100, 100, 5,2,3,3,1,2,2, 1,1, 'ENG', 28.97, '#EE2737', '#FFFFFF', 73),
    ("Luton", "4-3-3",73,72,72,72, 100, 100, 2,3,1,2,2,1,2, 1,1, 'ENG', 20.68, '#F78F1E', '#FFFFFF', 72)
]

ENG2 = [
    ("Leicester", "3-3-4",74,75,76,73, 100, 100, 1,1,3,1,2,1,1, 1,2, 'ENG', 47.77, '#003090', '#ffffff', 75),
    ("Ipswich", "3-5-2",68,69,69,68, 100, 100, 4,1,1,1,2,2,1, 1,2, 'ENG', 7.47, '#3a64a3', '#FEFEFE', 69),
    ("Southampton", "5-3-2",72,74,70,71, 100, 100, 5,1,2,3,2,2,1, 1,2, 'ENG', 40.52, '#d71920', '#ffffff', 73),
    ("Leeds", "3-5-2",76,72,72,72, 100, 100, 3,2,1,2,2,1,1, 1,2, 'ENG', 41.24, '#FFCD00', '#1D428A', 73),
    ("West Brom", "3-3-4",69,70,72,70, 100, 100, 1,1,3,1,2,1,2, 1,2, 'ENG', 10.98, '#FFFFFF', '#060067', 72),
    ("Sunderland", "4-3-3",71,69,69,57, 100, 100, 4,2,2,3,2,1,2, 1,2, 'ENG', 16.07, '#eb172b', '#000000', 70),
    ("Hull City", "4-4-2",68,70,71,69, 100, 100, 3,2,3,1,1,1,2, 1,2, 'ENG', 14.92, '#f5971d', '#000000', 70),
    ("Bristol City", "4-3-3",69,69,70,66, 100, 100, 3,1,2,3,2,1,2, 1,2, 'ENG', 7.52, '#E21F29', '#ffffff', 70),
    ("Preston North End", "3-4-3",74,68,70,70, 100, 100, 4,3,3,3,2,1,2, 1,2, 'ENG', 8.3, '#002156', '#ffffff', 70),
    ("Watford", "3-5-2",72,69,71,70, 100, 100, 1,1,1,2,2,2,1, 1,2, 'ENG', 12.93, '#FBEE23', '#000000', 72),
    ("Cardiff City", "4-4-2",73,68,70,70, 100, 100, 2,1,3,3,1,1,2, 1,2, 'ENG', 8.93, '#2b58ae', '#ffffff', 71),
    ("Norwich City", "3-4-3",74,71,72,70, 100, 100, 5,2,3,1,2,1,2, 1,2, 'ENG', 14, '#00a650', '#ffee00', 72),
    ("Coventry City", "4-4-2",69,70,71,71, 100, 100, 2,3,1,1,1,1,2, 1,2, 'ENG', 10.98, '#77bbff', '#ffffff', 72),
    ("Middlesbrough", "3-3-4",71,71,70,69, 100, 100, 3,1,1,3,1,1,1, 1,2, 'ENG', 13.45, '#FFFFFF', '#e11b22', 72),
    ("Blackburn Rovers", "4-5-1",68,70,69,70, 100, 100, 2,2,1,3,1,1,1, 1,2, 'ENG', 12.36, '#78bcff', '#ffed00', 71),
    ("Plymouth Argyle", "4-2-4",71,67,67,67, 100, 100, 4,1,3,3,2,2,2, 1,2, 'ENG', 5.26, '#004f3e', '#ffffff', 68),
    ("Swansea City", "4-3-3",68,67,70,70, 100, 100, 2,3,3,2,2,2,2, 1,2, 'ENG', 13.04, '#FFFFFF', '#000000', 71),
    ("Stoke City", "4-2-4",73,69,70,71, 100, 100, 4,3,3,1,2,2,2, 1,2, 'ENG', 9.81, '#e03a3e', '#ffffff', 71),
    ("Birmingham City", "3-5-2",71,69,69,69, 100, 100, 1,1,1,2,2,1,1, 1,2, 'ENG', 9.38, '#103bce', '#FFFFFF', 70),
    ("Millwall", "5-4-1",68,70,71,72, 100, 100, 1,1,3,2,1,1,1, 1,2, 'ENG', 8.26, '#00194A', '#ffffff', 71),
    ("Rotherham United", "3-3-4",71,65,68,67, 100, 100, 4,2,3,1,2,2,2, 1,2, 'ENG', 3.53, '#e21d25', '#000000', 69),
    ("Huddersfield", "3-4-3",74,67,66,68, 100, 100, 3,1,1,3,1,1,2, 1,2, 'ENG', 5.85, '#0E63AD', '#ffffff', 68),
    ("Sheffield Wednesday", "5-4-1",71,67,69,68, 100, 100, 5,2,1,3,2,2,1, 1,2, 'ENG', 3.21, '#0e62aa', '#ffffff', 69),
    ("QPR", "5-3-2",74,69,68,67, 100, 100, 1,3,1,3,1,1,2, 1,2, 'ENG', 6.18, '#FFFFFF', '#1d5ba4', 69)
]

# Dodajemy przykładowe drużyny#0nazwa, 1formacja, 2sila_bramkarza, 3sila_obrony, 4sila_pomocy, 5sila_napadu, 6zaangazowanie,
#7sila_trenera, 1nastawienie, 2dlugosc_podan, 3pressing, 4wslizgi, 5krycie, 6kontry, 7pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, color1, color2, sila podst

ENG3 = [
    ("Derby County", "5-4-1",68,67,66,66, 100, 100, 4,3,1,3,1,1,2, 1,3, 'ENG', 3.04, '#ffffff', '#000000', 68),
    ("Bolton Wanderers", "3-5-2",69,65,65,67, 100, 100, 3,3,1,1,1,2,1, 1,3, 'ENG', 2.04, '#ffffff', '#263c7e', 67),
    ("Blackpool", "3-4-3",66,66,65,66, 100, 100, 4,2,1,1,2,1,2, 1,3, 'ENG', 2.73, '#FF8C00', '#ffffff', 67),
    ("Barnsley", "4-5-1",65,65,65,65, 100, 100, 1,2,2,3,2,2,2, 1,3, 'ENG', 2.37, '#d71921', '#ffffff', 66),
    ("Charlton Athletic", "5-4-1",66,65,66,62, 100, 100, 3,1,1,1,2,1,1, 1,3, 'ENG', 2.45, '#D6011D', '#FFFFFF', 66),
    ("Reading", "4-2-4",67,64,65,59, 100, 100, 4,2,1,1,1,2,2, 1,3, 'ENG', 2.74, '#0000FF', '#FFFFFF', 66),
    ("Peterborough", "4-3-3",60,65,65,71, 100, 100, 4,1,2,3,1,1,1, 1,3, 'ENG', 3.18, '#338AD6', '#FAF7F7', 66),
    ("Portsmouth", "3-3-4",65,66,64,70, 100, 100, 5,2,1,1,1,2,2, 1,3, 'ENG', 2.23, '#0754ED', '#ffffff', 66),
    ("Wigan Athletic", "4-2-4",66,64,63,67, 100, 100, 4,3,2,2,2,2,2, 1,3, 'ENG', 2.03, '#ffffff', '#1d59af', 66),
    ("Oxford United", "5-3-2",64,65,65,65, 100, 100, 4,2,3,3,1,1,2, 1,3, 'ENG', 1.75, '#FFFF00', '#0000FF', 65),
    ("Wycombe Wanderers", "4-5-1",69,64,66,64, 100, 100, 5,1,1,3,2,1,1, 1,3, 'ENG', 1.34, '#0099FF', '#003399', 65),
    ("Bristol Rovers", "3-4-3",63,63,65,65, 100, 100, 4,2,1,3,1,1,2, 1,3, 'ENG', 1.85, '#0000FF', '#FFFFFF', 65),
    ("Burton Albion", "4-4-2",66,64,64,64, 100, 100, 5,1,1,2,1,2,2, 1,3, 'ENG', 1.1, '#FFFF00', '#000000', 65),
    ("Lincoln City", "4-4-2",64,64,64,64, 100, 100,  3,1,3,3,2,2,2, 1,3, 'ENG', 1.63, '#FF0000', '#FFFFFF', 65),
    ("Leyton Orient", "4-4-2",64,63,64,64, 100, 100, 2,1,3,2,2,2,2, 1,3, 'ENG', 1.17, '#ed2227', '#ffffff', 65),
    ("Shrewsbury Town", "4-2-4",67,63,63,64, 100, 100, 5,1,3,1,1,1,2, 1,3, 'ENG', 1.26, '#0e2240', '#ffffff', 64),
    ("Fleetwood Town", "3-5-2",66,65,63,63, 100, 100, 1,3,3,2,2,2,2, 1,3, 'ENG', 1.62, '#FF0000', '#FFFFFF', 64),
    ("Cambridge United", "4-2-4",63,64,63,63, 100, 100, 3,1,3,2,2,1,1, 1,3, 'ENG', 1.14, '#F0D313', '#0F0303', 64),
    ("Northampton Town", "3-4-3",64,63,64,65, 100, 100, 5,3,2,3,1,1,2, 1,3, 'ENG', 1.11, '#990000', '#ffffff', 64),
    ("Exeter City", "4-2-4",60,63,63,63, 100, 100, 1,3,2,2,2,2,2, 1,3, 'ENG', 1.69, '#FF0000', '#ffffff', 64),
    ("Cheltenham Town", "4-3-3",66,63,62,63, 100, 100, 3,3,3,2,1,2,2, 1,3, 'ENG', 0.91, '#FF0000', '#ffffff', 64),
    ("Stevenage", "4-3-3",64,63,64,62, 100, 100, 4,1,2,1,1,2,2, 1,3, 'ENG', 1.28, '#FF0000', '#ffffff', 64),
    ("Carlisle United", "4-2-4",63,63,64,62, 100, 100, 1,3,3,2,2,1,1, 1,3, 'ENG', 1.36, '#1F47BF', '#ffffff', 64),
    ("Port Vale", "3-4-3",66,64,63,62, 100, 100, 5,1,3,1,2,2,2, 1,3, 'ENG', 1.27, '#ffffff', '#000000', 64)
]

ENG4 = [
    ("Wrexham", "4-3-3",66,65,64,65, 100, 100, 4,2,2,1,1,2,1, 1,4, "ENG", 1.37, "#ffffff", "#000000", 64),
    ("MK Dons", "4-5-1",65,63,63,65, 100, 100, 4,2,1,3,2,2,2, 1,4, "ENG", 1.22, "#ffffff", "#000000", 64),
    ("Stockport County", "4-4-2",64,63,65,63, 100, 100, 4,1,2,2,1,1,2, 1,4, "ENG", 1.34, "#1e5593", "#ffffff", 64),
    ("Gillingham", "4-3-3",62,63,64,63, 100, 100, 4,1,2,2,2,1,2, 1,4, "ENG", 0.89, "#0000FF", "#ffffff", 63),
    ("Salford City", "3-5-2",63,64,63,63, 100, 100, 2,1,1,3,2,2,2, 1,4, "ENG", 0.93, "#000000", "#ffffff", 63),
    ("Bradford City", "5-2-3",65,61,63,63, 100, 100, 3,3,1,3,1,1,2, 1,4, "ENG", 0.97, "#990033", "#FF9900", 63),
    ("Mansfield Town", "3-4-3",61,63,63,62, 100, 100, 4,2,1,3,2,2,2, 1,4, "ENG", 0.95, "#F5B803", "#1B48B8", 63),
    ("Forest GR", "4-5-1",65,64,61,62, 100, 100, 2,1,1,3,1,1,2, 1,4, "ENG", 1.26, "#4CBA02", "#030303", 63),
    ("Notts County", "3-4-3",62,60,63,66, 100, 100, 2,3,1,1,1,1,2, 1,4, "ENG", 0.88, "#ffffff", "#000000", 62),
    ("Harrogate Town", "5-2-3",59,62,60,64, 100, 100, 2,3,1,3,2,1,1, 1,4, "ENG", 0.76, "#0F0C06", "#FFE819", 62),
    ("Grimsby Town", "4-3-3",60,62,62,63, 100, 100, 2,3,2,1,1,2,2, 1,4, "ENG", 0.99, "#ffffff", "#000000", 62),
    ("Swindon Town", "4-5-1",60,62,62,62, 100, 100, 1,1,2,3,2,2,2, 1,4, "ENG", 0.77, "#FF0000", "#ffffff", 62),
    ("AFC Wimbledon", "3-4-3",64,60,62,62, 100, 100, 1,3,3,3,2,2,2, 1,4, "ENG", 0.84, "#0000FF", "#FFFF00", 62),
    ("Walsall", "4-2-4",63,62,61,62, 100, 100, 3,1,3,3,2,2,2, 1,4, "ENG", 0.84, "#E20B1E", "#ffffff", 62),
    ("Barrow", "4-5-1",61,61,61,61, 100, 100, 2,1,1,3,2,2,2, 1,4, "ENG", 0.85, "#223D7D", "#ffffff", 62),
    ("Colchester United", "5-4-1",61,61,62,58, 100, 100, 1,1,1,3,2,1,1, 1,4, "ENG", 1.18, "#438BF7", "#ffffff", 62),
    ("Tranmere Rovers", "4-2-4",62,61,61,62, 100, 100, 1,1,1,3,2,2,2, 1,4, "ENG", 0.79, "#ffffff", "#084BF5", 61),
    ("Doncaster Rovers", "3-4-3",61,61,60,62, 100, 100, 3,2,3,2,2,1,2, 1,4, "ENG", 1.08, "#FF0000", "#000000", 61),
    ("Sutton United", "3-3-4",63,62,61,61, 100, 100, 2,2,2,1,1,2,2, 1,4, "ENG", 0.68, "#fdbe00", "#673200", 61),
    ("Accrington Stanley", "4-2-4",61,59,62,59, 100, 100, 2,1,3,2,2,1,1, 1,4, "ENG", 0.83, "#FF0000", "#000000", 61),
    ("Crewe Alexandra", "4-3-3",58,61,61,62, 100, 100, 3,3,2,1,1,1,2, 1,4, "ENG", 1.07, "#ffffff", "#FF0000", 60),
    ("Newport County", "4-3-3",60,60,60,61, 100, 100, 2,3,1,1,1,1,1, 1,4, "ENG", 0.78, "#EBA10C", "#000000", 60),
    ("Crawley Town", "5-4-1",58,60,60,58, 100, 100, 1,2,3,2,2,2,2, 1,4, "ENG", 0.69, "#FC0000", "#000000", 60),
    ("Morecambe", "3-4-3",60,61,60,57, 100, 100, 2,1,3,3,2,1,1, 1,4, "ENG", 0.84, "#FF0000", "#000000", 60)
]

EU = [
    ("Manchester City", "4-2-4",88,83,86,87, 100, 100, 2,1,1,3,2,2,1, 1,1, 'ENG', 258, '#6CABDD', '#FFFFFF', 89),
    ("Manchester United", "4-3-3",85,80,83,82, 100, 100, 4,2,3,1,1,1,1, 1,1, 'ENG', 159.05, '#DA291C', '#FFFFFF', 83),
    ("Arsenal", "4-4-2",84,81,84,82, 100, 100, 2,2,1,3,1,1,2, 1,1, 'ENG', 222, '#EF0107', '#FFFFFF', 85),
    ("Newcastle", "3-4-3",84,82,81,79, 100, 100, 2,3,2,1,5,2,1, 1,1, 'ENG', 128.14, '#241F20', '#FFFFFF', 83),
    ("Sevilla", "3-4-3",82,82,79,80, 100, 100, 4,3,3,2,1,2,1, 1,1, "SPA", 0, "#FF0000", "#ffffff", 80),
    ("Atletico Madrid", "4-5-1",81,81,82,85, 100, 100, 1,2,2,2,2,2,1, 1,1, "SPA", 0, "#CF321F", "#ffffff", 83),
    ("Barcelona", "5-4-1",83,83,84,84, 100, 100, 4,2,1,2,2,1,2, 1,1, "SPA", 0, "#004C99", "#A60042", 84),
    ("Real Madrid", "4-5-1",83,83,85,85, 100, 100, 3,2,2,3,1,1,1, 1,1, "SPA", 0, "#ffffff", "#004996", 85),
    ("Milan", "5-3-2",81,81,79,81, 100, 100, 5,1,1,2,2,2,1, 1,1, "ITA", 0, "#B50909", "#050505", 80),
    ("Inter", "3-3-4",82,82,83,81, 100, 100, 5,3,3,1,2,1,1, 1,1, "ITA", 0, "#000000", "#0055A0", 82),
    ("Lazio", "3-4-3",80,80,79,81, 100, 100, 3,2,1,1,2,2,2, 1,1, "ITA", 0, "#DCECF2", "#ffffff", 80),
    ("Napoli", "5-3-2",80,80,82,82, 100, 100, 3,2,1,1,2,2,2, 1,1, "ITA", 0, "#0080FF", "#ffffff", 81),
    ("Union Berlin", "3-4-3",77,77,75,74, 100, 100, 4,3,3,1,2,1,2, 1,1, "GER", 0, "#E40019", "#ffffff", 77),
    ("Bayern", "3-5-2",83,83,84,90, 100, 100, 4,3,1,1,1,2,1, 1,1, "GER", 0, "#DB072D", "#ffffff", 84),
    ("Borussia Dortmund", "5-3-2",81,81,81,81, 100, 100, 4,1,3,3,2,2,2, 1,1, "GER", 0, "#FDF105", "#000000", 81),
    ("RB Leipzig", "5-2-3",79,79,80,80, 100, 100, 5,2,2,2,2,2,2, 1,1, "GER", 0, "#dd0741", "#001f47", 80),
    ("Lens", "5-4-1",77,77,75,77, 100, 100, 5,2,1,2,1,2,1, 1,1, "FRA", 0, "#FFDF00", "#F50505", 77),
    ("PSG", "4-5-1",83,83,79,86, 100, 100, 5,1,3,1,1,1,2, 1,1, "FRA", 0, "#00093F", "#ffffff", 83),
    ("Marseille", "5-4-1",78,78,78,77, 100, 100, 4,1,1,2,2,2,2, 1,1, "FRA", 0, "#ffffff", "#099FFF", 78),
    ("Real Sociedad", "4-3-3",79,79,81,79, 100, 100, 4,2,1,1,2,2,1, 1,1, "SPA", 0, "#0000FF", "#ffffff", 79),
    ("Antwerp", "4-4-2",73,73,72,76, 100, 100, 2,1,3,3,2,1,2, 1,1, "OTH", 0, "#ffffff", "#FF0000", 73),
    ("Benfica", "4-4-2",79,79,80,80, 100, 100, 2,3,2,2,2,1,2, 1,1, "OTH", 0, "#FF0000", "#ffffff", 79),
    ("Braga", "3-3-4",75,75,77,77, 100, 100, 3,3,1,1,2,2,1, 1,1, "OTH", 0, "#E80C0C", "#ffffff", 76),
    ("Celtic", "5-3-2",71,71,75,74, 100, 100, 1,2,2,2,1,2,2, 1,1, "OTH", 0, "#009933", "#ffffff", 74),
    ("Crvena zvezda", "3-3-4",73,73,74,73, 100, 100, 3,1,1,2,1,1,2, 1,1, "OTH", 0, "#F50C0C", "#ffffff", 73),
    ("Feyenoord", "3-4-3",77,77,74,76, 100, 100, 5,3,2,3,1,1,2, 1,1, "OTH", 0, "#FF0808", "#ffffff", 76),
    ("Galatasaray", "4-5-1",77,77,79,80, 100, 100, 4,2,2,3,2,1,1, 1,1, "OTH", 0, "#FFAE00", "#FF0000", 78),
    ("Salzburg", "5-4-1",71,71,73,69, 100, 100, 4,2,1,2,2,1,2, 1,1, "OTH", 0, "#E41349", "#ffffff", 73),
    ("Shakhtar Donetsk", "3-4-3",70,70,71,74, 100, 100, 2,3,3,3,2,2,2, 1,1, "OTH", 0, "#FF6600", "#000000", 71),
    ("Young Boys", "4-3-3",69,69,69,74, 100, 100, 5,2,3,1,2,2,1, 1,1, "OTH", 0, "#FFD940", "#000000", 71),
    ("Copenhagen", "4-5-1",72,72,74,69, 100, 100, 2,2,3,3,2,1,2, 1,1, "OTH", 0, "#0C09D9", "#ffffff", 72),
    ("FC Porto", "5-2-3",77,77,78,78, 100, 100, 1,2,1,2,1,2,2, 1,1, "OTH", 0, "#0037EB", "#ffffff", 78),
    ("PSV", "4-4-2",75,75,74,78, 100, 100, 1,1,2,2,2,2,2, 1,1, "OTH", 0, "#ED1C23", "#ffffff", 76),
    ("Dinamo Zagreb", "5-2-3",71,71,72,70, 100, 100, 4,2,2,3,1,1,2, 1,1, "OTH", 0, "#1C388C", "#E32118", 71),
    ("AEK Athens", "5-4-1",74,74,75,76, 100, 100, 5,2,1,3,2,2,2, 1,1, "OTH", 0, "#FFFF00", "#000000", 75),
    ("Slavia Praha", "4-2-4",74,74,74,71, 100, 100, 1,2,3,3,2,1,2, 1,1, "OTH", 0, "#B80707", "#ffffff", 73), # CL teams
    ("Liverpool", "4-2-4",89,84,82,84, 100, 100, 1,2,1,3,2,2,1, 1,2, 'ENG', 173.32, '#c8102E', '#FFFFFF', 88),
    ("Aston Villa", "5-3-2",85,79,79,82, 100, 100, 4,2,3,1,2,1,2, 1,2, 'ENG', 127.7, '#95bfe5', '#670e36', 81),
    ("Brighton", "5-2-3",75,78,77,77, 100, 100,  4,1,3,1,2,1,2, 1,2, 'ENG', 97.62, '#0057B8', '#FFFFFF', 78),
    ("Real Betis", "4-5-1",77,77,79,83, 100, 100, 2,3,3,1,1,1,1, 1,2, "SPA", 0, "#00954C", "#ffffff", 79),
    ("Villarreal", "3-3-4",77,77,80,79, 100, 100, 2,1,2,1,1,2,1, 1,2, "SPA", 0, "#FFFF00", "#0073FF", 79),
    ("Osasuna", "5-2-3",77,77,77,77, 100, 100, 5,3,1,2,2,2,2, 1,2, "SPA", 0, "#d91a21", "#0a346f", 77),
    ("Roma", "5-4-1",81,81,78,82, 100, 100, 4,3,1,3,1,1,2, 1,2, "ITA", 0, "#FFB22E", "#9E142B", 80),
    ("Atalanta", "5-4-1",77,77,77,79, 100, 100, 3,3,1,2,1,2,1, 1,2, "ITA", 0, "#295CB0", "#000000", 78),
    ("Juventus", "4-5-1",79,79,80,81, 100, 100, 5,2,1,3,1,1,1, 1,2, "ITA", 0, "#ffffff", "#000000", 80),
    ("Freiburg", "3-4-3",77,77,76,76, 100, 100, 4,1,3,1,2,2,1, 1,2, "GER", 0, "#ffffff", "#000000", 76),
    ("Leverkusen", "4-3-3",79,79,81,81, 100, 100, 2,3,1,1,2,1,1, 1,2, "GER", 0, "#FF0000", "#000000", 80),
    ("Eintracht Frankfurt", "3-5-2",76,76,76,76, 100, 100, 1,1,1,3,1,2,1, 1,2, "GER", 0, "#FF0000", "#000000", 76),
    ("Rennes", "4-4-2",74,74,78,77, 100, 100, 5,1,1,1,1,2,2, 1,2, "FRA", 0, "#E13327", "#ffffff", 76),
    ("Toulouse", "5-4-1",72,72,71,75, 100, 100, 4,3,1,3,1,2,2, 1,2, "FRA", 0, "#8D42D4", "#ffffff", 72),
    ("Sparta Praha", "5-2-3",74,74,73,73, 100, 100, 2,2,1,1,2,1,1, 1,2, "OTH", 0, "#B31616", "#ffffff", 73),
    ("West Ham", "4-5-1",79,78,79,78, 100, 100, 3,3,1,2,2,1,1, 1,2, 'ENG', 92.42, '#7A263A', '#F3D459', 79),
    ("Rangers", "4-2-4",74,74,74,72, 100, 100, 3,2,2,2,1,2,2, 1,2, "OTH", 0, "#0000FF", "#ffffff", 73),
    ("Quarabag", "5-2-3",67,67,69,66, 100, 100, 4,2,3,3,2,2,1, 1,2, "OTH", 0, "#000000", "#ffffff", 67),
    ("Sporting CP", "5-2-3",78,78,77,78, 100, 100, 2,1,1,1,1,1,2, 1,2, "OTH", 0, "#008056", "#ffffff", 77),
    ("Ajax", "3-4-3",74,74,75,75, 100, 100, 4,3,2,2,2,1,1, 1,2, "OTH", 0, "#FF0000", "#ffffff", 75),
    ("Aris Limassol", "4-5-1",65,65,67,66, 100, 100, 1,3,3,3,1,2,2, 1,2, "OTH", 0, "#368944", "#ffffff", 66),
    ("Hacken", "5-2-3",68,68,70,66, 100, 100, 3,2,2,1,2,1,2, 1,2, "OTH", 0, "#1b1819", "#a79448", 69),
    ("LASK", "4-2-4",69,69,69,68, 100, 100, 2,3,1,3,1,2,2, 1,2, "OTH", 0, "#000000", "#ffffff", 69),
    ("Maccabi Haifa", "5-3-2",69,69,69,71, 100, 100, 5,3,2,2,1,1,2, 1,2, "OTH", 0, "#14A11D", "#ffffff", 70),
    ("Molde", "3-5-2",67,67,68,69, 100, 100, 2,1,1,2,1,1,1, 1,2, "OTH", 0, "#3366FF", "#ffffff", 68),
    ("Olympiacos", "4-5-1",75,75,76,76, 100, 100, 1,2,1,3,1,1,2, 1,2, "OTH", 0, "##FF0000", "#ffffff", 76),
    ("Panathinaikos", "4-5-1",74,75,72,74, 100, 100, 2,1,1,3,2,2,1, 1,2, "OTH", 0, "##007840", "#ffffff", 74),
    ("Rakow", "3-4-3",67,67,69,69, 100, 100, 5,2,2,2,2,2,1, 1,2, "OTH", 0, "#C70000", "#ffffff", 69),
    ("Servette", "4-4-2",67,67,70,69, 100, 100, 5,3,2,1,2,1,1, 1,2, "OTH", 0, "#870E26", "#ffffff", 68),
    ("Sheriff", "3-3-4",66,66,68,70, 100, 100, 1,1,3,1,2,2,2, 1,2, "OTH", 0, "#FFFF00", "#000000", 69),
    ("Sturm Graz", "5-2-3",70,70,71,69, 100, 100, 3,2,3,2,2,1,2, 1,2, "OTH", 0, "#000000", "#ffffff", 70),
    ("TSC Backa Topola", "5-3-2",68,68,71,70, 100, 100, 3,1,1,2,2,2,2, 1,2, "OTH", 0, "#0C00BA", "#38EB38", 69),
    ("Union SG", "4-4-2",71,71,70,68, 100, 100, 4,2,1,2,1,1,2, 1,2, "OTH", 0, "#20459D", "#F7EB37", 70),
    ("Cukaricki", "3-4-3",70,70,69,68, 100, 100, 5,2,1,3,2,1,2, 1,2, "OTH", 0, "#ffffff", "#000000", 69),
    ("Ludogorets", "3-4-3",72,72,71,74, 100, 100, 4,1,1,2,2,1,1, 1,2, "OTH", 0, "#006433", "#ffffff", 72),
    ("Girona", "4-4-2",76,76,76,77, 100, 100, 5,1,2,2,2,2,2, 1,0, "SPA", 0, "#FF0000", "#ffffff", 76),
    ("Athletic Bilbao", "3-4-3",77,77,79,77, 100, 100, 4,2,1,2,1,2,2, 1,0, "SPA", 0, "#FF0000", "#ffffff", 79),
    ("Valencia", "4-3-3",76,76,74,74, 100, 100, 5,1,1,1,1,1,1, 1,0, "SPA", 0, "#ffffff", "#000000", 75),
    ("Fiorentina", "3-4-3",78,78,77,78, 100, 100, 1,2,2,2,2,2,2, 1,0, "ITA", 0, "#5C2180", "#ffffff", 78),
    ("Bologna", "4-5-1",73,73,76,73, 100, 100, 1,2,3,1,2,2,2, 1,0, "ITA", 0, "#ED0909", "#483DEB", 74),
    ("Torino", "3-3-4",76,76,74,76, 100, 100, 3,1,3,2,2,1,2, 1,0, "ITA", 0, "#A62D2D", "#ffffff", 75),
    ("Stuttgart", "5-2-3",73,73,73,76, 100, 100, 4,2,3,2,1,2,2, 1,0, "GER", 0, "#ffffff", "#FF0000", 73),
    ("Wolfsburg", "5-4-1",75,75,78,76, 100, 100, 4,2,3,3,2,1,1, 1,0, "GER", 0, "#0C4011", "#ffffff", 77),
    ("Borussia Mönchengladbach", "5-3-2",75,75,76,74, 100, 100, 2,3,3,3,1,1,2, 1,0, "GER", 0, "#000000", "#ffffff", 76),
    ("OGC Nice", "3-3-4",75,75,76,77, 100, 100, 5,1,2,2,2,2,2, 1,0, "FRA", 0, "#000000", "#ffffff", 76),
    ("Monaco", "5-3-2",75,75,77,81, 100, 100, 1,2,2,2,1,2,1, 1,0, "FRA", 0, "#FF0000", "#ffffff", 77),
    ("LOSC", "4-5-1",75,75,75,77, 100, 100, 1,2,1,1,1,2,1, 1,0, "FRA", 0, "#F20505", "#ffffff", 76),
    ("KI Klaksvik", "3-3-4",62,62,62,63, 100, 100, 5,1,1,1,2,2,1, 1,2, "OTH", 0, "#094FA3", "#ffffff", 62),
    ("Aberdeen", "5-3-2",66,66,66,70, 100, 100, 2,1,3,3,1,1,2, 1,0, "OTH", 0, "#FF0000", "#000000", 67),
    ("Lugano", "4-2-4",64,64,69,69, 100, 100, 2,2,3,3,2,1,2, 1,0, "OTH", 0, "#000000", "#ffffff", 67),
    ("Olimpija Lubljana", "5-3-2",65,65,65,65, 100, 100, 3,1,3,1,2,2,2, 1,0, "OTH", 0, "#009933", "#ffffff", 65),
    ("Slovan Bratislava", "4-5-1",65,65,66,65, 100, 100, 5,1,2,3,1,1,2, 1,0, "OTH", 0, "#00A6FF", "#ffffff", 65),
    ("Zrinjski", "5-2-3",63,63,62,62, 100, 100, 4,3,3,2,1,1,2, 1,0, "OTH", 0, "#2B3885", "#ffffff", 62),
    ("Zorya Luhansk", "5-3-2",66,66,67,64, 100, 100, 2,2,2,1,2,1,2, 1,0, "OTH", 0, "#000000", "#ffffff", 66),
    ("Astana", "3-3-4",64,64,66,63, 100, 100, 4,3,1,2,1,2,1, 1,0, "OTH", 0, "#FFFF00", "#0000FF", 65),
    ("BATE Borisov", "3-4-3",61,61,62,62, 100, 100, 4,2,2,3,1,1,2, 1,0, "OTH", 0, "#233D92", "#FCDA06", 62),
    ("Dnipro-1", "3-4-3",67,67,71,71, 100, 100, 5,1,3,3,2,1,2, 1,0, "OTH", 0, "#00418E", "#ffffff", 69),
    ("Genk", "3-3-4",73,73,72,71, 100, 100, 2,3,1,2,1,1,1, 1,0, "OTH", 0, "#ffffff", "#0000FF", 73),
    ("Zalgiris Vilnius", "4-3-3",64,64,64,63, 100, 100, 5,3,1,3,2,1,1, 1,0, "OTH", 0, "#44A204", "#ffffff", 63),
    ("HJK", "4-3-3",65,65,65,63, 100, 100, 4,1,3,1,1,2,1, 1,0, "OTH", 0, "#ffffff", "#6CB6CC", 65),
    ("Ferencvaros", "5-4-1",70,70,71,71, 100, 100, 2,2,2,2,1,2,2, 1,0, "OTH", 0, "#006600", "#ffffff", 71),
    ("Flora Tallin", "4-2-4",61,61,61,61, 100, 100, 4,1,2,1,1,2,1, 1,0, "OTH", 0, "#009900", "#ffffff", 61),
    ("Dinamo Tbilisi", "4-5-1",62,62,61,62, 100, 100, 1,3,1,2,1,1,1, 1,0, "OTH", 0, "#321FFF", "#ffffff", 62),
    ("Club Brugge", "5-3-2",72,72,74,72, 100, 100, 2,3,2,1,2,1,2, 1,0, "OTH", 0, "#0000FF", "#000000", 74),
    ("Fenerbahce", "3-4-3",74,74,76,78, 100, 100, 1,2,2,2,2,2,1, 1,0, "OTH", 0, "#FFED00", "#002D72", 77),
    ("Maccabi Tel Aviv", "5-2-3",65,65,66,64, 100, 100, 4,1,2,2,2,1,1, 1,0, "OTH", 0, "#123163", "#FFFF00", 65),
    ("PAOK", "3-4-3",70,70,73,72, 100, 100, 3,1,1,2,2,1,2, 1,0, "OTH", 0, "#000000", "#ffffff", 72),
    ("Viktoria Plzen", "4-2-4",72,72,73,72, 100, 100, 5,1,1,3,1,2,2, 1,0, "OTH", 0, "#FF0000", "#0000FF", 73),
    ("Anderlecht", "5-2-3",71,71,74,73, 100, 100, 1,2,2,1,2,1,2, 1,0, "OTH", 0, "#ffffff", "#660099", 74),
    ("Legia", "3-3-4",67,67,69,68, 100, 100, 1,1,3,1,2,1,2, 1,0, "OTH", 0, "#ffffff", "#000000", 68),
    ("Ballkani", "3-5-2",61,61,61,63, 100, 100, 5,3,3,2,2,1,2, 1,0, "OTH", 0, "#FFFD07", "#000000", 62),
    ("AZ Alkmaar", "4-3-3",71,71,75,71, 100, 100, 5,3,3,3,2,1,1, 1,0, "OTH", 0, "#db0021", "#ffffff", 73),
    ("Breidablik", "4-5-1",60,60,61,61, 100, 100, 4,3,2,3,1,1,1, 1,0, "OTH", 0, "#CC0204", "#ffffff", 61),
    ("Nordsjælland", "4-2-4",68,68,68,69, 100, 100, 4,1,2,1,1,1,1, 1,0, "OTH", 0, "#e42223", "#fee813", 68),
    ("Levski", "3-4-3",69,69,68,69, 100, 100, 2,3,1,1,2,2,2, 1,0, "OTH", 0, "#216BFF", "#ffffff", 69),
    ("Farul Constanta", "4-2-4",68,68,69,68, 100, 100, 4,3,3,1,2,1,2, 1,0, "OTH", 0, "#0C3A7C", "#ffffff", 69),
    ("FCSB", "5-2-3",68,68,69,70, 100, 100, 5,1,1,1,2,2,1, 1,0, "OTH", 0, "#0000FF", "#FFFF00", 69),
    ("Hajduk Split", "4-3-3",70,70,70,77, 100, 100, 3,2,3,2,1,2,1, 1,0, "OTH", 0, "#21409a", "#ffffff", 71),
    ("Malmo FF", "4-5-1",66,66,69,70, 100, 100, 2,1,3,3,1,1,2, 1,0, "OTH", 0, "#81C0FF", "#ffffff", 70),
    ("APOEL", "4-4-2",66,66,69,70, 100, 100, 4,3,1,2,2,1,1, 1,0, "OTH", 0, "#2E3A90", "#F5BC21", 69)
]

kraje = [
    ("ENG", 1),
    ("ENG", 2),
    ("ENG", 3),
    ("ENG", 4)
]

def create_leagues(leagues):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.executemany('''
        INSERT INTO ligi (kraj, poziom_rozgrywkowy) VALUES (?, ?)
    ''', leagues)

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_teams(teams):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.executemany('''
        INSERT INTO druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', teams)

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_teams_eu(teams):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.executemany('''
        INSERT INTO eu_druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', teams)

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_schedule():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobieramy ilość lig
    cursor.execute("SELECT COUNT(DISTINCT poziom_rozgrywkowy) FROM druzyny WHERE kraj = 'ENG'")
    poziomy_rozgrywkowe = cursor.fetchone()

    for poziom_rozgrywkowy in range(1, poziomy_rozgrywkowe[0] + 1):
        # Pobieramy drużyny z bazy danych
        cursor.execute("SELECT nazwa FROM druzyny WHERE poziom_rozgrywkowy = ?", (poziom_rozgrywkowy,))
        teams = [row[0] for row in cursor.fetchall()]

        random.shuffle(teams)

        # Generujemy terminarz
        for kolejka in range(1, len(teams)):
            i1 = 0
            i2 = kolejka
            i2pocz = kolejka
            matches = []
            for mecze_w_kolejce in range(1, len(teams) // 2 + 1):
                if i1 < i2:
                    druzyny = [teams[i1], teams[i2]] if (kolejka % 2) == 0 else [teams[i2], teams[i1]]
                    matches.append(druzyny)
                else:
                    if i1 == i2:
                        i2 = len(teams) - 1
                        druzyny = [teams[i1], teams[i2]] if (kolejka % 2) == 0 else [teams[i2], teams[i1]]
                        matches.append(druzyny)
                        i1 = i2pocz
                    if i1 > i2:
                        i1 = i2pocz + 1
                        i2 = len(teams) - 2 if i1 != len(teams) - 2 else len(teams) - 1
                        druzyny = [teams[i1], teams[i2]] if (kolejka % 2) == 0 else [teams[i2], teams[i1]]
                        matches.append(druzyny)
                i1 += 1
                i2 -= 1
            # Wstawiamy mecze do bazy danych
            for match in matches:
                cursor.execute('''
                    INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
                ''', (match[0], match[1], '-', kolejka, poziom_rozgrywkowy))

                # Powtórzone mecze z zamienionymi rolami drużyn
                cursor.execute('''
                    INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
                ''', (match[1], match[0], '-', kolejka + len(teams) - 1, poziom_rozgrywkowy))

    # tworzymy 1 runde pucharu
    cursor.execute("""
        UPDATE druzyny
        SET cup_round = 1
    """)
    # Najlepsze druyny przenieś do 2 rundy
    cursor.execute("""
        UPDATE druzyny
        SET cup_round = 2
        WHERE nazwa IN (
            SELECT nazwa
            FROM druzyny
            ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC
            LIMIT 36
        )
    """)

    cursor.execute("SELECT nazwa FROM druzyny WHERE cup_round = 1")

    first_round_teams = cursor.fetchall()
    random.shuffle(first_round_teams)

    cup_games = int(len(first_round_teams)/2)

    for game in range(cup_games):
        t1_index = (game + 1) * 2 - 1
        t2_index = t1_index - 1
        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, 1, 1, "cup")
        ''', (first_round_teams[t1_index][0], first_round_teams[t2_index][0], '-',))

    # Liga mistrzow i liga europy
    cursor.execute("""
        UPDATE eu_druzyny
        SET cup_round = 1
    """)
    for i in range(1,3):
        cursor.execute("""
            SELECT nazwa
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu)
        """, (i,))

        eu_teams = cursor.fetchall()
        eu_games = int(len(eu_teams)/2)
        for game_eu in range(eu_games):
            t1_index = game_eu
            t2_index = len(eu_teams) - 1 - game_eu
            cursor.execute('''
                INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, 1, ?, "EU")
            ''', (eu_teams[t1_index][0], eu_teams[t2_index][0], '-', i,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_next_eu_group_stage_fixture(round):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for i in range(1,3):
        cursor.execute("""
            SELECT nazwa
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
        """, (i,))

        eu_teams = cursor.fetchall()

        eu_games = int(len(eu_teams)/2)
        for game_eu in range(eu_games):
            t1_index = (game_eu + 1) * 2 - 1
            t2_index = t1_index - 1
            cursor.execute('''
                INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
            ''', (eu_teams[t1_index][0], eu_teams[t2_index][0], '-', round, i,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_next_eu_round_fixture(round):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for poziom_rozgrywkowy in range(1,3):
        if round == 2:
            cursor.execute("""
                UPDATE eu_druzyny
                SET cup_round = 3
                WHERE nazwa IN (
                    SELECT nazwa
                    FROM eu_druzyny
                    WHERE poziom_rozgrywkowy = ?
                    ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                    LIMIT 8
                )
            """, (poziom_rozgrywkowy,))

            cursor.execute("""
                UPDATE eu_druzyny
                SET cup_round = 2
                WHERE nazwa IN (
                    SELECT nazwa
                    FROM eu_druzyny
                    WHERE poziom_rozgrywkowy = ?
                    ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                    LIMIT 16 OFFSET 8
                )
            """, (poziom_rozgrywkowy,))

            # Stworz runde 2
            cursor.execute("""
                SELECT nazwa
                FROM eu_druzyny
                WHERE poziom_rozgrywkowy = ? and cup_round = 2
                ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                LIMIT 8
            """, (poziom_rozgrywkowy,))

            top_round_2_teams = cursor.fetchall()
            random.shuffle(top_round_2_teams)

            cursor.execute("""
                SELECT nazwa
                FROM eu_druzyny
                WHERE poziom_rozgrywkowy = ? and cup_round = 2
                ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                LIMIT 8 OFFSET 8
            """, (poziom_rozgrywkowy,))

            bottom_round_2_teams = cursor.fetchall()
            random.shuffle(bottom_round_2_teams)

            for index, team in enumerate(top_round_2_teams):
                top_team = team[0]
                bottom_team = bottom_round_2_teams[index][0]
                cursor.execute('''
                    INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                ''', (bottom_team, top_team, '-', 9, poziom_rozgrywkowy,))
                cursor.execute('''
                    INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                ''', (top_team, bottom_team, '-', 10, poziom_rozgrywkowy,))

        elif round >= 3 and round <=6:
            arr_kolejka = [10,12,14,16]
            kolejka = arr_kolejka[round-3]

            cursor.execute("""
                SELECT druzyna_gospodarza, druzyna_gosci, wynik
                FROM mecze
                WHERE poziom_rozgrywkowy = ? and kolejka = ? AND rozgrywki = 'EU'
            """, (poziom_rozgrywkowy, kolejka,))

            matches = cursor.fetchall()

            for match in matches:
                t1 = match[0]
                t2 = match[1]
                wynik_t1m1, wynik_t2m1 = match[2].split('-')
                wynik_t1m1 = int(wynik_t1m1)
                wynik_t2m1 = int(wynik_t2m1)
                cursor.execute("""
                    SELECT druzyna_gospodarza, druzyna_gosci, wynik
                    FROM mecze
                    WHERE rozgrywki = 'EU' AND kolejka = ? AND druzyna_gospodarza = ? AND druzyna_gosci = ?
                """, ((kolejka - 1), t2, t1,))
                second_playoff_match = cursor.fetchone()
                wynik_t2m2, wynik_t1m2 = second_playoff_match[2].split('-')
                wynik_t2m2 = int(wynik_t2m2)
                wynik_t1m2 = int(wynik_t1m2)
                wynik_t1 = wynik_t1m1 + wynik_t1m2
                wynik_t2 = wynik_t2m1 + wynik_t2m2
                karne_byly = False
                karne = False
                if wynik_t1 > wynik_t2:
                    winner = t1
                elif wynik_t2 > wynik_t1:
                    winner = t2
                elif wynik_t1 == wynik_t2:
                    karne_byly = True
                    karne = random.choice([True, False])
                    if karne:
                        winner = t1
                    else:
                        winner = t2

                cursor.execute("""
                UPDATE eu_druzyny
                    SET cup_round = cup_round + 1
                    WHERE nazwa = ?
                """, (winner,))

                new_result = f"({wynik_t1}) {'p.' if karne_byly and karne else ''} {wynik_t1m1} - {wynik_t2m1} {'p.' if karne_byly and not karne else ''} ({wynik_t2})"

                cursor.execute("""
                    UPDATE mecze
                    SET wynik = ?
                    WHERE rozgrywki = 'EU' AND kolejka = ? AND druzyna_gospodarza = ? AND druzyna_gosci = ?
                """, (new_result, kolejka, t1, t2,))

            if round == 3:
                # Stworz runde 3
                cursor.execute("""
                    SELECT nazwa
                    FROM eu_druzyny
                    WHERE poziom_rozgrywkowy = ? and cup_round = 3
                    ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                    LIMIT 8
                """, (poziom_rozgrywkowy,))

                top_round_2_teams = cursor.fetchall()
                random.shuffle(top_round_2_teams)

                cursor.execute("""
                    SELECT nazwa
                    FROM eu_druzyny
                    WHERE poziom_rozgrywkowy = ? and cup_round = 3
                    ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                    LIMIT 8 OFFSET 8
                """, (poziom_rozgrywkowy,))

                bottom_round_2_teams = cursor.fetchall()
                random.shuffle(bottom_round_2_teams)

                for index, team in enumerate(top_round_2_teams):
                    top_team = team[0]
                    bottom_team = bottom_round_2_teams[index][0]
                    cursor.execute('''
                        INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                    ''', (bottom_team, top_team, '-', 11, poziom_rozgrywkowy,))
                    cursor.execute('''
                        INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                    ''', (top_team, bottom_team, '-', 12, poziom_rozgrywkowy,))
            else:
                cursor.execute("""
                    SELECT nazwa
                    FROM eu_druzyny
                    WHERE poziom_rozgrywkowy = ? and cup_round = ?
                """, (poziom_rozgrywkowy, round,))

                teams = cursor.fetchall()
                random.shuffle(teams)

                round_matches = int(len(teams)/2)

                for match in range(round_matches):
                    t1_index = (match + 1) * 2 - 1
                    t2_index = t1_index - 1
                    t1_r = teams[t1_index][0]
                    t2_r = teams[t2_index][0]
                    cursor.execute('''
                        INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                    ''', (t1_r, t2_r, '-', (kolejka + 1), poziom_rozgrywkowy))
                    if kolejka != 16:
                        cursor.execute('''
                            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "EU")
                        ''', (t2_r, t1_r, '-', (kolejka + 2), poziom_rozgrywkowy))

        elif round == 7:
            cursor.execute("""
                SELECT druzyna_gospodarza, druzyna_gosci, wynik
                FROM mecze
                WHERE poziom_rozgrywkowy = ? and kolejka = ? AND rozgrywki = 'EU'
            """, (poziom_rozgrywkowy, 17,))

            match = cursor.fetchone()

            t1 = match[0]
            t2 = match[1]
            wynik_t1, wynik_t2 = match[2].split('-')
            wynik_t1 = int(wynik_t1)
            wynik_t2 = int(wynik_t2)

            karne_byly = False
            karne = False

            if wynik_t1 > wynik_t2:
                winner = t1
            elif wynik_t2 > wynik_t1:
                winner = t2
            elif wynik_t1 == wynik_t2:
                karne_byly = True
                karne = random.choice([True, False])
                if karne:
                    winner = t1
                else:
                    winner = t2

            cursor.execute("""
            UPDATE eu_druzyny
                SET cup_round = cup_round + 1,
                basic_strength = basic_strength + 2
                WHERE nazwa = ?
            """, (winner,))

            new_result = f"{'p.' if karne_byly and karne else ''} {wynik_t1} - {wynik_t2} {'p.' if karne_byly and not karne else ''}"

            cursor.execute("""
                UPDATE mecze
                SET wynik = ?
                WHERE rozgrywki = 'EU' AND kolejka = ? AND druzyna_gospodarza = ? AND druzyna_gosci = ?
            """, (new_result, 17, t1, t2,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def cup_advane(wynik):
    if wynik['gospodarze']['gole'] > wynik['goscie']['gole']:
        winners = wynik['gospodarze']['nazwa']
    elif wynik['gospodarze']['gole'] < wynik['goscie']['gole']:
        winners = wynik['goscie']['nazwa']
    else:
        if wynik['gospodarze']['karne']:
            winners = wynik['gospodarze']['nazwa']
        elif wynik['goscie']['karne']:
            winners = wynik['goscie']['nazwa']

    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Resetowanie statystyk
    cursor.execute("""
        UPDATE druzyny SET
        cup_round = cup_round + 1
        WHERE nazwa = ?
    """, (winners,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_next_cup_round_schedule():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Wykonanie zapytania SQL, aby znaleźć największą wartość w kolumnie
    cursor.execute("SELECT MAX(cup_round) FROM druzyny")

    # Pobranie wyniku zapytania
    cup_round = cursor.fetchone()[0]

    cursor.execute("SELECT nazwa FROM druzyny WHERE cup_round = ?", (cup_round,))

    cup_round_teams = cursor.fetchall()
    if len(cup_round_teams) > 1:
        random.shuffle(cup_round_teams)

        cup_games = int(len(cup_round_teams)/2)

        for game in range(cup_games):
            t1_index = (game + 1) * 2 - 1
            t2_index = t1_index - 1
            cursor.execute('''
                INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, 1, "cup")
            ''', (cup_round_teams[t1_index][0], cup_round_teams[t2_index][0], '-', cup_round,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_playoffs():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for poziom_rozgrywkowy in range(2,5):
        if poziom_rozgrywkowy == 4:
            offset = 3
        else:
            offset = 2
        # Wykonanie zapytania SQL, aby znaleźć największą wartość w kolumnie
        cursor.execute("""
            SELECT nazwa
            FROM druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
            LIMIT 4 OFFSET ?
        """, (poziom_rozgrywkowy, offset,))

        playoffs_teams = cursor.fetchall()

        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
        ''', (playoffs_teams[3][0], playoffs_teams[0][0], '-', 47, poziom_rozgrywkowy,))
        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
        ''', (playoffs_teams[0][0], playoffs_teams[3][0], '-', 48, poziom_rozgrywkowy,))
        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
        ''', (playoffs_teams[2][0], playoffs_teams[1][0], '-', 47, poziom_rozgrywkowy,))
        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
        ''', (playoffs_teams[1][0], playoffs_teams[2][0], '-', 48, poziom_rozgrywkowy,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def create_playoffs_finals():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for poziom_rozgrywkowy in range(2,5):
        # Wykonanie zapytania SQL, aby znaleźć największą wartość w kolumnie
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci, wynik
            FROM mecze
            WHERE poziom_rozgrywkowy = ? AND kolejka = 47
        """, (poziom_rozgrywkowy,))

        first_playoff_matches = cursor.fetchall()

        finalists = []

        for match in first_playoff_matches:
            t1 = match[0]
            t2 = match[1]
            wynik_t1m1, wynik_t2m1 = match[2].split('-')
            wynik_t1m1 = int(wynik_t1m1)
            wynik_t2m1 = int(wynik_t2m1)
            cursor.execute("""
                SELECT druzyna_gospodarza, druzyna_gosci, wynik
                FROM mecze
                WHERE poziom_rozgrywkowy = ? AND kolejka = 48 AND druzyna_gospodarza = ? AND druzyna_gosci = ?
            """, (poziom_rozgrywkowy, match[1], match[0],))
            second_playoff_match = cursor.fetchone()
            wynik_t2m2, wynik_t1m2 = second_playoff_match[2].split('-')
            wynik_t2m2 = int(wynik_t2m2)
            wynik_t1m2 = int(wynik_t1m2)
            wynik_t1 = wynik_t1m1 + wynik_t1m2
            wynik_t2 = wynik_t2m1 + wynik_t2m2
            karne_byly = False
            karne = False
            if wynik_t1 > wynik_t2:
                winner = t1
            elif wynik_t2 > wynik_t1:
                winner = t2
            elif wynik_t1 == wynik_t2:
                karne_byly = True
                karne = random.choice([True, False])
                if karne:
                    winner = t1
                else:
                    winner = t2

            finalists.append(winner)

            new_result = f"({wynik_t2}) {'p.' if karne_byly and not karne else ''} {wynik_t2m2} - {wynik_t1m2} {'p.' if karne_byly and karne else ''} ({wynik_t1})"

            cursor.execute("""
                UPDATE mecze
                SET wynik = ?
                WHERE poziom_rozgrywkowy = ? AND kolejka = 48 AND druzyna_gospodarza = ? AND druzyna_gosci = ?
            """, (new_result, poziom_rozgrywkowy, match[1], match[0],))

        cursor.execute('''
            INSERT INTO mecze (druzyna_gospodarza, druzyna_gosci, wynik, kolejka, poziom_rozgrywkowy, rozgrywki) VALUES (?, ?, ?, ?, ?, "league")
        ''', (finalists[0], finalists[1], '-', 49, poziom_rozgrywkowy,))
        
    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def promote_playoffs_winners():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for poziom_rozgrywkowy in range(2,5):
        # Wykonanie zapytania SQL, aby znaleźć największą wartość w kolumnie
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci, wynik
            FROM mecze
            WHERE poziom_rozgrywkowy = ? AND kolejka = 49
        """, (poziom_rozgrywkowy,))

        playoffs_final = cursor.fetchone()

        t1 = playoffs_final[0]
        t2 = playoffs_final[1]

        wynik_t1, wynik_t2 = playoffs_final[2].split('-')
        wynik_t2 = int(wynik_t2)
        wynik_t1 = int(wynik_t1)

        if wynik_t1 > wynik_t2:
            winner = t1
        elif wynik_t2 > wynik_t1:
            winner = t2
        elif wynik_t1 == wynik_t2:
            karne = random.choice([True, False])
            if karne:
                winner = t1
            else:
                winner = t2

            new_result = f"{'p.' if winner == t1 else ''} {wynik_t1} - {wynik_t1} {'p.' if winner == t2 else ''}"

            cursor.execute("""
                UPDATE mecze
                SET wynik = ?
                WHERE poziom_rozgrywkowy = ? AND kolejka = 49 AND druzyna_gospodarza = ? AND druzyna_gosci = ?
            """, (new_result, poziom_rozgrywkowy, t1, t2,))

        cursor.execute("""
            UPDATE druzyny
            SET status_utrzymania = 'awans'
            WHERE nazwa = ?
        """, (winner,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def update_eu_cups():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Dodanie drużyn do europejskich pucharów
    podzial_zespolow = [
        [
            ['winners', 2],
            ['ENG', 4],
            ['SPA', 4],
            ['ITA', 4],
            ['GER', 4],
            ['FRA', 3],
            ['OTH', 15]
        ],
        [
            ['ENG', 3], # cup winner + 2
            ['SPA', 3],
            ['ITA', 3],
            ['GER', 3],
            ['FRA', 2],
            ['OTH', 22]
        ]
    ]

    winners = []

    for poziom_rozgrywkowy in range(1,3):
        # Zwycięzca EU
        cursor.execute("""
            SELECT nazwa, kraj
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ? AND cup_round = (SELECT MAX(cup_round) FROM eu_druzyny WHERE poziom_rozgrywkowy = ?)
        """, (poziom_rozgrywkowy, poziom_rozgrywkowy,))

        winner = cursor.fetchone()

        winners.append(winner)

    cursor.execute("DELETE FROM eu_druzyny WHERE kraj = 'ENG'")
    
    cursor.execute("""
        UPDATE eu_druzyny SET
        poziom_rozgrywkowy = 0
    """)

    # Dodaj angielskie zespoly
    cursor.execute("""
        SELECT nazwa
        FROM druzyny
        WHERE poziom_rozgrywkowy = 1
        ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
        LIMIT 4
    """)

    next_season_cl_teams = cursor.fetchall()

    for team in next_season_cl_teams:
        cursor.execute("""
            INSERT INTO eu_druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength)
                SELECT nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, 1, kraj, budget, bg_color, fg_color, basic_strength
                FROM druzyny
                WHERE nazwa = ?
        """, (team[0],))

    # Dodaj zespoły topowych lig
    for i in range(2,6):
        cursor.execute("""
            SELECT nazwa
            FROM eu_druzyny
            WHERE kraj = ?
            ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC
            LIMIT ?
        """, (podzial_zespolow[0][i][0], podzial_zespolow[0][i][1],))

        najsilniejsze_druzyny = cursor.fetchall()

        for druzyna in najsilniejsze_druzyny:
            cursor.execute("""
                UPDATE eu_druzyny SET
                poziom_rozgrywkowy = 1
                WHERE nazwa = ?
            """, (druzyna[0],))

    # Dodaj zwycięzców pucharów
    for winner in winners:
        if winner[1] == 'ENG':
            cursor.execute("""
                INSERT INTO eu_druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength)
                SELECT nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, 1, kraj, budget, bg_color, fg_color, basic_strength
                FROM druzyny
                WHERE nazwa = ? AND NOT EXISTS (
                    SELECT 1
                    FROM eu_druzyny
                    WHERE nazwa = ?
                )
            """, (winner[0], winner[0]))

            row_count = cursor.rowcount

            if row_count <= 0:
                podzial_zespolow[0][6][1] += 1
        else:
            cursor.execute("""
                UPDATE eu_druzyny SET
                poziom_rozgrywkowy = 1
                WHERE nazwa = ? AND poziom_rozgrywkowy = 0
            """, (winner[0],))

            row_count = cursor.rowcount

            if row_count <= 0:
                podzial_zespolow[0][6][1] += 1

    cursor.execute("""
        SELECT nazwa
        FROM eu_druzyny
        WHERE kraj = 'OTH' AND poziom_rozgrywkowy = 0
        ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu + RANDOM() * 8) DESC
        LIMIT ?
    """, (podzial_zespolow[0][6][1],))

    pozostale_druzyny = cursor.fetchall()

    for druzyna in pozostale_druzyny:
        cursor.execute("""
            UPDATE eu_druzyny SET
            poziom_rozgrywkowy = 1
            WHERE nazwa = ?
        """, (druzyna[0],))

    # Liga europy
    # Dodaj zwyciezce pucharu
    cursor.execute("""
        SELECT nazwa
        FROM druzyny
        WHERE cup_round = (SELECT MAX(cup_round) FROM druzyny)
    """)

    winner = cursor.fetchone()

    cursor.execute("""
        INSERT INTO eu_druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength)
        SELECT nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, 2, kraj, budget, bg_color, fg_color, basic_strength
        FROM druzyny
        WHERE nazwa = ? AND NOT EXISTS (
            SELECT 1
            FROM eu_druzyny
            WHERE nazwa = ?
        )
    """, (winner[0], winner[0],))

    row_count = cursor.rowcount

    if row_count > 0:
        eng_el_limit = 2
    else:
        eng_el_limit = 3

    # Dodaj angielskie zespoly
    cursor.execute("""
        SELECT nazwa
        FROM druzyny
        WHERE poziom_rozgrywkowy = 1
        ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
        LIMIT 6 OFFSET 4
    """)

    england_teams = cursor.fetchall()
    itterator = 0
    while eng_el_limit > 0:
        cursor.execute("""
            INSERT INTO eu_druzyny (nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, poziom_rozgrywkowy, kraj, budget, bg_color, fg_color, basic_strength)
            SELECT nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa, 2, kraj, budget, bg_color, fg_color, basic_strength
            FROM druzyny
            WHERE nazwa = ? AND NOT EXISTS (
                SELECT 1
                FROM eu_druzyny
                WHERE nazwa = ?
            )
        """, (england_teams[itterator][0], england_teams[itterator][0],))

        row_count = cursor.rowcount

        if row_count > 0:
            eng_el_limit -= 1
        itterator += 1

    # Dodaj zespoły pozostałych lig
    for i in range(1,6):
        cursor.execute("""
            SELECT nazwa
            FROM eu_druzyny
            WHERE kraj = ? AND poziom_rozgrywkowy = 0
            ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu + RANDOM() * 10) DESC
            LIMIT ?
        """, (podzial_zespolow[1][i][0], podzial_zespolow[1][i][1],))

        najsilniejsze_druzyny = cursor.fetchall()

        for druzyna in najsilniejsze_druzyny:
            cursor.execute("""
                UPDATE eu_druzyny SET
                poziom_rozgrywkowy = 2
                WHERE nazwa = ?
            """, (druzyna[0],))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()
    
def reset_schedule():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Usuwamy terminarz
    cursor.execute("DELETE FROM mecze")

    # Resetowanie statystyk
    cursor.execute("""
        UPDATE druzyny SET
        punkty = 0,
        zwyciestwa = 0,
        remisy = 0,
        porazki = 0,
        bramki_strzelone = 0,
        bramki_stracone = 0,
        zolte_kartki = 0,
        czerwone_kartki = 0,
        forma = ''
    """)

    # Resetowanie statystyk
    cursor.execute("""
        UPDATE eu_druzyny SET
        punkty = 0,
        zwyciestwa = 0,
        remisy = 0,
        porazki = 0,
        bramki_strzelone = 0,
        bramki_stracone = 0,
        zolte_kartki = 0,
        czerwone_kartki = 0,
        forma = ''
    """)

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

    create_schedule()

def update_teams_for_new_season(nazwa_klubu):
    zmiana_ligi = 1
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Sprawdzamy ile poziomów rozgrywkowych
    cursor.execute("SELECT COUNT(DISTINCT poziom_rozgrywkowy) FROM druzyny")
    poziomy_rozgrywkowe = cursor.fetchone()[0]

    #
    for poziom_rozgrywkowy in range(1, poziomy_rozgrywkowe + 1):
        if 1 <= poziom_rozgrywkowy < poziomy_rozgrywkowe:
            if poziom_rozgrywkowy == 3:
                spadki = 4
            else:
                spadki = 3
            # Wybieramy najsłabsze zespoły
            cursor.execute("""
                SELECT nazwa
                FROM druzyny
                WHERE poziom_rozgrywkowy = ?
                ORDER BY punkty ASC, (bramki_strzelone - bramki_stracone) ASC, bramki_strzelone ASC, zwyciestwa ASC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) ASC, nazwa DESC
                LIMIT ?
            """, (poziom_rozgrywkowy, spadki,))
            weakest_teams = cursor.fetchall()

            # Dla każdej drużyny dodaj status spadek
            for team in weakest_teams:
                cursor.execute("""
                    UPDATE druzyny
                    SET status_utrzymania = 'spadek'
                    WHERE nazwa = ?
                """, (team[0],))

        if poziom_rozgrywkowy > 1:
            if poziom_rozgrywkowy == 4:
                awanse = 3
            else:
                awanse = 2
            # Wybieramy 3 najlepsze zespoły
            cursor.execute("""
                SELECT nazwa
                FROM druzyny
                WHERE poziom_rozgrywkowy = ?
                ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                LIMIT ?
            """, (poziom_rozgrywkowy, awanse,))
            strongest_teams = cursor.fetchall()

            # Dla każdej drużyny dodaj status awans
            for team in strongest_teams:
                cursor.execute("""
                    UPDATE druzyny
                    SET status_utrzymania = 'awans'
                    WHERE nazwa = ?
                """, (team[0],))

    cursor.execute("""
        SELECT status_utrzymania
        FROM druzyny
        WHERE NAZWA = ?
    """, (nazwa_klubu,))

    status_utrzymania = cursor.fetchone()[0]

    if status_utrzymania == 'spadek':
        zmiana_ligi = 2
    elif status_utrzymania == 'awans':
        zmiana_ligi = 0

    # Sprawdzamy status dla każdej drużyny i aktualizujemy poziom_rozgrywkowy
    cursor.execute("""
        UPDATE druzyny
        SET poziom_rozgrywkowy = 
            CASE 
                WHEN status_utrzymania = 'spadek' THEN poziom_rozgrywkowy + 1
                WHEN status_utrzymania = 'awans' THEN poziom_rozgrywkowy - 1
                ELSE poziom_rozgrywkowy
            END,
            status_utrzymania = 'stay'
    """)
    
    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()
    return zmiana_ligi

def add_winners(season):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobierz listę państw
    cursor.execute("SELECT DISTINCT kraj FROM ligi")
    kraje = [row[0] for row in cursor.fetchall()]

    # Dla każdego kraju
    for kraj in kraje:
        cursor.execute("SELECT COUNT(DISTINCT poziom_rozgrywkowy) FROM ligi WHERE kraj = ?", (kraj,))
        ligi = cursor.fetchone()[0]
        # Dla każdego poziomu rozgrywkowego
        for liga in range(1, ligi + 1):
            # Wybieramy 3 najlepsze zespoły
            cursor.execute("""
                SELECT nazwa
                FROM druzyny
                WHERE poziom_rozgrywkowy = ? AND kraj = ?
                ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
                LIMIT 3
            """, (liga, kraj,))
            top3 = cursor.fetchall()
            # I dodajemy je do bazy
            cursor.execute("INSERT INTO winners (country, league_level, season, first, second, third, competition) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (kraj, liga, season, top3[0][0], top3[1][0], top3[2][0], 'league',))
            
    cursor.execute("""
        SELECT nazwa
        FROM druzyny
        ORDER BY cup_round DESC
        LIMIT 2
    """)

    cup_finalists = cursor.fetchall()

    cursor.execute("INSERT INTO winners (country, league_level, season, first, second, third, competition) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('ENG', 0, season, cup_finalists[0][0], cup_finalists[1][0], '-', 'cup',))

    for poziom_rozgrywkowy in range(1,3):
        cursor.execute("""
            SELECT nazwa
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY cup_round DESC
            LIMIT 2
        """, (poziom_rozgrywkowy,))

        cup_finalists = cursor.fetchall()

        cursor.execute("INSERT INTO winners (country, league_level, season, first, second, third, competition) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ('EU', poziom_rozgrywkowy, season, cup_finalists[0][0], cup_finalists[1][0], '-', 'EU',))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def initiate():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Tworzymy tabelę "ligi" z odpowiednimi polami
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ligi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kraj TEXT NOT NULL,
            poziom_rozgrywkowy INTEGER NOT NULL
        )
    ''')

        # Tworzymy tabelę dla drużyn z nowymi atrybutami
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS druzyny (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            formacja TEXT,
            sila_bramkarza INTEGER,
            sila_obrony INTEGER,
            sila_pomocy INTEGER,
            sila_napadu INTEGER,
            zaangazowanie INTEGER,
            sila_trenera INTEGER,
            nastawienie INTEGER,
            dlugosc_podan INTEGER,
            pressing INTEGER,
            wslizgi INTEGER,
            krycie INTEGER,
            kontry INTEGER,
            pulapki_offsidowe INTEGER,
            premia_domowa REAL,
            punkty INTEGER DEFAULT 0,
            zwyciestwa INTEGER DEFAULT 0,
            remisy INTEGER DEFAULT 0,
            porazki INTEGER DEFAULT 0,
            bramki_strzelone INTEGER DEFAULT 0,
            bramki_stracone INTEGER DEFAULT 0,
            zolte_kartki INTEGER DEFAULT 0,
            czerwone_kartki INTEGER DEFAULT 0,
            forma TEXT DEFAULT '',
            poziom_rozgrywkowy INTEGER,
            kraj TEXT,
            status_utrzymania TEXT DEFAULT 'stay',
            budget DECIMAL(10, 2),
            bg_color TEXT,
            fg_color TEXT,
            basic_strength INTEGER,
            cup_round INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eu_druzyny (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            formacja TEXT,
            sila_bramkarza INTEGER,
            sila_obrony INTEGER,
            sila_pomocy INTEGER,
            sila_napadu INTEGER,
            zaangazowanie INTEGER,
            sila_trenera INTEGER,
            nastawienie INTEGER,
            dlugosc_podan INTEGER,
            pressing INTEGER,
            wslizgi INTEGER,
            krycie INTEGER,
            kontry INTEGER,
            pulapki_offsidowe INTEGER,
            premia_domowa REAL,
            punkty INTEGER DEFAULT 0,
            zwyciestwa INTEGER DEFAULT 0,
            remisy INTEGER DEFAULT 0,
            porazki INTEGER DEFAULT 0,
            bramki_strzelone INTEGER DEFAULT 0,
            bramki_stracone INTEGER DEFAULT 0,
            zolte_kartki INTEGER DEFAULT 0,
            czerwone_kartki INTEGER DEFAULT 0,
            forma TEXT DEFAULT '',
            poziom_rozgrywkowy INTEGER,
            kraj TEXT,
            status_utrzymania TEXT DEFAULT 'stay',
            budget DECIMAL(10, 2),
            bg_color TEXT,
            fg_color TEXT,
            basic_strength INTEGER,
            cup_round INTEGER DEFAULT 1
        )
    ''')

    # Tworzymy tabelę dla meczów z nowymi atrybutami
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mecze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            druzyna_gospodarza TEXT NOT NULL,
            druzyna_gosci TEXT NOT NULL,
            wynik TEXT,
            kolejka INTEGER NOT NULL,
            poziom_rozgrywkowy INTEGER,
            rozgrywki TEXT
        )
    ''')

    # Tworzymy save
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            selected_club TEXT,
            league_level INTEGER,
            gameweek INTEGER,
            season INTEGER
        )
    ''')

    # Tworzymy transfer market
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfer_market (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER,
            upgrade_chances INTEGER,
            neutral_chances INTEGER,
            downgrade_chances INTEGER,
            expire_time INTEGER,
            price DECIMAL(10, 2)
        )
    ''')

    # Tworzymy transfer market
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfer_market_sell (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER,
            neutral_chances INTEGER,
            downgrade_chances INTEGER,
            expire_time INTEGER,
            price DECIMAL(10, 2)
        )
    ''')

    # Tworzymy tabelę zwycięzcy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            league_level INTEGER NOT NULL,
            season INTEGER,
            first TEXT,
            second TEXT,
            third TEXT,
            competition TEXT
        )
    ''')

    # Pobierz liczbę rekordów w tabeli saved_game
    cursor.execute("SELECT COUNT(*) FROM saved_game")
    result = cursor.fetchone()
    count_records = result[0]

    # Jeżeli nie ma żadnych rekordów, dodaj jeden
    if count_records == 0:
        cursor.execute("INSERT INTO saved_game (selected_club, league_level, gameweek, season) VALUES (?, ?, ?, ?)",
                    ("", 1, 1, 1,))


    
    conn.commit()
    conn.close()

def start_new_game():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Usuwamy ligi
    cursor.execute("DELETE FROM ligi")

    # Usuwamy druzyny
    cursor.execute("DELETE FROM druzyny")

    # Usuwamy druzyny
    cursor.execute("DELETE FROM eu_druzyny")

    # Usuwamy terminarz
    cursor.execute("DELETE FROM mecze")

    # Usuwamy transfery
    cursor.execute("DELETE FROM transfer_market")

    # Usuwamy ofert
    cursor.execute("DELETE FROM transfer_market_sell")

    # Usuwamy historie
    cursor.execute("DELETE FROM winners")

    # czyścimy save
    cursor.execute("""
        UPDATE saved_game
        SET selected_club = ?, league_level = ?, gameweek = ?, season = ?
        WHERE id = 1
    """, ("", 1, 1, 1,))
    
    conn.commit()
    conn.close()

    create_leagues(kraje)
    create_teams(ENG1)
    create_teams(ENG2)
    create_teams(ENG3)
    create_teams(ENG4)
    create_teams_eu(EU)
    create_schedule()

def create_transfer_list(club):
    for i in range(10):
        create_list_player(club)
    for i in range(3):
        create_offers(club)

def create_list_player(club):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobieramy nazwy klubów z bazy danych
    cursor.execute("""SELECT sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu
        FROM druzyny
        WHERE nazwa = ?
    """, (club,))
    stats = cursor.fetchone()

    pozycja = random.choices(
        [1,2,3,4],
        [10,30,30,30]
    )[0]
    los = random.randint(0, 3 * (100 - stats[pozycja-1]))
    upgrade_chances = min(max(0, los), 90)
    neutral_chances = random.randint(round((100 - upgrade_chances) / 3), 100 - upgrade_chances)
    downgrade_chances = 100 - upgrade_chances - neutral_chances
    expire_time = random.randint(3, 15)
    price = get_price(pozycja, stats[pozycja - 1]) * (1 + ((upgrade_chances - 50) * 0.75 / 100) - ((downgrade_chances - 50) * 0.5 / 100)) * (1 + (random.uniform(-10, 10.000001) / 100))
    price = round(price, 2)
    cursor.execute("""INSERT INTO transfer_market (position, upgrade_chances, neutral_chances, downgrade_chances, expire_time, price)
        VALUES (?, ?, ?, ?, ?, ?)""", (pozycja, upgrade_chances, neutral_chances, downgrade_chances, expire_time, price,))

    # Zamykamy połączenie z bazą danych
    conn.commit()
    conn.close()

def create_offers(club):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobieramy nazwe klubu z bazy danych
    cursor.execute("""SELECT sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu
        FROM druzyny
        WHERE nazwa = ?
    """, (club,))
    stats = cursor.fetchone()

    pozycja = random.choices(
        [1,2,3,4],
        [10,30,30,30]
    )[0]
    neutral_chances = random.randint(0, 80)
    downgrade_chances = 100 - neutral_chances
    expire_time = random.randint(3, 8)
    price = get_price(pozycja, stats[pozycja - 1]) * (1 + ((downgrade_chances - 50) * 0.75 / 100) - ((neutral_chances - 50) * 0.5 / 100)) * (1 + (random.uniform(-5, 30.000001) / 100))
    price = round(price, 2)
    cursor.execute("""INSERT INTO transfer_market_sell (position, neutral_chances, downgrade_chances, expire_time, price)
        VALUES (?, ?, ?, ?, ?)""", (pozycja, neutral_chances, downgrade_chances, expire_time, price,))

    # Zamykamy połączenie z bazą danych
    conn.commit()
    conn.close()

def get_price(position, skill):
    cena_bramkarza = 0.5 + 0.04 * max(0, min(skill - 60, 5)) +\
        0.14 * max(0, min(skill - 65, 5)) +\
        0.52 * max(0, min(skill - 70, 5)) +\
        2.2 * max(0, min(skill - 75, 5)) +\
        5 * max(0, min(skill - 80, 5)) +\
        4 * max(0, min(skill - 85, 5)) +\
        8 * max(0, min(skill - 90, 5)) +\
        20 * max(0, min(skill - 95, 5))

    cena_obroncy = 0.6 + 0.08 * max(0, min(skill - 60, 5)) +\
        0.1 * max(0, min(skill - 65, 5)) +\
        0.9 * max(0, min(skill - 70, 5)) +\
        2.4 * max(0, min(skill - 75, 5)) +\
        4.4 * max(0, min(skill - 80, 5)) +\
        11.4 * max(0, min(skill - 85, 5)) +\
        10.6 * max(0, min(skill - 90, 5)) +\
        30 * max(0, min(skill - 95, 5))

    cena_pomocnika = 0.7 + 0.06 * max(0, min(skill - 60, 5)) +\
        0.16 * max(0, min(skill - 65, 5)) +\
        0.84 * max(0, min(skill - 70, 5)) +\
        2.8 * max(0, min(skill - 75, 5)) +\
        6 * max(0, min(skill - 80, 5)) +\
        10.6 * max(0, min(skill - 85, 5)) +\
        14.4 * max(0, min(skill - 90, 5)) +\
        35 * max(0, min(skill - 95, 5))

    cena_napastnika = 0.8 + 0.04 * max(0, min(skill - 60, 5)) +\
        0.2 * max(0, min(skill - 65, 5)) +\
        0.8 * max(0, min(skill - 70, 5)) +\
        3.4 * max(0, min(skill - 75, 5)) +\
        7.4 * max(0, min(skill - 80, 5)) +\
        12 * max(0, min(skill - 85, 5)) +\
        16 * max(0, min(skill - 90, 5)) +\
        40 * max(0, min(skill - 95, 5))
    
    prices = [round(cena_bramkarza, 2), round(cena_obroncy, 2), round(cena_pomocnika, 2), round(cena_napastnika, 2)]

    return prices[position-1]

def fill_transfer_market(club):
    # Połącz się z bazą danych
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Zmniejsz o 1 czas zakończenia aukcji
    cursor.execute("""UPDATE transfer_market
        SET expire_time = expire_time - 1
    """)

    cursor.execute("""UPDATE transfer_market_sell
        SET expire_time = expire_time - 1
    """)

    # Usuń zakończone aukcje
    cursor.execute("""DELETE FROM transfer_market
        WHERE expire_time = 0
    """)

    cursor.execute("""DELETE FROM transfer_market_sell
        WHERE expire_time = 0
    """)

    # Wykonaj zapytanie
    cursor.execute("SELECT COUNT(*) FROM transfer_market")

    # Pobierz wynik
    players_buy = cursor.fetchone()[0]

    # Wykonaj zapytanie
    cursor.execute("SELECT COUNT(*) FROM transfer_market_sell")

    # Pobierz wynik
    players_sell = cursor.fetchone()[0]
    
    # Zamknij połączenie
    conn.commit()
    conn.close()

    for i in range(players_buy, 10):
        create_list_player(club)

    for i in range(players_sell, 3):
        create_offers(club)

def change_strength(team, position, up_or_down, price, player_id, buy_or_sell):
    if position == 1:
        zmieniana_pozycja = "sila_bramkarza"
    elif position == 2:
        zmieniana_pozycja = "sila_obrony"
    elif position == 3:
        zmieniana_pozycja = "sila_pomocy"
    elif position == 4:
        zmieniana_pozycja = "sila_napadu"
    if up_or_down == 1:
        znak = "+"
    elif up_or_down == 2:
        znak = "*"
    elif up_or_down == 3:
        znak = "-"
    
    query = f"""
        UPDATE druzyny
        SET {zmieniana_pozycja} = {zmieniana_pozycja} {znak} 1
        WHERE nazwa = '{team}'
    """

    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Aktualizujemy siłę na podstawie danych
    cursor.execute(query)
    
    if buy_or_sell == 'buy':
        # Aktualizujemy budżet
        cursor.execute("""
            UPDATE druzyny
            SET budget = budget - ?
            WHERE nazwa = ?
        """, (price, team,))

        # Aktualizujemy listę transferową
        cursor.execute("""
            DELETE FROM transfer_market
            WHERE id = ?
        """, (player_id,))

    elif buy_or_sell == 'sell':
        # Aktualizujemy budżet
        cursor.execute("""
            UPDATE druzyny
            SET budget = budget + ?
            WHERE nazwa = ?
        """, (price, team,))

        # Aktualizujemy listę transferową
        cursor.execute("""
            DELETE FROM transfer_market_sell
            WHERE id = ?
        """, (player_id,))

    # Zamykamy połączenie z bazą danych
    conn.commit()
    conn.close()

def season_end_update_teams(team):
    rewards = [
        [200,190,180,170,160,150,130,110,90,85,80,75,72,72,70,70,68,68,65,65],
        [40,35,30,30,25,25,20,20,18,18,17,17,16,16,15,15,14,14,13,13,12,12,11,11],
        [8,7.75,7.5,7.25,7,6.75,6.5,6.25,6,5.75,5.5,5.25,5,4.75,4.5,4.25,4,3.75,3.5,3.25,3,2.75,2.5,2.25],
        [2,1.9,1.8,1.7,1.6,1.5,1.5,1.4,1.4,1.3,1.3,1.2,1.2,1.1,1.1,1,1,1,1,1,1,1,1,1]
    ]
    expected_strength_array = [
        [90,89,87,85,83,82,81,80,79,78,77,76,76,75,75,74,74,73,73,73],
        [73,73,73,73,73,73,72,72,72,71,71,71,71,71,71,70,70,70,69,69,69,69,69,69],
        [69,69,69,69,69,69,68,68,68,67,67,67,67,67,67,66,66,66,65,65,65,65,65,65],
        [65,65,65,65,65,65,64,64,64,63,63,63,63,63,63,62,62,62,61,61,61,61,61,61]
    ]
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT poziom_rozgrywkowy)
        FROM druzyny
    """)

    poziomy_rozgrywkowe = cursor.fetchone()[0]

    for poziom_rozgrywkowy in range(poziomy_rozgrywkowe):
        cursor.execute("""
            SELECT COUNT(*)
            FROM druzyny
            WHERE poziom_rozgrywkowy = ?
        """, (poziom_rozgrywkowy + 1,))

        liczba_druzyn = cursor.fetchone()[0]

        cursor.execute("""
            SELECT nazwa, pozycja, oczekiwana_pozycja, basic_strength, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, budget
            FROM (
                SELECT nazwa,
                    ROW_NUMBER() OVER (ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC) as pozycja,
                    ROW_NUMBER() OVER (ORDER BY (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, sila_napadu DESC, sila_pomocy DESC, sila_obrony DESC, sila_bramkarza DESC) as oczekiwana_pozycja,
                    basic_strength,
                    sila_bramkarza,
                    sila_obrony,
                    sila_pomocy,
                    sila_napadu,
                    budget
                FROM druzyny
                WHERE poziom_rozgrywkowy = ?
            )
        """, (poziom_rozgrywkowy + 1,))
        
        dane = cursor.fetchall()

        for index in range(liczba_druzyn):
            nazwa = dane[index][0]
            if not nazwa == team:
                pozycja = dane[index][1]
                oczekiwana_pozycja = dane[index][2]
                sila = dane[index][3]
                oczekiwana_sila = expected_strength_array[poziom_rozgrywkowy][pozycja - 1]
                sila_bramkarza = dane[index][4]
                sila_obrony = dane[index][5]
                sila_pomocy = dane[index][6]
                sila_napadu = dane[index][7]
                sb_roznica = oczekiwana_sila - sila_bramkarza
                so_roznica = oczekiwana_sila - sila_obrony
                sp_roznica = oczekiwana_sila - sila_pomocy
                sn_roznica = oczekiwana_sila - sila_napadu

                reward = rewards[poziom_rozgrywkowy][pozycja - 1]

                roznica_pozycja = oczekiwana_pozycja - pozycja
                roznica_sila = oczekiwana_sila - sila

                budget = dane[index][8]
                koszt_zawodnika = get_price(2, sila)
                ilosc_zakupow = int(budget // koszt_zawodnika)

                sila_zmiana = sprawdz_szanse_na_zmiane(roznica_pozycja, roznica_sila, 0)
                sb_zmiana = sprawdz_szanse_na_zmiane(sb_roznica, sb_roznica, ilosc_zakupow)
                so_zmiana = sprawdz_szanse_na_zmiane(so_roznica, so_roznica, ilosc_zakupow)
                sp_zmiana = sprawdz_szanse_na_zmiane(sp_roznica, sp_roznica, ilosc_zakupow)
                sn_zmiana = sprawdz_szanse_na_zmiane(sn_roznica, sn_roznica, ilosc_zakupow)

                final_sila = min(100, max(30, sila + sila_zmiana))
                final_bramkarz = min(100, max(30, sila_bramkarza + sb_zmiana))
                final_obrona = min(100, max(30, sila_obrony + so_zmiana))
                final_pomoc = min(100, max(30, sila_pomocy + sp_zmiana))
                final_napad = min(100, max(30, sila_napadu + sn_zmiana))

                final_budget = (budget % koszt_zawodnika) + reward

                if oczekiwana_pozycja + 3 > pozycja:
                    zmiana_trenera = random.choices(
                        [True, False],
                        [0.8, 0.2]
                    )[0]
                else:
                    zmiana_trenera = random.choices(
                        [True, False],
                        [0.2, 0.8]
                    )[0]

                if zmiana_trenera:
                    zmien_taktyke(nazwa, cursor, 'ENG')

                # Dodaj pieniadze na podstawie tabeli nagrod
                cursor.execute("""
                    UPDATE druzyny
                    SET basic_strength = ?,
                        sila_bramkarza = ?,
                        sila_obrony = ?,
                        sila_pomocy = ?,
                        sila_napadu = ?,
                        budget = ?
                    WHERE nazwa = ?
                """, (final_sila, final_bramkarz, final_obrona, final_pomoc, final_napad, final_budget, nazwa,))
            else:
                pozycja = dane[index][1]
                reward = rewards[poziom_rozgrywkowy][pozycja - 1]
                budget = dane[index][8]
                final_budget = budget + reward
                cursor.execute("""
                    UPDATE druzyny
                    SET budget = ?
                    WHERE nazwa = ?
                """, (final_budget, nazwa,))

    # Zwycięzca pucharu
    cursor.execute("SELECT MAX(cup_round) FROM druzyny")

    # Pobranie wyniku zapytania
    cup_round = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE druzyny
        SET budget = budget + 15
        WHERE cup_round = ?
    """, (cup_round,))

    for poziom_rozgrywkowy in range(1,3):
        prize = [40, 15]
        # Zwycięzca EU
        cursor.execute("""
            SELECT nazwa, kraj
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ? AND cup_round = (SELECT MAX(cup_round) FROM eu_druzyny WHERE poziom_rozgrywkowy = ?)
        """, (poziom_rozgrywkowy, poziom_rozgrywkowy,))

        winner = cursor.fetchone()

        if winner[1] == 'ENG':
            cursor.execute("""
            UPDATE druzyny
                SET budget = budget + ?
                WHERE nazwa = ?
            """, (prize[poziom_rozgrywkowy-1], winner[0],))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def season_end_update_eu_teams():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nazwa, basic_strength, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu
        FROM (
            SELECT nazwa,
                basic_strength,
                sila_bramkarza,
                sila_obrony,
                sila_pomocy,
                sila_napadu
            FROM eu_druzyny
            WHERE kraj NOT LIKE 'ENG'
        )
    """)

    dane = cursor.fetchall()

    for index in range(len(dane)):
        nazwa = dane[index][0]

        sila = dane[index][1]
        sila_bramkarza = dane[index][2]
        sila_obrony = dane[index][3]
        sila_pomocy = dane[index][4]
        sila_napadu = dane[index][5]

        sb_roznica = sila - sila_bramkarza
        so_roznica = sila - sila_obrony
        sp_roznica = sila - sila_pomocy
        sn_roznica = sila - sila_napadu

        sila_zmiana = random.choices(
            [1, 0, -1],
            [33, 34, 33]
        )[0]
        sb_zmiana = sprawdz_szanse_na_zmiane(sb_roznica, sb_roznica, 0)
        so_zmiana = sprawdz_szanse_na_zmiane(so_roznica, so_roznica, 0)
        sp_zmiana = sprawdz_szanse_na_zmiane(sp_roznica, sp_roznica, 0)
        sn_zmiana = sprawdz_szanse_na_zmiane(sn_roznica, sn_roznica, 0)

        final_sila = min(97, max(55, sila + sila_zmiana))
        final_bramkarz = min(97, max(55, sila_bramkarza + sb_zmiana))
        final_obrona = min(97, max(55, sila_obrony + so_zmiana))
        final_pomoc = min(97, max(55, sila_pomocy + sp_zmiana))
        final_napad = min(97, max(55, sila_napadu + sn_zmiana))
        
        zmiana_trenera = random.choices(
            [True, False],
            [0.8, 0.2]
        )[0]

        if zmiana_trenera:
            zmien_taktyke(nazwa, cursor, 'EU')

        # Dodaj pieniadze na podstawie tabeli nagrod
        cursor.execute("""
            UPDATE eu_druzyny
            SET basic_strength = ?,
                sila_bramkarza = ?,
                sila_obrony = ?,
                sila_pomocy = ?,
                sila_napadu = ?
            WHERE nazwa = ?
        """, (final_sila, final_bramkarz, final_obrona, final_pomoc, final_napad, nazwa,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def zmien_taktyke(team, cursor, type):
    formacje = ["3-5-2", "3-4-3", "3-3-4", "4-5-1", "4-4-2", "4-3-3", "4-2-4", "5-4-1", "5-3-2", "5-2-3"]
    los_formacja = random.randint(0, 9)
    formacja = formacje[los_formacja]
    nastawienie = random.randint(1, 5)
    dlugosc_podan = random.randint(1, 3)
    pressing = random.randint(1, 3)
    wslizgi = random.randint(1, 3)
    krycie = random.randint(1, 2)
    kontry = random.randint(1, 2)
    pulapki_offsidowe = random.randint(1, 2)

    if type == 'EU':
        cursor.execute("""
            UPDATE eu_druzyny
            SET formacja = ?,
                nastawienie = ?,
                dlugosc_podan = ?,
                pressing = ?,
                wslizgi = ?,
                krycie = ?,
                kontry = ?,
                pulapki_offsidowe = ?
            WHERE nazwa = ?
        """, (formacja, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, team,))
    else:
        cursor.execute("""
            UPDATE druzyny
            SET formacja = ?,
                nastawienie = ?,
                dlugosc_podan = ?,
                pressing = ?,
                wslizgi = ?,
                krycie = ?,
                kontry = ?,
                pulapki_offsidowe = ?
            WHERE nazwa = ?
        """, (formacja, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, team,))

def sprawdz_szanse_na_zmiane(tolerowana_roznica, liczona_roznica, zakupieni_gracze):
    bonus = zakupieni_gracze
    # jeżeli różnica pozycji nie większa niż 2 to szanse równe
    if abs(tolerowana_roznica) < 3:
        szansa_wzrost = 33 + bonus
        szansa_spadek = 33 - bonus
        szansa_bez_zmian = 34
    else:
        szansa_wzrost = min(100, max(0, (33 + liczona_roznica * (4 if liczona_roznica > 0 else 3) + bonus)))
        szansa_spadek = min(100, max(0, (33 - liczona_roznica * (4 if liczona_roznica < 0 else 3) - bonus)))
        szansa_bez_zmian = 100 - szansa_wzrost - szansa_spadek

    szanse_zmiana = random.choices(
        [1, 0, -1],
        [szansa_wzrost, szansa_bez_zmian, szansa_spadek]
    )[0]

    return szanse_zmiana

def budget_update(team, result, competition):
    rewards = [
        [2.2, 0.9], #1L
        [0.47, 0.2], #2L
        [0.18, 0.08], #3L
        [0.06, 0.02], #4L
        [0,0.3,0.8,1,2,4,8], #CUP
        [2.5, 1, 3, 5, 10, 15], #EU
        [1, 0.3, 1, 2, 4, 7] #EL
    ]
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobieramy poziom rozgrywkowy i pozycję
    if competition == "league":
        cursor.execute("SELECT poziom_rozgrywkowy FROM druzyny WHERE nazwa = ?", (team,))
        poziom_rozgrywkowy = cursor.fetchone()[0]

        reward = rewards[poziom_rozgrywkowy-1][result - 1]
    elif competition == "cup":
        cursor.execute("SELECT MAX(cup_round) FROM druzyny")
        runda = cursor.fetchone()[0]
        if runda == 2:
            cursor.execute("""SELECT
                    cup_round,
                    COUNT(*) AS ilosc_wystapien
                FROM
                    druzyny
                WHERE
                    cup_round IN (1, 2)
                GROUP BY
                    cup_round
            """)
            druzyny_dla_rund12 = cursor.fetchall()
            d_runda1 = druzyny_dla_rund12[0][1]
            d_runda2 = druzyny_dla_rund12[1][1]
            if d_runda1 > d_runda2:
                runda = 1
        reward = rewards[4][runda-1]
    elif competition == "EU":
        cursor.execute("SELECT MAX(cup_round) FROM eu_druzyny")
        runda = cursor.fetchone()[0]

        cursor.execute("SELECT poziom_rozgrywkowy FROM eu_druzyny WHERE nazwa = ?", (team,))
        poziom = cursor.fetchone()[0]
        if poziom == 1:
            arr_index = 5
        else:
            arr_index = 6

        if runda == 1:
            reward = rewards[arr_index][result - 1]
        else:
            reward = rewards[arr_index][runda-1]

    # Dodaj pieniadze na podstawie tabeli nagrod
    if reward > 0:
        cursor.execute("""
            UPDATE druzyny SET
            budget = budget + ?
            WHERE nazwa = ?
        """, (reward, team,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def clear_cards(team1, team2, rozgrywki):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Wyczyść kartki
    if rozgrywki == 'league':
        cursor.execute("""
            UPDATE druzyny
            SET zolte_kartki = zolte_kartki % 10,
                czerwone_kartki = 0
            WHERE nazwa = ? or nazwa = ?
        """, (team1, team2,))
    elif rozgrywki == 'EU':
        cursor.execute("""
            UPDATE eu_druzyny
            SET zolte_kartki = zolte_kartki % 3,
                czerwone_kartki = 0
            WHERE nazwa = ? or nazwa = ?
        """, (team1, team2,))

    # Zatwierdzamy zmiany i zamykamy połączenie
    conn.commit()
    conn.close()

def load_game():
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pobieramy nazwy klubów z bazy danych
    cursor.execute("SELECT selected_club, league_level, gameweek, season FROM saved_game")
    data = cursor.fetchall()[0]

    # Zamykamy połączenie z bazą danych
    conn.close()

    return data

def save_game(klub, poziom_rozgrywkowy, gameweek, sezon):
    # Łączymy się z bazą danych
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Zapisz
    cursor.execute("""
        UPDATE saved_game
        SET selected_club = ?, league_level = ?, gameweek = ?, season = ?
        WHERE id = 1
    """, (klub, poziom_rozgrywkowy, gameweek, sezon,))

    # Zamykamy połączenie z bazą danych
    conn.commit()
    conn.close()