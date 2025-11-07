-- Initialize the fridgie database

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO items (name, quantity) VALUES
    ('Milk', 2),
    ('Eggs', 12),
    ('Bread', 1),
    ('Cheese', 1),
    ('Apples', 5);
