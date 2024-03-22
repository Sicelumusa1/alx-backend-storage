-- creates a trigger that decreases the quantity of an item after adding a new order

DELIMITER //

CREATE TRIGGER update_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_id INT;
    DECLARE order_quantity INT;

    -- Get the item ID and order quantity from inserted order
    SELECT item_id, number INTO item_id, order_quantity FROM items WHERE name = NEW.item_name;

    -- Update the item quantity
    UPDATE items
    SET quantity = quantity - order_quantity
    WHERE id = item_id;
END;
//
DELIMITER;
