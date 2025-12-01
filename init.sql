CREATE USER 'web_user'@'localhost' IDENTIFIED BY 'Webuser-123';

CREATE DATABASE website;

GRANT ALL PRIVILEGES ON website.* TO 'web_user'@'localhost';

USE website;

CREATE TABLE url (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    short_code VARCHAR(255) NOT NULL,
    created_at VARCHAR(255),
    updated_at VARCHAR(255)
);
