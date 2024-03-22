-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal

DELIMITER //

CREATE OR REPLACE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_total_score DECIMAL(10, 2);
    DECLARE v_total_count INT;
    DECLARE v_average_score DECIMAL(10, 2);

    -- Calculate the total score for the user
    SELECT SUM(score) INTO v_total_score
    FROM corrections
    WHERE user_id = p_user_id;

    -- Count the number of corrections for the user
    SELECT COUNT(*) INTO v_total_count
    FROM corrections
    WHERE user_id = p_user_id;

    -- Calculate the average score
    IF v_total_count > 0 THEN
	SET v_average_score = v_total_score / v_total_count;
    ELSE
	SET v_average_score = 0
    END IF;

    -- Update/insert the average score for the user
    INSERT INTO user_average_scores (user_id, average_score)
    VALUES (p_user_id, v_average_score)
    ON DUPLICATE KEY UPDATE average_score = v_average_score;
END;

//

DELIMITER ;
