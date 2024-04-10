CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    register_status BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    register_status BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    register_status BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

create table location_category_reviewed (
    id INTEGER primary key autoincrement,
    location_id INTEGER not null references locations,
    category_id INTEGER not null references categories,
    user_id INTEGER not null references users,
    reviewed_title Text not null,
    reviewed_desc Text not null,
    reviewed_star INTEGER default 5 not null,
    reviewed_at DATETIME default CURRENT_TIMESTAMP,
    register_status BOOLEAN default 1 not null
);
