UPDATE "Relay" SET calibration = '{"inverse":"on"}' WHERE hardware = 'gpio';

UPDATE "Relay" SET hardware = 'gpio' WHERE hardware = 'gpio-inverse';
