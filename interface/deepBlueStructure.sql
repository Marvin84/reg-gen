CREATE TABLE IF NOT EXISTS `experiments` (
  `_id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `genome` varchar(255) NOT NULL,
  `epigenetic_mark` text NOT NULL,
  `sample_id` varchar(255) NOT NULL,
  `technique` varchar(255) NOT NULL,
  `project` text NOT NULL,
  `data_type` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `format` text NOT NULL,
  PRIMARY KEY (`_id`)
);

CREATE TABLE IF NOT EXISTS `sample_info` (
  `sample_id` varchar(255) NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`sample_id`)
);

CREATE TABLE IF NOT EXISTS `extra_metadata` (
  `experiment_id` varchar(255) NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`experiment_id`)
);



/*'_id',
'name'
'description',
'genome',
'epigenetic_mark',
'sample_id',
'technique',
'project',
'data_type',
'type',
'format',

'extra_metadata',
'sample_info',
'upload_info',
'columns',*/