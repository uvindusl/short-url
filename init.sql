CREATE DATABASE IF NOT EXISTS website;

CREATE USER IF NOT EXISTS 'web_user'@'localhost' IDENTIFIED BY 'Webuser-123';

GRANT ALL PRIVILEGES ON website.* TO 'web_user'@'localhost';
FLUSH PRIVILEGES;

USE website;

CREATE TABLE IF NOT EXISTS url (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    short_code VARCHAR(255) NOT NULL,
    created_at VARCHAR(255),
    updated_at VARCHAR(255)
);
