
CREATE TABLE IF NOT EXISTS dictionnary(
   central_word TEXT,
   position_ TEXT,
   word_neighbor TEXT
);

CREATE TABLE IF NOT EXISTS word(
   word TEXT,
   PRIMARY KEY(word),
   FOREIGN KEY(word) REFERENCES dictionnary(central_word)
);

CREATE TABLE IF NOT EXISTS run(
   jobId TEXT,
   date_ TEXT,
   PRIMARY KEY(jobId)
);

 
INSERT INTO run VALUES ("0","1970-01-01");