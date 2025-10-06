-- Tests autonomes pour tous les triggers (assistée avec l'aide de l'IA)
-- =============================================================================
-- TEST 1: TRIGGER bonne_habilite
-- =============================================================================

-- Nettoyage
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM BUDGET;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

-- Données pour test 1
INSERT INTO HABILITATION VALUES ("H001", "Chimique"), ("H002", "Biologique");
INSERT INTO PERSONNEL VALUES ("PER001", "MARTIN"), ("PER002", "DUPONT");
INSERT INTO PLATEFORME VALUES ("PLA001", "DinoLab", 2, 100.00, 30, 90);
INSERT INTO NECESSITER VALUES ("H001", "PLA001"), ("H002", "PLA001");
INSERT INTO SPECIALISER_EN VALUES ("H001", "PER001"), ("H002", "PER001"); -- PER001 a les bonnes habilitations
-- PER002 n'a aucune habilitation
INSERT INTO BUDGET VALUES ("B001", 1000.00, '2025-09-01');
INSERT INTO CAMPAGNE VALUES ("C001", 2, '2025-09-15', "PLA001", "B001");

SELECT "=== TEST 1: bonne_habilite ===" as Info;
-- Test qui PASSE
INSERT INTO PARTICIPER VALUES ("PER001", "C001");
SELECT "PER001 ajouté avec succès" as Resultat;

-- Test qui ÉCHOUE
--  INSERT INTO PARTICIPER VALUES ("PER002", "C001"); -- Décommentez pour tester l'échec

-- =============================================================================
-- TEST 2: TRIGGER verif_personnel_affecte
-- =============================================================================

-- Nettoyage
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM BUDGET;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

-- Données pour test 2
INSERT INTO HABILITATION VALUES ("H001", "Chimique");
INSERT INTO PERSONNEL VALUES ("PER001", "MARTIN");
INSERT INTO PLATEFORME VALUES ("PLA001", "DinoLab", 1, 100.00, 30, 90), ("PLA002", "FossilCenter", 1, 85.50, 30, 60);
INSERT INTO NECESSITER VALUES ("H001", "PLA001"), ("H001", "PLA002");
INSERT INTO SPECIALISER_EN VALUES ("H001", "PER001");
INSERT INTO BUDGET VALUES ("B001", 1000.00, '2025-09-01'), ("B002", 500.00, '2025-10-01');
INSERT INTO CAMPAGNE VALUES ("C001", 2, '2025-09-15', "PLA001", "B001"); -- Du 15 au 17 sept
INSERT INTO PARTICIPER VALUES ("PER001", "C001");

SELECT "=== TEST 2: verif_personnel_affecte ===" as Info;
-- Test qui PASSE (pas de conflit)
INSERT INTO CAMPAGNE VALUES ("C002", 1, '2025-10-20', "PLA002", "B002");
INSERT INTO PARTICIPER VALUES ("PER001", "C002");
SELECT "PER001 ajouté sur C002 sans conflit" as Resultat;

-- Test qui ÉCHOUE (conflit de dates)
INSERT INTO CAMPAGNE VALUES ("C003", 1, '2025-09-16', "PLA002", "B002"); -- Conflit avec C001
-- INSERT INTO PARTICIPER VALUES ("PER001", "C003"); -- Décommentez pour tester l'échec

-- =============================================================================
-- TEST 3: TRIGGER verif_plateforme_affecte
-- =============================================================================

-- Nettoyage
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM BUDGET;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

-- Données pour test 3
INSERT INTO PLATEFORME VALUES ("PLA001", "DinoLab", 1, 100.00, 30, 90);
INSERT INTO BUDGET VALUES ("B001", 1000.00, '2025-09-01'), ("B002", 500.00, '2025-10-01');
INSERT INTO CAMPAGNE VALUES ("C001", 2, '2025-09-15', "PLA001", "B001"); -- PLA001 occupée du 15 au 17

SELECT "=== TEST 3: verif_plateforme_affecte ===" as Info;
-- Test qui PASSE (pas de conflit)
INSERT INTO CAMPAGNE VALUES ("C002", 1, '2025-10-20', "PLA001", "B002");
SELECT "C002 créée sans conflit" as Resultat;

-- Test qui ÉCHOUE (conflit de dates)
-- INSERT INTO CAMPAGNE VALUES ("C003", 1, '2025-09-16', "PLA001", "B002"); -- Décommentez pour tester l'échec

-- =============================================================================
-- TEST 4: TRIGGER respectBudget
-- =============================================================================

-- Nettoyage
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM BUDGET;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

-- Données pour test 4
INSERT INTO PLATEFORME VALUES ("PLA001", "DinoLab", 1, 100.00, 30, 90); -- 100€/jour
INSERT INTO BUDGET VALUES ("B001", 1000.00, '2025-09-01'), ("B002", 500.00, '2025-10-01');

SELECT "=== TEST 4: respectBudget ===" as Info;
-- Test qui PASSE (budget suffisant)
INSERT INTO CAMPAGNE VALUES ("C001", 3, '2025-09-15', "PLA001", "B001"); -- 300€ sur budget de 1000€
SELECT "C001 créée, budget respecté" as Resultat;

-- Ajoutons une autre campagne pour voir le budget couvert
INSERT INTO CAMPAGNE VALUES ("C002", 2, '2025-09-20', "PLA001", "B001"); -- +200€ = 500€ total
SELECT "C002 créée, budget couvert maintenant 500€/1000€" as Resultat;

-- Test qui ÉCHOUE (budget dépassé) - maintenant on a déjà 500€ utilisés
-- INSERT INTO CAMPAGNE VALUES ("C003", 6, '2025-09-25', "PLA001", "B001"); -- +600€ = 1100€ total > 1000€

-- =============================================================================
-- TE0.T 5: TRIGGER verif_duree_plateforme (maintenance)
-- =============================================================================

-- Nettoyage
DELETE FROM PARTICIPER;
DELETE FROM CAMPAGNE;
DELETE FROM BUDGET;
DELETE FROM SPECIALISER_EN;
DELETE FROM NECESSITER;
DELETE FROM PLATEFORME;
DELETE FROM PERSONNEL;
DELETE FROM HABILITATION;

-- Données pour test 5
INSERT INTO PLATEFORME VALUES ("PLA001", "DinoLab", 1, 100.00, 30, 90); -- 90 jours avant maintenance
INSERT INTO BUDGET VALUES ("B001", 1000.00, '2025-09-01');

SELECT "=== TEST 5: verif_duree_plateforme ===" as Info;
SELECT "Maintenance avant:", jours_av_mainte FROM PLATEFORME WHERE id_pla = "PLA001";
INSERT INTO CAMPAGNE VALUES ("C001", 5, '2025-09-15', "PLA001", "B001"); -- Utilise 5 jours
SELECT "Maintenance après:", jours_av_mainte FROM PLATEFORME WHERE id_pla = "PLA001";

-- =============================================================================
-- RÉSUMÉ DES TESTS
-- =============================================================================

SELECT "=== TOUS LES TESTS TERMINÉS ===" as Info;
SELECT "Pour tester les échecs, décommentez les lignes marquées dans chaque section" as Instructions;