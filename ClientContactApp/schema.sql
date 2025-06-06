-- Client Table
CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client_code TEXT NOT NULL UNIQUE,
    --created_at DATETIME DEFAULT CURRENT_TIMESTAMP  --login information 
);

-- Contact Table
CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
   -- created_at DATETIME DEFAULT CURRENT_TIMESTAMP  --login information 
);

-- Link Table for Many-to-Many Relationship
CREATE TABLE IF NOT EXISTS client_contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES contact(id) ON DELETE CASCADE,
    UNIQUE (client_id, contact_id)
);