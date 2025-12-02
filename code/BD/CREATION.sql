DROP TABLE IF EXISTS ESPECE;

DROP TABLE IF EXISTS EXTRAIRE;

DROP TABLE IF EXISTS ECHANTILLON; 

DROP TABLE IF EXISTS SEQUENCE;

DROP TABLE IF EXISTS PARTICIPER;

DROP TABLE IF EXISTS CAMPAGNE;

DROP TABLE IF EXISTS BUDGET;

DROP TABLE IF EXISTS SPECIALISER_EN;

DROP TABLE IF EXISTS NECESSITER;

DROP TABLE IF EXISTS UTILISER;

DROP TABLE IF EXISTS OPERATION_MAINTENANCE;

DROP TABLE IF EXISTS MAINTENANCE;

DROP TABLE IF EXISTS MATERIEL;

DROP TABLE IF EXISTS PLATEFORME;

DROP TABLE IF EXISTS PERSONNEL;

DROP TABLE IF EXISTS HABILITATION;

CREATE TABLE
    HABILITATION (
        id_hab VARCHAR(10) PRIMARY KEY, 
        nom_hab VARCHAR(20)
    );

CREATE TABLE
    PERSONNEL (
        Id_pers VARCHAR(10) PRIMARY KEY,
        nom_pers VARCHAR(20)
    );

CREATE TABLE
    PLATEFORME (
        id_pla VARCHAR(10) PRIMARY KEY,
        nom_pla VARCHAR(20),
        nb_pers_nec INT,
        cout_exploi_jour FLOAT,
        inter_mainte INT /*intervalle de maintenance en jours*/
    );

CREATE TABLE
    MAINTENANCE (
        id_maint VARCHAR(10) PRIMARY KEY,
        id_pla VARCHAR(10),
        date_deb_maint DATE,
        date_fin_maint DATE,
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
    );

CREATE TABLE
    OPERATION_MAINTENANCE (
        id_op_maint VARCHAR(10) PRIMARY KEY,
        id_pla VARCHAR(10),
        date_maintenance DATE,
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
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
        id_hab VARCHAR(10),
        id_pla VARCHAR(10),
        PRIMARY KEY (id_hab, id_pla),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla)
    );

CREATE TABLE
    SPECIALISER_EN (
        id_hab VARCHAR(10),
        Id_pers VARCHAR(10),
        PRIMARY KEY (id_hab, Id_pers),
        FOREIGN KEY (id_hab) REFERENCES HABILITATION (id_hab),
        FOREIGN KEY (Id_pers) REFERENCES PERSONNEL (Id_pers)
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
        id_pla VARCHAR(10),
        id_budg VARCHAR(10),
        FOREIGN KEY (id_pla) REFERENCES PLATEFORME (id_pla),
        FOREIGN KEY (id_budg) REFERENCES BUDGET (id_budg)
    );

CREATE TABLE
    PARTICIPER (
        Id_pers VARCHAR(10),
        id_camp VARCHAR(10),
        PRIMARY KEY (Id_pers, id_camp),
        FOREIGN KEY (Id_pers) REFERENCES PERSONNEL (Id_pers),
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
        nom_esp VARCHAR(40),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );

CREATE TABLE
    ECHANTILLON (
        id_ech VARCHAR(10) PRIMARY KEY,
        id_seq VARCHAR(10),
        commentaire VARCHAR(255),
        FOREIGN KEY (id_seq) REFERENCES SEQUENCE (id_seq)
    );


