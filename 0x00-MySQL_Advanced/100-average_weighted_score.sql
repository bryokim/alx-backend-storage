-- Creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER $$ ;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT) BEGIN DECLARE weighted_avg FLOAT;

SELECT
    SUM(sw) / SUM(w) INTO weighted_avg
FROM
    (
        SELECT
            p.weight as w,
            (c.score * p.weight) as sw
        FROM
            corrections c
            INNER JOIN projects p ON c.project_id = p.id
        WHERE
            c.user_id = user_id
    ) AS T;

UPDATE users
SET
    average_score = weighted_avg
WHERE
    id = user_id;

END$$

DELIMITER ; $$
