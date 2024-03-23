-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE OR  REPLACE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_user_id INT;
    DECLARE v_total_score DECIMAL(10, 2);
    DECLARE v_total_weight DECIMAL(10, 2);
    DECLARE v_average_score DECIMAL(10, 2);

    -- Declare cursor for iterating over users
    DECLARE cur CURSOR FOR
        SELECT id FROM users;

    -- Declare continue handler to exit loop when no more rows
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Start looping over users
    user_loop: LOOP
        FETCH cur INTO v_user_id;
	IF done THEN
	    LEAVE user_loop;
        END IF;

	-- Calculate the total weighted score and the total weight
        SELECT SUM(score * weight), SUM(weight)
	INTO v_total_score, v_total_weight
	FROM scores
	WHERE user_id = v_user_id;

	-- Calculate the average weighted score
        IF v_total_weight > 0 THEN
	    SET v_average_score = v_total_score / v_total_weight;
        ELSE
	    SET v_average_score = 0;
        END IF;

	-- Store the average weighted score in the database
        UPDATE users
	SET average_weighted_score = v_average_score
	WHERE id = v_user_id;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END//

DELIMITER ;
