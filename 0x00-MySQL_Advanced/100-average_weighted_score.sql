-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //

CREATE OR REPLACE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_total_score DECIMAL(10, 2);
    DECLARE v_total_weight DECIMAL(10, 2);
    DECLARE v_average_score DECIMAL(10, 2);

    -- Calculate the total weighted score and the total weight
    SELECT SUM(score * weight), SUM(weight)
    INTO v_total_score, v_total_weight
    FROM scores
    WHERE user_id = p_user_id;

    -- Calculate the average weighted score
    IF v_total_weight > 0 THEN
	SET v_average_score = v_total_score / v_total_weight;
    ELSE
	SET v_average_score = 0;
    END IF;

    -- Store the average weighted score in the database
    UPDATE users
    SET average_weighted_score = v_average_score
    WHERE id = p_user_id;
END//

DELIMITER ;
