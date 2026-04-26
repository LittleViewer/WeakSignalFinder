-- SQLite
DROP TABLE idCountryFeed;
CREATE TABLE idCountryFeed(
   idCountry VARCHAR(3),
   nameCountry VARCHAR(50),
   nameModel VARCHAR(50),
   PRIMARY KEY(idCountry),
   UNIQUE(nameCountry)
);

CREATE TABLE feedLinkRss(
   link VARCHAR(250),
   nameOrganization VARCHAR(50),
   idCountry VARCHAR(3),
   idCountry_1 VARCHAR(3) NOT NULL,
   PRIMARY KEY(link),
   FOREIGN KEY(idCountry_1) REFERENCES idCountryFeed(idCountry)
);
