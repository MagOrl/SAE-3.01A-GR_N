-- Creation des tables

CREATE TABLE
    HABILITATION (id_hab varchar(10) primary key, nom_hab varchar(20));

CREATE TABLE
    PERSONNEL (
        id_pers varchar(10) primary key,
        nom_pers varchar(20)
    );

CREATE TABLE
    PLATEFORME (
        id_pla varchar(10) primary key,
        nom_pla varchar(20),
        nb_pers_nec int,
        cout_exploi_jour decimal(10, 2),
        inter_mainte int
    );

CREATE TABLE
    MATERIEL (
        id_mat varchar(10) primary key,
        id_hab varchar(10),
        nom_mat varchar(20),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab)
    );

CREATE TABLE
    UTILISER (
        id_mat varchar(10),
        id_pla varchar(10),
        primary key (id_mat, id_pla),
        FOREIGN KEY (id_mat) REFERENCES MATERIEL (id_mat),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
    );

CREATE TABLE
    NECESSITER (
        id_hab varchar(10),
        id_pla varchar(10),
        primary key (id_hab, id_pla),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
    );

CREATE TABLE
    SPECIALISER_EN (
        id_hab varchar(10),
        id_pers varchar(10),
        primary key (id_hab, id_pers),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (id_pers) REFERENCES PERSONNEL (id_pers)
    );

CREATE TABLE
    BUDGET (
        id_budg varchar(10) primary key,
        valeur float,
        date_deb_mois date
    );

CREATE TABLE
    CAMPAGNE (
        id_camp varchar(10),
        id_pla varchar(10),
        nom_lieu_fouille varchar(20),
        duree float,
        jma date,
        id_budg varchar(10),
        primary key (id_camp),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla),
        FOREIGN KEY (id_budg) REFERENCES BUDGET (id_budg)
    );

CREATE TABLE
    PARTICIPER (
        id_pers varchar(10),
        id_camp varchar(10),
        primary key (id_pers, id_camp),
        FOREIGN KEY (id_pers) REFERENCES PERSONNEL (id_pers),
        FOREIGN KEY (id_camp) REFERENCES CAMPAGNE (id_camp)
    );

CREATE TABLE
    SEQUENCE (
        id_seq varchar(10) primary key,
        nom_fichier varchar(20)
    );

CREATE TABLE
    EXTRAIRE (
        id_seq varchar(10),
        id_camp varchar(10),
        primary key (id_camp, id_seq),
        FOREIGN KEY (id_camp) REFERENCES CAMPAGNE (id_camp),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

CREATE TABLE
    ESPECE (
        id_esp varchar(10) primary key,
        id_seq varchar(10),
        nom_esp varchar(40),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

CREATE TABLE
    ECHANTILLION (
        id_ech varchar(10) primary key,
        id_seq varchar(10),
        commentaire varchar(255),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

-- Creation des Trigger

delimiter //
CREATE OR REPLACE TRIGGER bonne_habilite 
BEFORE INSERT ON PARTICIPER FOR EACH ROW 
BEGIN 
    IF ((SELECT id_hab FROM PERSONNEL NATURAL JOIN SPECIALISER_EN WHERE id_pers = NEW.id_pers) != (SELECT id_hab FROM CAMPAGNE NATURAL JOIN PLATEFORME NATURAL JOIN NECESSITER WHERE id_camp = NEW.id_camp))
    THEN 
        signal SQLSTATE '45000' SET MESSAGE_TEXT = 'Pas la bonne habilité pour le personel.';
    END IF;
END //
delimiter ;