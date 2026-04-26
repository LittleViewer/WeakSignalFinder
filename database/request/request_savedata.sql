DROP TABLE jobIdDateTime;
CREATE TABLE jobIdDateTime(
   jobId VARCHAR(50),
   dateTime DATETIME,
   PRIMARY KEY(jobId)
);

DROP TABLE saveData;
CREATE TABLE saveData(
   jobId VARCHAR(50),
   dateTime DATETIME,
   type VARCHAR(50),
   data TEXT,
   FOREIGN KEY(jobId) REFERENCES jobIdDateTime(jobId)
);
