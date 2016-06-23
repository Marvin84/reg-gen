CREATE TABLE IF NOT EXISTS `experiments` (
  `experiment_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `genome` varchar(50) NOT NULL,
  `epigenetic_mark` varchar(50) NOT NULL,
  `sample_id` varchar(20) NOT NULL,
  `technique` varchar(100) NOT NULL,
  `project` varchar(50) NOT NULL,
  `data_type` varchar(20) NOT NULL,
  `format` text NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`experiment_id`)
);

CREATE TABLE IF NOT EXISTS `sample_info` (
  `sample_id` varchar(255) NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`sample_id`, `key`)
);

CREATE TABLE IF NOT EXISTS `extra_metadata` (
  `experiment_id` varchar(255) NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`experiment_id`, `key`)
);

CREATE INDEX `experiments_genome` ON `experiments` (`genome` ASC);
CREATE INDEX `experiments_project` ON `experiments` (`project` ASC);
CREATE INDEX `experiments_genome_project` ON `experiments` (`genome` ASC, `project` ASC);
CREATE INDEX `experiments_sample_id` ON `experiments` (`sample_id` ASC);
CREATE INDEX `sample_info_key` ON `sample_info` (`key` ASC);
CREATE INDEX `extra_metadata_key` ON `extra_metadata` (`key` ASC);

-------------------- full-text search tables with triggers to keep them synced with data tables
CREATE VIRTUAL TABLE experiments_fts USING fts4(experiment_id,description, content='experiments', notindexed=experiment_id);
CREATE TRIGGER experiments_bu BEFORE UPDATE ON experiments BEGIN
  DELETE FROM experiments_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER experiments_bd BEFORE DELETE ON experiments BEGIN
  DELETE FROM experiments_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER experiments_au AFTER UPDATE ON experiments BEGIN
  INSERT INTO experiments_fts(docid, experiment_id, description) VALUES(new.rowid, new.experiment_id, new.description);
END;
CREATE TRIGGER experiments_ai AFTER INSERT ON experiments BEGIN
  INSERT INTO experiments_fts(docid, experiment_id, description) VALUES(new.rowid, new.experiment_id, new.description);
END;


CREATE VIRTUAL TABLE sample_info_fts USING fts4(sample_id,key,value, content='sample_info', notindexed=sample_id);
CREATE TRIGGER sample_info_bu BEFORE UPDATE ON sample_info BEGIN
  DELETE FROM sample_info_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER sample_info_bd BEFORE DELETE ON sample_info BEGIN
  DELETE FROM sample_info_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER sample_info_au AFTER UPDATE ON sample_info BEGIN
  INSERT INTO sample_info_fts(docid, sample_id, key, value) VALUES(new.rowid, new.sample_id, new.key, new.value);
END;
CREATE TRIGGER sample_info_ai AFTER INSERT ON sample_info BEGIN
  INSERT INTO sample_info_fts(docid, sample_id, key, value) VALUES(new.rowid, new.sample_id, new.key, new.value);
END;


CREATE VIRTUAL TABLE extra_metadata_fts USING fts4(experiment_id,key,value, content='extra_metadata', notindexed=experiment_id);
CREATE TRIGGER extra_metadata_bu BEFORE UPDATE ON extra_metadata BEGIN
  DELETE FROM extra_metadata_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER extra_metadata_bd BEFORE DELETE ON extra_metadata BEGIN
  DELETE FROM extra_metadata_fts WHERE docid=old.rowid;
END;
CREATE TRIGGER extra_metadata_au AFTER UPDATE ON extra_metadata BEGIN
  INSERT INTO extra_metadata_fts(docid, experiment_id, key, value) VALUES(new.rowid, new.experiment_id, new.key, new.value);
END;
CREATE TRIGGER extra_metadata_ai AFTER INSERT ON extra_metadata BEGIN
  INSERT INTO extra_metadata_fts(docid, experiment_id, key, value) VALUES(new.rowid, new.experiment_id, new.key, new.value);
END;