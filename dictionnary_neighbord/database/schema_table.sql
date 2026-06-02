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

CREATE TABLE IF NOT EXISTS last_seen(
   date TEXT,
   jobId TEXT,
   type_seen TEXT,
   data TEXT,
   FOREIGN KEY (jobId) REFERENCES run(jobId)
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

CREATE TABLE IF NOT EXISTS intensity_word(
   jobId TEXT,
   word TEXT,
   absolute_value INTEGER,
   relative_value REAL,
   FOREIGN KEY (jobId) REFERENCES run(jobId),
   FOREIGN KEY (word) REFERENCES word(word)
);

INSERT OR IGNORE INTO run VALUES ('0','1970-01-01');