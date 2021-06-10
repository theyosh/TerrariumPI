CREATE TABLE IF NOT EXISTS "Webcam" (
	"id"	TEXT NOT NULL,
	"hardware"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"width"	INTEGER NOT NULL,
	"height"	INTEGER NOT NULL,
	"rotation"	TEXT NOT NULL,
	"awb"	TEXT NOT NULL,
	"archive"	JSON NOT NULL,
	"motion"	JSON NOT NULL,
	"markers"	JSON NOT NULL,
	"enclosure"	TEXT,
	FOREIGN KEY("enclosure") REFERENCES "Enclosure"("id") ON DELETE SET NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Relay" (
	"id"	TEXT NOT NULL,
	"hardware"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"wattage"	REAL,
	"flow"	REAL,
	"manual_mode"	BOOLEAN,
	"replacement"	DATETIME,
	"calibration"	JSON NOT NULL,
	"webcam"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Setting" (
	"id"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "SensorHistory" (
	"sensor"	TEXT NOT NULL,
	"timestamp"	DATETIME NOT NULL,
	"value"	REAL NOT NULL,
	"limit_min"	REAL NOT NULL,
	"limit_max"	REAL NOT NULL,
	"alarm_min"	REAL NOT NULL,
	"alarm_max"	REAL NOT NULL,
	"exclude_avg"	BOOLEAN NOT NULL,
	PRIMARY KEY("sensor","timestamp"),
	FOREIGN KEY("sensor") REFERENCES "Sensor"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Sensor" (
	"id"	TEXT NOT NULL,
	"hardware"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"limit_min"	REAL,
	"limit_max"	REAL,
	"alarm_min"	REAL,
	"alarm_max"	REAL,
	"max_diff"	REAL,
	"exclude_avg"	BOOLEAN NOT NULL,
	"calibration"	JSON NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "RelayHistory" (
	"relay"	TEXT NOT NULL,
	"timestamp"	DATETIME NOT NULL,
	"value"	REAL NOT NULL,
	"wattage"	REAL NOT NULL,
	"flow"	REAL NOT NULL,
	PRIMARY KEY("relay","timestamp"),
	FOREIGN KEY("relay") REFERENCES "Relay"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Audiofile_Playlist" (
	"audiofile"	TEXT NOT NULL,
	"playlist"	TEXT NOT NULL,
	PRIMARY KEY("audiofile","playlist"),
	FOREIGN KEY("playlist") REFERENCES "Playlist"("id") ON DELETE CASCADE,
	FOREIGN KEY("audiofile") REFERENCES "Audiofile"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Playlist" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"volume"	REAL,
	"shuffle"	BOOLEAN,
	"repeat"	BOOLEAN,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "NotificationMessage_NotificationService" (
	"notificationmessage"	TEXT NOT NULL,
	"notificationservice"	TEXT NOT NULL,
	FOREIGN KEY("notificationservice") REFERENCES "NotificationService"("id") ON DELETE CASCADE,
	PRIMARY KEY("notificationmessage","notificationservice"),
	FOREIGN KEY("notificationmessage") REFERENCES "NotificationMessage"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "NotificationService" (
	"id"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"rate_limit"	INTEGER,
	"enabled"	BOOLEAN NOT NULL,
	"setup"	JSON NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "NotificationMessage" (
	"id"	TEXT NOT NULL,
	"title"	TEXT NOT NULL,
	"message"	TEXT NOT NULL,
	"rate_limit"	INTEGER,
	"enabled"	BOOLEAN NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "ButtonHistory" (
	"button"	TEXT NOT NULL,
	"timestamp"	DATETIME NOT NULL,
	"value"	REAL NOT NULL,
	PRIMARY KEY("button","timestamp"),
	FOREIGN KEY("button") REFERENCES "Button"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Button" (
	"id"	TEXT NOT NULL,
	"hardware"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"calibration"	JSON NOT NULL,
	"enclosure"	TEXT,
	FOREIGN KEY("enclosure") REFERENCES "Enclosure"("id") ON DELETE SET NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Area" (
	"id"	TEXT NOT NULL,
	"enclosure"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"mode"	TEXT NOT NULL,
	"setup"	JSON NOT NULL,
	"state"	JSON NOT NULL,
	FOREIGN KEY("enclosure") REFERENCES "Enclosure"("id") ON DELETE CASCADE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Enclosure" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"image"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Audiofile" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"filename"	TEXT NOT NULL UNIQUE,
	"duration"	REAL NOT NULL,
	"filesize"	REAL NOT NULL,
	PRIMARY KEY("id")
);
CREATE INDEX IF NOT EXISTS "idx_webcam__enclosure" ON "Webcam" (
	"enclosure"
);
CREATE INDEX IF NOT EXISTS "idx_relay__webcam" ON "Relay" (
	"webcam"
);
CREATE INDEX IF NOT EXISTS "idx_audiofile_playlist" ON "Audiofile_Playlist" (
	"playlist"
);
CREATE INDEX IF NOT EXISTS "idx_notificationmessage_notificationservice" ON "NotificationMessage_NotificationService" (
	"notificationservice"
);
CREATE INDEX IF NOT EXISTS "idx_button__enclosure" ON "Button" (
	"enclosure"
);
CREATE INDEX IF NOT EXISTS "idx_area__enclosure" ON "Area" (
	"enclosure"
);
