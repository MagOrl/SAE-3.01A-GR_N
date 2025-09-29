CREATE TABLE
    HABILITATION (
        id_hab VARCHAR(10) PRIMARY KEY, 
        nom_hab VARCHAR(20)
    );

CREATE TABLE
    PERSONNEL (
        id_pers VARCHAR(10) PRIMARY KEY,
        nom_pers VARCHAR(20)
    );

CREATE TABLE
    PLATEFORME (
        id_pla VARCHAR(10) PRIMARY KEY,
        nom_pla VARCHAR(20),
        nb_pers_nec INT,
        cout_exploi_jour INT,
        inter_mainte INT,
        jours_av_mainte INT
    );

CREATE TABLE
    NECESSITER (
        id_hab VARCHAR(10),
        id_pla VARCHAR(10),
        PRIMARY KEY (id_hab, id_pla),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
    );

CREATE TABLE
    SPECIALISER_EN (
        id_hab VARCHAR(10),
        id_pers VARCHAR(10),
        PRIMARY KEY (id_hab, id_pers),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (id_pers) REFERENCES PERSONNEL (id_pers)
    );

CREATE TABLE
    BUDGET (
        id_budg VARCHAR(10) PRIMARY KEY,
        valeur FLOAT,
        date_deb_mois DATE
    );

CREATE TABLE
    CAMPAGNE (
        id_camp VARCHAR(10) PRIMARY KEY,
        duree INT,
        date_deb_camp DATE,
        cout_realisation FLOAT
        id_pla VARCHAR(10),
        id_budg VARCHAR(10),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla),
        FOREIGN KEY (id_budg) REFERENCES BUDGET (id_budg)
    );

CREATE TABLE
    PARTICIPER (
        id_pers VARCHAR(10),
        id_camp VARCHAR(10),
        PRIMARY KEY (id_pers, id_camp),
        FOREIGN KEY (id_pers) REFERENCES PERSONNEL (id_pers),
        FOREIGN KEY (id_camp) REFERENCES CAMPAGNE (id_camp)
    );

CREATE TABLE
    SEQUENCE (
        id_seq VARCHAR(10) PRIMARY KEY,
        nom_fichier VARCHAR(40)
    );

CREATE TABLE
    EXTRAIRE (
        id_seq VARCHAR(10),
        id_camp VARCHAR(10),
        PRIMARY KEY (id_camp, id_seq),
        FOREIGN KEY (id_camp) REFERENCES CAMPAGNE (id_camp),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

CREATE TABLE
    ESPECE (
        id_esp VARCHAR(10) PRIMARY KEY,
        id_seq VARCHAR(10),
        nom_esp VARCHAR(40)
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

CREATE TABLE
    ECHANTILLON (
        id_ech VARCHAR(10) PRIMARY KEY,
        id_seq VARCHAR(10),
        commentaire VARCHAR(255),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

DELIMITER |
CREATE OR REPLACE TRIGGER respectBudget BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    declare mes VARCHAR(200);
    declare cout_total_camp FLOAT;
    declare budget FLOAT;

    SELECT valeur into budget FROM BUDGET WHERE id_budg = NEW.id_budg; 
    SELECT sum(cout_realisation) into cout_total_camp FROM CAMPAGNE WHERE id_budg = NEW.id_budg;
    IF cout_total_camp + NEW.cout_realisation > budget then
        set mes = concat("Insertion impossible, la campagne est hors budget. \n Budget couvert : ", cout_total_camp, "/", budget)
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    END IF;
END |
