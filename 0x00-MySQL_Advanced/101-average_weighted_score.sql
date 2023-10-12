-- creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN

DECLARE done INT DEFAULT 0;
DECLARE user_id INT;
DECLARE weighted_avg FLOAT;
DECLARE curUserId CURSOR FOR SELECT id FROM users;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

OPEN curUserId;

computeAvg: LOOP
    FETCH curUserId INTO user_id;

    IF done = 1 THEN
        LEAVE computeAvg;
    END IF;

    -- Compute weighted average and update the user's average_score
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

END LOOP computeAvg;

CLOSE curUserId;

END$$

DELIMITER ;
