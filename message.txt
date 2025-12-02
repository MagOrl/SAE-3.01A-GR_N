-- Jeu de donnees adapte au nouveau modele SQLAlchemy (IDs numeriques, noms de tables inferes)
-- Purge ordonnee (enfants -> parents)
DELETE FROM extraire;
DELETE FROM participer;
DELETE FROM espece;
DELETE FROM echantillon;
DELETE FROM sequence;
DELETE FROM campagne;
DELETE FROM specialiser_en;
DELETE FROM necessiter;
DELETE FROM utiliser;
DELETE FROM materiel;
DELETE FROM operation_maintenance;
DELETE FROM maintenance;
DELETE FROM plateforme;
DELETE FROM budget;
DELETE FROM personnel;
DELETE FROM habilitation;

INSERT INTO habilitation (id_hab, nom_hab) VALUES
    (1, 'Chimique'),
    (2, 'Biologique'),
    (3, 'Geologique'),
    (4, 'Paleontologique'),
    (5, 'Radiologique'),
    (6, 'Microscopique'),
    (7, 'Spectroscopique'),
    (8, 'Cristallographique'),
    (9, 'Immunologique'),
    (10, 'Moleculaire');

INSERT INTO personnel (Id_pers, nom_pers) VALUES
    (1, 'LEROY'),
    (2, 'MARTIN'),
    (3, 'BERNARD'),
    (4, 'THOMAS'),
    (5, 'PETIT'),
    (6, 'ROBERT'),
    (7, 'RICHARD'),
    (8, 'DURAND'),
    (9, 'DUBOIS'),
    (10, 'MOREAU');

INSERT INTO plateforme (id_pla, nom_pla, nb_pers_nec, cout_exploi_jour, inter_mainte, jours_av_mainte) VALUES
    (1, 'LesDino', 20, 100.50, 30, 30),
    (2, 'FossilLab', 15, 85.25, 60, 60),
    (3, 'DinoCenter', 25, 120.75, 30, 30),
    (4, 'PaleoStation', 18, 95.00, 90, 90),
    (5, 'JurassicLab', 22, 110.30, 60, 60),
    (6, 'CretaceousHub', 30, 140.80, 30, 30),
    (7, 'TriassicBase', 12, 75.60, 120, 120),
    (8, 'MesozoicCenter', 28, 135.20, 60, 60),
    (9, 'DinoTech', 16, 88.90, 90, 90),
    (10, 'FossilWorks', 24, 115.45, 30, 30);

INSERT INTO maintenance (id_maint, id_pla, date_deb_maint, date_fin_maint) VALUES
    (1, 1, '2025-12-05', '2025-12-06'),
    (2, 2, '2025-12-15', '2025-12-17'),
    (3, 3, '2025-12-25', '2025-12-26'),
    (4, 4, '2026-01-05', '2026-01-07'),
    (5, 5, '2026-01-15', '2026-01-16'),
    (6, 6, '2026-01-25', '2026-01-27'),
    (7, 7, '2026-02-05', '2026-02-06'),
    (8, 8, '2026-02-15', '2026-02-17'),
    (9, 9, '2026-02-22', '2026-02-23'),
    (10, 10, '2026-02-25', '2026-02-27');

INSERT INTO operation_maintenance (id_op_maint, id_pla, date_maintenance) VALUES
    (1, 1, '2025-12-05'),
    (2, 2, '2025-12-16'),
    (3, 3, '2025-12-25'),
    (4, 4, '2026-01-06'),
    (5, 5, '2026-01-15'),
    (6, 6, '2026-01-26'),
    (7, 7, '2026-02-05'),
    (8, 8, '2026-02-16'),
    (9, 9, '2026-02-22'),
    (10, 10, '2026-02-26');

INSERT INTO materiel (id_mat, id_hab, nom_mat) VALUES
    (1, 3, 'Pelleteuse'),
    (2, 4, 'Truelle'),
    (3, 4, 'Pinceau'),
    (4, 3, 'Tamis'),
    (5, 3, 'Marteau'),
    (6, 2, 'Scalpel'),
    (7, 1, 'Gants'),
    (8, 5, 'Lunettes'),
    (9, 4, 'Sac a dos'),
    (10, 6, 'Camera'),
    (11, 3, 'GPS');

INSERT INTO utiliser (id_mat, id_pla) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 1);

INSERT INTO necessiter (id_hab, id_pla) VALUES
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 1),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO specialiser_en (id_hab, Id_pers) VALUES
    (1, 1),
    (2, 1),
    (1, 2),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO sequence (id_seq, nom_fichier) VALUES
    (1, 'S001.fasta'),
    (2, 'S002.fasta'),
    (3, 'S003.fasta'),
    (4, 'S004.fasta'),
    (5, 'S005.fasta'),
    (6, 'S006.fasta'),
    (7, 'S007.fasta'),
    (8, 'S008.fasta'),
    (9, 'S009.fasta'),
    (10, 'S010.fasta');

INSERT INTO echantillon (id_ech, id_seq, commentaire) VALUES
    (1, 1, 'Echantillon dun T-Rex'),
    (2, 2, 'Echantillon de Triceratops'),
    (3, 3, 'Echantillon de Velociraptor'),
    (4, 4, 'Echantillon de Brachiosaure'),
    (5, 5, 'Echantillon de Stegosaure'),
    (6, 6, 'Echantillon dAllosaure'),
    (7, 7, 'Echantillon de Diplodocus'),
    (8, 8, 'Echantillon de Pteranodon'),
    (9, 9, 'Echantillon dAnkylosaure'),
    (10, 10, 'Echantillon de Spinosaure');

INSERT INTO budget (id_budg, valeur, date_deb_mois) VALUES
    (1, 41999.99, '2025-09-25'),
    (2, 35000.00, '2025-01-15'),
    (3, 28500.50, '2025-02-10'),
    (4, 52000.75, '2025-03-05'),
    (5, 19999.99, '2025-04-20'),
    (6, 67500.25, '2025-05-12'),
    (7, 33250.80, '2025-06-18'),
    (8, 45000.00, '2025-07-03'),
    (9, 58750.45, '2025-08-14'),
    (10, 22000.60, '2025-09-08');

INSERT INTO campagne (id_camp, duree, date_deb_camp, id_pla, id_budg, nom_lieu_fouille) VALUES
    (1, 2, '2025-09-11', 1, 1, 'Site Alpha'),
    (2, 3, '2025-10-15', 2, 2, 'Site Beta'),
    (3, 1, '2025-11-20', 3, 3, 'Site Gamma'),
    (4, 4, '2025-08-05', 4, 4, 'Site Delta'),
    (5, 2, '2025-12-03', 5, 5, 'Site Epsilon'),
    (6, 5, '2025-07-18', 6, 6, 'Site Zeta'),
    (7, 3, '2025-06-22', 7, 7, 'Site Eta'),
    (8, 2, '2025-05-14', 8, 8, 'Site Theta'),
    (9, 1, '2025-04-28', 9, 9, 'Site Iota'),
    (10, 4, '2025-03-12', 10, 10, 'Site Kappa');

INSERT INTO participer (Id_pers, id_camp) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO extraire (id_camp, id_seq) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO espece (id_esp, id_seq, nom_esp) VALUES
    (1, 1, 'T-Rex'),
    (2, 2, 'Triceratops'),
    (3, 3, 'Velociraptor'),
    (4, 4, 'Brachiosaure'),
    (5, 5, 'Stegosaure'),
    (6, 6, 'Allosaure'),
    (7, 7, 'Diplodocus'),
    (8, 8, 'Pteranodon'),
    (9, 9, 'Ankylosaure'),
    (10, 10, 'Spinosaure');
