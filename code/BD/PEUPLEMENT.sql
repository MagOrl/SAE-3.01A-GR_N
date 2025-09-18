--Insertions supplémentaires faites avec l'aide d'une IA
DELETE FROM ESPECE;
DELETE FROM EXTRAIRE;
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM ECHANTILLION;
DELETE FROM SEQUENCE;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

INSERT INTO
    HABILITATION
VALUES
    ("H001", "Chimique"),
    ("H002", "Biologique"),
    ("H003", "Géologique"),
    ("H004", "Paléontologique"),
    ("H005", "Radiologique"),
    ("H006", "Microscopique"),
    ("H007", "Spectroscopique"),
    ("H008", "Cristallographique"),
    ("H009", "Immunologique"),
    ("H010", "Moléculaire");

INSERT INTO
    PERSONNEL
VALUES
    ("PER001", "LEROY"),
    ("PER002", "MARTIN"),
    ("PER003", "BERNARD"),
    ("PER004", "THOMAS"),
    ("PER005", "PETIT"),
    ("PER006", "ROBERT"),
    ("PER007", "RICHARD"),
    ("PER008", "DURAND"),
    ("PER009", "DUBOIS"),
    ("PER010", "MOREAU");




INSERT INTO
    PLATEFORME
VALUES
    ("PLA001", "LesDino", 20, 100.50, 1),
    ("PLA002", "FossilLab", 15, 85.25, 2),
    ("PLA003", "DinoCenter", 25, 120.75, 1),
    ("PLA004", "PaleoStation", 18, 95.00, 3),
    ("PLA005", "JurassicLab", 22, 110.30, 2),
    ("PLA006", "CretaceousHub", 30, 140.80, 1),
    ("PLA007", "TriassicBase", 12, 75.60, 4),
    ("PLA008", "MesozoicCenter", 28, 135.20, 2),
    ("PLA009", "DinoTech", 16, 88.90, 3),
    ("PLA010", "FossilWorks", 24, 115.45, 1);

INSERT INTO
    MATERIEL
VALUES
    ("M001", "H003", "Pelleteuse"),
    ("M002", "H004", "Truelle"),
    ("M003", "H004", "Pinceau"),
    ("M004", "H003", "Tamis"),
    ("M005", "H003", "Marteau"),
    ("M006", "H002", "Scalpel"),
    ("M007", "H001", "Gants"),
    ("M008", "H005", "Lunettes"),
    ("M009", "H004", "Sac à dos"),
    ("M010", "H006", "Caméra"),
    ("M011", "H003", "GPS");

INSERT INTO
    UTILISER
VALUES
    ("M001", "PLA001"),
    ("M002", "PLA002"),
    ("M003", "PLA003"),
    ("M004", "PLA004"),
    ("M005", "PLA005"),
    ("M006", "PLA006"),
    ("M007", "PLA007"),
    ("M008", "PLA008"),
    ("M009", "PLA009"),
    ("M010", "PLA010"),
    ("M011", "PLA001");

INSERT INTO
    NECESSITER
VALUES
    ("H001", "PLA001"),
    ("H002", "PLA002"),
    ("H003", "PLA003"),
    ("H004", "PLA004"),
    ("H005", "PLA005"),
    ("H006", "PLA006"),
    ("H007", "PLA007"),
    ("H008", "PLA008"),
    ("H009", "PLA009"),
    ("H010", "PLA010");

INSERT INTO
    SPECIALISER_EN
VALUES
    ("H001", "PER001"),
    ("H002", "PER002"),
    ("H003", "PER003"),
    ("H004", "PER004"),
    ("H005", "PER005"),
    ("H006", "PER006"),
    ("H007", "PER007"),
    ("H008", "PER008"),
    ("H009", "PER009"),
    ("H010", "PER010");

INSERT INTO
    SEQUENCE
VALUES
    ("S001"),
    ("S002"),
    ("S003"),
    ("S004"),
    ("S005"),
    ("S006"),
    ("S007"),
    ("S008"),
    ("S009"),
    ("S010");

INSERT INTO
    ECHANTILLION
VALUES
    ("ECH001", "S001", "Échantillon d'un T-Rex"),
    ("ECH002", "S002", "Échantillon de Tricératops"),
    ("ECH003", "S003", "Échantillon de Vélociraptor"),
    ("ECH004", "S004", "Échantillon de Brachiosaure"),
    ("ECH005", "S005", "Échantillon de Stégosaure"),
    ("ECH006", "S006", "Échantillon d'Allosaure"),
    ("ECH007", "S007", "Échantillon de Diplodocus"),
    ("ECH008", "S008", "Échantillon de Ptéranodon"),
    ("ECH009", "S009", "Échantillon d'Ankylosaure"),
    ("ECH010", "S010", "Échantillon de Spinosaure");

INSERT INTO
    CAMPAGNE
VALUES
    ("C001", "PLA001", "LaOuYaDino", 2, '2025-09-11'),
    ("C002", "PLA002", "ValleeFossile", 3, '2025-10-15'),
    ("C003", "PLA003", "CanyonPrehistoire", 1, '2025-11-20'),
    ("C004", "PLA004", "CollineCretace", 4, '2025-08-05'),
    ("C005", "PLA005", "DesertJurassique", 2, '2025-12-03'),
    ("C006", "PLA006", "ForetTriassique", 5, '2025-07-18'),
    ("C007", "PLA007", "RiviereFossile", 3, '2025-06-22'),
    ("C008", "PLA008", "MontagnesDino", 2, '2025-05-14'),
    ("C009", "PLA009", "PlainePaleonto", 1, '2025-04-28'),
    ("C010", "PLA010", "LacPrehistoire", 4, '2025-03-12');

INSERT INTO
    PARTICIPER
VALUES
    ("PER001", "C001"),
    ("PER002", "C002"),
    ("PER003", "C003"),
    ("PER004", "C004"),
    ("PER005", "C005"),
    ("PER006", "C006"),
    ("PER007", "C007"),
    ("PER008", "C008"),
    ("PER009", "C009"),
    ("PER010", "C010");

INSERT INTO
    EXTRAIRE
VALUES
    ("S001", "C001"),
    ("S002", "C002"),
    ("S003", "C003"),
    ("S004", "C004"),
    ("S005", "C005"),
    ("S006", "C006"),
    ("S007", "C007"),
    ("S008", "C008"),
    ("S009", "C009"),
    ("S010", "C010");

INSERT INTO
    ESPECE
VALUES
    ("ESP001", "S001", "T-Rex"),
    ("ESP002", "S002", "Tricératops"),
    ("ESP003", "S003", "Vélociraptor"),
    ("ESP004", "S004", "Brachiosaure"),
    ("ESP005", "S005", "Stégosaure"),
    ("ESP006", "S006", "Allosaure"),
    ("ESP007", "S007", "Diplodocus"),
    ("ESP008", "S008", "Ptéranodon"),
    ("ESP009", "S009", "Ankylosaure"),
    ("ESP010", "S010", "Spinosaure");