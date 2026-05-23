CREATE TABLE IF NOT EXISTS jobIdDateTime(
   jobId VARCHAR(50),
   dateTime DATETIME,
   PRIMARY KEY(jobId)
);

CREATE TABLE IF NOT EXISTS saveData(
   jobId VARCHAR(50),
   dateTime DATETIME,
   type VARCHAR(50),
   data TEXT,
   FOREIGN KEY(jobId) REFERENCES jobIdDateTime(jobId)
);

CREATE TABLE IF NOT EXISTS idCountryFeed(
   idCountry VARCHAR(3),
   nameCountry VARCHAR(50),
   nameModel VARCHAR(50),
   PRIMARY KEY(idCountry),
   UNIQUE(nameCountry)
);

CREATE TABLE IF NOT EXISTS feedLinkRss(
   link VARCHAR(250),
   nameOrganization VARCHAR(50),
   idCountry VARCHAR(3),
   idCountry_1 VARCHAR(3) NOT NULL,
   PRIMARY KEY(link),
   FOREIGN KEY(idCountry_1) REFERENCES idCountryFeed(idCountry)
);