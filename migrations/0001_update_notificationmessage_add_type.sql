ALTER TABLE "NotificationMessage" ADD COLUMN "type" TEXT NOT NULL default "";
UPDATE NotificationMessage SET type = id;
