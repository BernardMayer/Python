-- 
-- La pattern '\v' devrait etre \p{Cntrl}, mais teradata declenche une erreur 9134 not valid pattern
-- , 1 a partir du premier caractere
-- , 0 toute les occurences
-- , 'i' ignore la casse ('c' respect de la casse)
-- 
-- select  max(length(objectscript_script )) FROM objectscript_fwk retourne un peu moins de 26000

--DATABASE dmup10meta_tec_fwk_0;
DATABASE dzuda0meta_tec_fwk_0;

-- Liste des requêtes
SELECT 
object_name, 
--REGEXP_REPLACE(CAST(objectscript_script AS VARCHAR(4000)), '\v', ' ', 1, 0, 'c' ) AS requete
--REGEXP_REPLACE(REGEXP_REPLACE(CAST(objectscript_script AS VARCHAR(4000)), '\v', ' ', 1, 0, 'c' ), '\s{1,}', ' ', 1, 0, 'c') AS requete
REGEXP_REPLACE(REGEXP_REPLACE(CAST(objectscript_script AS CLOB), '\v', ' ', 1, 0, 'c' ), '\s{1,}', ' ', 1, 0, 'c') AS requete
FROM objectscript_fwk
JOIN object_fwk
	ON object_fwk.object_code = objectscript_fwk.object_code
JOIN scripttype_fwk
	ON scripttype_fwk.scripttype_id = objectscript_fwk.scripttype_id
WHERE 
scripttype_code = 'QRY'
AND datasource_id = 3;

 
-- Liste des liens requête job
SELECT 
src.object_name, 
tgt.object_alias_name AS job_name
FROM objectjoin_fwk
JOIN object_fwk AS tgt
	ON tgt.object_code = objectjoin_fwk.object_code
JOIN object_fwk AS src
	ON src.object_code = objectjoin_fwk.object_code_from
JOIN flux_object_fwk
	ON flux_object_fwk.object_code = tgt.object_code
JOIN module_fwk
	ON flux_object_fwk.module_id = module_fwk.module_id
JOIN module_job_fwk
	ON module_job_fwk.module_id = module_fwk.module_id
JOIN job_fwk
	ON module_job_fwk.job_id = job_fwk.job_id
WHERE 
jointype_id = 1
AND job_code IN ('JN21', 'JS21', 'JS22');
