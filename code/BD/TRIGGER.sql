-- Creation des Trigger

delimiter |
CREATE OR REPLACE TRIGGER bonne_habilite 
BEFORE INSERT ON PARTICIPER FOR EACH ROW 
BEGIN     
DECLARE habCamp VARCHAR(10);
DECLARE fini boolean DEFAULT FALSE;
DECLARE cursCamp CURSOR FOR SELECT id_hab FROM CAMPAGNE natural join PLATEFORME natural join NECESSITER WHERE id_camp = NEW.id_camp;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
OPEN cursCamp;
read_loop : LOOP
    FETCH cursCamp into habCamp; 
    IF fini THEN
        LEAVE read_loop;
    END IF;     
    IF(habCamp not in(SELECT id_hab FROM SPECIALISER_EN WHERE id_pers = new.id_pers)) THEN
        signal SQLSTATE '45000' set MESSAGE_TEXT = "Le personel ne possède pas l'une des habilitation requise pour la plateforme."; 
    END IF; 
END LOOP;
end|

CREATE OR REPLACE TRIGGER verif_personnel_affecte 
BEFORE INSERT ON PARTICIPER FOR EACH ROW 
begin 
    declare date_camp date;
    declare duree_camp float;
    declare date_ajoutee date;
    declare date_fin_camp date;
    declare fini boolean DEFAULT FALSE;
    
    declare curs_personnel CURSOR FOR 
        SELECT c.date_deb_camp, c.duree 
        FROM CAMPAGNE c 
        NATURAL JOIN PARTICIPER p 
        WHERE p.id_pers = NEW.id_pers;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;

    SELECT date_deb_camp INTO date_ajoutee FROM CAMPAGNE WHERE id_camp = NEW.id_camp;

    OPEN curs_personnel; 
    
    read_loop: LOOP
        FETCH curs_personnel INTO date_camp, duree_camp;
        
        IF fini THEN
            LEAVE read_loop;
        END IF;        
        
        SET date_fin_camp = DATE_ADD(date_camp, INTERVAL duree_camp DAY);        
        
        IF (date_ajoutee >= date_camp AND date_ajoutee <= date_fin_camp) THEN 
            signal SQLSTATE '45000' set MESSAGE_TEXT = 'Le personnel est déjà affecté à une autre campagne pendant cette période.';
        END IF; 
        
    END LOOP;
    
    CLOSE curs_personnel;
end |

CREATE OR REPLACE TRIGGER verif_plateforme_affecte 
BEFORE INSERT ON CAMPAGNE FOR EACH ROW 
begin 
    declare date_camp date;
    declare duree_camp float;
    declare date_fin_camp date;
    declare nouv_date_fin date;
    declare fini boolean DEFAULT FALSE;
    
    declare curs_plateforme CURSOR FOR 
        SELECT c.date_deb_camp, c.duree 
        FROM CAMPAGNE c 
        WHERE c.id_pla = NEW.id_pla;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
    OPEN curs_plateforme; 
    read_loop: LOOP
        FETCH curs_plateforme INTO date_camp, duree_camp;
        
        IF fini THEN
            LEAVE read_loop;
        END IF;        

        SET date_fin_camp = DATE_ADD(date_camp, INTERVAL duree_camp DAY);        
        SET nouv_date_fin =  DATE_ADD(NEW.date_deb_camp, INTERVAL NEW.duree DAY); 

        IF (NEW.date_deb_camp >= date_camp AND NEW.date_deb_camp <= date_fin_camp) OR (nouv_date_fin >= date_camp AND nouv_date_fin <= date_fin_camp) THEN 
            signal SQLSTATE '45000' set MESSAGE_TEXT = 'La plateforme est déjà affecté à une autre campagne pendant cette période.';
        END IF; 
        
    END LOOP;
    
    CLOSE curs_plateforme;
end |

create or replace TRIGGER verif_nb_pers BEFORE INSERT 
ON CAMPAGNE FOR EACH ROW 
begin 
    declare nb_pers int;
    SELECT count(*) into nb_pers FROM PARTICIPER WHERE id_camp = NEW.id_camp;
    IF nb_pers < (SELECT nb_pers_nec FROM CAMPAGNE natural join PLATEFORME WHERE id_camp = NEW.id_camp) 
    THEN
    signal SQLSTATE '45000' set MESSAGE_TEXT = 'Le nombre de personne essayant de participer est trop faible'; 
    END IF;
end |

create or replace PROCEDURE maj_maintenance_plateform(la_plat varchar(10), maj_duree int) begin 
declare duree_acc int;
SELECT jours_av_mainte into duree_acc FROM PLATEFORME WHERE id_pla = la_plat;
IF((duree_acc >= maj_duree)) THEN
    UPDATE PLATEFORME 
    SET jours_av_mainte = jours_av_mainte - maj_duree
    WHERE id_pla = la_plat;
ELSE 
    UPDATE PLATEFORME 
    SET jours_av_mainte = inter_mainte - maj_duree 
    WHERE id_pla = la_plat;
END IF;

end |

CREATE OR REPLACE TRIGGER verif_duree_plateforme
BEFORE INSERT ON CAMPAGNE FOR EACH ROW 
begin
call maj_maintenance_plateform(NEW.id_pla,NEW.duree);
end |

CREATE OR REPLACE TRIGGER respectBudget BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    declare mes VARCHAR(200);
    declare cout_total_camp FLOAT DEFAULT 0;
    declare budget FLOAT;
    declare new_cout_jour FLOAT;

    SELECT cout_exploi_jour into new_cout_jour FROM PLATEFORME WHERE id_pla = NEW.id_pla;
    SELECT valeur into budget FROM BUDGET WHERE id_budg = NEW.id_budg; 

    SELECT sum(cout_exploi_jour*duree) into cout_total_camp 
    FROM CAMPAGNE c JOIN PLATEFORME p ON c.id_pla = p.id_pla 
    WHERE c.id_budg = NEW.id_budg;
    
    IF cout_total_camp IS NULL THEN
        SET cout_total_camp = 0;
    END IF;
    
    IF cout_total_camp + NEW.duree*new_cout_jour > budget then
        set mes = concat("Insertion impossible, la campagne est hors budget. Budget couvert : ", cout_total_camp, "/", budget);
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    END IF;
END |

delimiter ;