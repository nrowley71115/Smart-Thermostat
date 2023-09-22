CREATE TABLE data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    time TEXT,
    setpoint INTEGER,
    temperature TEXT,
    humidity FLOAT,
    heating TEXT,
    air_conditioning TEXT,
    fan TEXT,
    schedule TEXT
);