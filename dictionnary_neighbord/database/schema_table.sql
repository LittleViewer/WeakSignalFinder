CREATE TABLE IF NOT EXISTS dictionnary(
   central_word TEXT,
   position_ TEXT,
   word_neighbor TEXT,
   run_added TEXT
);

CREATE TABLE IF NOT EXISTS word(
   word TEXT,
   run_added TEXT,
   PRIMARY KEY(word),
   FOREIGN KEY(word) REFERENCES dictionnary(central_word)
);

CREATE TABLE IF NOT EXISTS run(
   jobId TEXT,
   date_ TEXT,
   PRIMARY KEY(jobId)
);

CREATE TABLE IF NOT EXISTS know_folder(
   jobId TEXT,
   name_folder TEXT,
   PRIMARY KEY(name_folder)
);

INSERT INTO run VALUES ("0","1970-01-01");