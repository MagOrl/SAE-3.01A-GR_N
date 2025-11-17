-- Triggers et procédure de gestion (version nettoyée)

CREATE OR REPLACE TRIGGER bonne_habilite
BEFORE INSERT ON PARTICIPER FOR EACH ROW
BEGIN
    DECLARE habCamp VARCHAR(10);
    DECLARE fini BOOLEAN DEFAULT FALSE;
    DECLARE cursCamp CURSOR FOR
        SELECT id_hab
        FROM CAMPAGNE
        NATURAL JOIN PLATEFORME
        NATURAL JOIN NECESSITER
        WHERE id_camp = NEW.id_camp;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
    OPEN cursCamp;
    read_loop: LOOP
        FETCH cursCamp INTO habCamp;
        IF fini THEN LEAVE read_loop; END IF;
        IF habCamp NOT IN (SELECT id_hab FROM SPECIALISER_EN WHERE id_pers = NEW.id_pers) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le personnel ne possède pas une habilitation requise pour la plateforme.';
        END IF;
    END LOOP;
    CLOSE cursCamp;
END;

CREATE OR REPLACE TRIGGER verif_personnel_affecte
BEFORE INSERT ON PARTICIPER FOR EACH ROW
BEGIN
    DECLARE date_camp DATE;
    DECLARE duree_camp FLOAT;
    DECLARE date_ajoutee DATE;
    DECLARE date_fin_camp DATE;
    DECLARE fini BOOLEAN DEFAULT FALSE;
    DECLARE curs_personnel CURSOR FOR
        SELECT c.date_deb_camp, c.duree
        FROM CAMPAGNE c
        NATURAL JOIN PARTICIPER p
        WHERE p.id_pers = NEW.id_pers;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
    SELECT date_deb_camp INTO date_ajoutee FROM CAMPAGNE WHERE id_camp = NEW.id_camp;
    OPEN curs_personnel;
    read_loop: LOOP
        FETCH curs_personnel INTO date_camp, duree_camp;
        IF fini THEN LEAVE read_loop; END IF;
        SET date_fin_camp = DATE_ADD(date_camp, INTERVAL duree_camp DAY);
        IF date_ajoutee BETWEEN date_camp AND date_fin_camp THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le personnel est déjà affecté à une autre campagne pendant cette période.';
        END IF;
    END LOOP;
    CLOSE curs_personnel;
END;

CREATE OR REPLACE TRIGGER verif_plateforme_affecte
BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    DECLARE date_camp DATE;
    DECLARE duree_camp FLOAT;
    DECLARE date_fin_camp DATE;
    DECLARE nouv_date_fin DATE;
    DECLARE fini BOOLEAN DEFAULT FALSE;
    DECLARE curs_plateforme CURSOR FOR
        SELECT c.date_deb_camp, c.duree
        FROM CAMPAGNE c
        WHERE c.id_pla = NEW.id_pla;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
    OPEN curs_plateforme;
    read_loop: LOOP
        FETCH curs_plateforme INTO date_camp, duree_camp;
        IF fini THEN LEAVE read_loop; END IF;
        SET date_fin_camp = DATE_ADD(date_camp, INTERVAL duree_camp DAY);
        SET nouv_date_fin = DATE_ADD(NEW.date_deb_camp, INTERVAL NEW.duree DAY);
        IF (NEW.date_deb_camp BETWEEN date_camp AND date_fin_camp)
           OR (nouv_date_fin BETWEEN date_camp AND date_fin_camp) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La plateforme est déjà affectée à une autre campagne pendant cette période.';
        END IF;
    END LOOP;
    CLOSE curs_plateforme;
END;

CREATE OR REPLACE TRIGGER verif_nb_pers
BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    DECLARE nb_pers INT;
    SELECT COUNT(*) INTO nb_pers FROM PARTICIPER WHERE id_camp = NEW.id_camp;
    IF nb_pers < (SELECT nb_pers_nec FROM CAMPAGNE NATURAL JOIN PLATEFORME WHERE id_camp = NEW.id_camp) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nombre de personnes insuffisant pour la campagne.';
    END IF;
END;

CREATE OR REPLACE PROCEDURE maj_maintenance_plateform(la_plat VARCHAR(10), maj_duree INT)
BEGIN
    DECLARE duree_acc INT;
    SELECT jours_av_mainte INTO duree_acc FROM PLATEFORME WHERE id_pla = la_plat;
    IF duree_acc >= maj_duree THEN
        UPDATE PLATEFORME
        SET jours_av_mainte = jours_av_mainte - maj_duree
        WHERE id_pla = la_plat;
    ELSE
        UPDATE PLATEFORME
        SET jours_av_mainte = inter_mainte - maj_duree
        WHERE id_pla = la_plat;
    END IF;
END;

CREATE OR REPLACE TRIGGER verif_duree_plateforme
BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    CALL maj_maintenance_plateform(NEW.id_pla, NEW.duree);
END;

CREATE OR REPLACE TRIGGER respectBudget
BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    DECLARE mes VARCHAR(200);
    DECLARE cout_total_camp FLOAT DEFAULT 0;
    DECLARE budget FLOAT;
    DECLARE new_cout_jour FLOAT;
    SELECT cout_exploi_jour INTO new_cout_jour FROM PLATEFORME WHERE id_pla = NEW.id_pla;
    SELECT valeur INTO budget FROM BUDGET WHERE id_budg = NEW.id_budg;
    SELECT SUM(cout_exploi_jour * duree) INTO cout_total_camp
    FROM CAMPAGNE c JOIN PLATEFORME p ON c.id_pla = p.id_pla
    WHERE c.id_budg = NEW.id_budg;
    IF cout_total_camp IS NULL THEN SET cout_total_camp = 0; END IF;
    IF cout_total_camp + NEW.duree * new_cout_jour > budget THEN
        SET mes = CONCAT('Insertion impossible, la campagne est hors budget. Budget couvert : ', cout_total_camp, '/', budget);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
    END IF;
END;