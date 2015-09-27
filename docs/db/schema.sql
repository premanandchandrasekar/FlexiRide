CREATE OR REPLACE FUNCTION utc_now()
RETURNS TIMESTAMP without time zone 
AS $$
    BEGIN
            RETURN now() at time zone 'UTC';
    END;
$$ LANGUAGE plpgsql VOLATILE
    COST 1;

-- Details Of the Device Installed
CREATE TABLE Device(
    id                 SERIAL PRIMARY KEY,
    device_location    VARCHAR(200) NOT NULL
);


-- Details of cabs Booked
CREATE TABLE CabsBooked(
    id                     SERIAL PRIMARY KEY,
    driver_name            VARCHAR(15) NOT NULL,
    cab_number             VARCHAR(15) UNIQUE NOT NULL,
    driver_mobile_number   VARCHAR(15) UNIQUE NOT NULL,
    sharing                BOOLEAN DEFAULT false,
    device_id              INTEGER REFERENCES Device,
    estimated_amount       REAL NOT NULL,
    estimated_time         TIMESTAMP,
    created_on             TIMESTAMP DEFAULT utc_now()
);


-- Details of the user
CREATE TABLE UserDetails(
    id                     SERIAL PRIMARY KEY,
    booking_id             INTEGER REFERENCES CabsBooked,
    user_mobile_number     VARCHAR(15) NULL,
    pickup_location        VARCHAR(15) NOT NULL,
    destination            VARCHAR(15) NOT NULL,
    estimated_amount       REAL NOT NULL,
    created_on             TIMESTAMP DEFAULT utc_now()
);

ALTER TABLE cabsbooked drop COLUMN estimated_time;
ALTER TABLE cabsbooked add COLUMN estimated_time INTEGER;
ALTER TABLE cabsbooked add COLUMN crn INTEGER;

