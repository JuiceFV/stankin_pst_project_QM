CREATE TABLE tokens (
    id SERIAL,
    ip VARCHAR(255),
    token VARCHAR(3)
);

INSERT INTO tokens (ip, token) VALUES ('127.0.0.1', '001');