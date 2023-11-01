ALTER TABLE "Relay" ADD COLUMN "notification" BOOLEAN NOT NULL default TRUE;

ALTER TABLE "Sensor" ADD COLUMN "notification" BOOLEAN NOT NULL default TRUE;

ALTER TABLE "Button" ADD COLUMN "notification" BOOLEAN NOT NULL default TRUE;

ALTER TABLE "Webcam" ADD COLUMN "notification" BOOLEAN NOT NULL default TRUE;
