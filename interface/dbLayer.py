def getGenomeSql():
  genomeSql = "SELECT '-- all --' AS genome UNION SELECT DISTINCT genome FROM experiments ORDER BY genome ASC"
  return genomeSql


def getDataSql():
  dataSql = """SELECT experiment_id, name, description, genome, epigenetic_mark, technique, project, data_type, biosource_name
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)"""
  return dataSql


def buildSqlWhere(ui):
  where = []
  
  # genome selection
  if ui.comboBoxGenome.currentIndex() > 0:
    where.append(('genome',str(ui.comboBoxGenome.currentText()),True))

  # build sql where clause from filter inputs
  filterInputs = [
    ("name", ui.lineEditName),
    ("description", ui.lineEditDescription),
    ("epigenetic_mark", ui.lineEditEpigenetic),
    ("technique", ui.lineEditTechnique),
    ("biosource_name", ui.lineEditBiosource),
    ("data_type", ui.lineEditDataType),
    ("project", ui.lineEditProject)]
  for (field,fIn) in filterInputs:
    content = fIn.text()
    if not content.isEmpty():
      where.append((field,str(content).strip(),False))

  whereStr = ""
  if len(where) > 0:
    whereStr = " WHERE " + " AND ".join(map(lambda (field,text,exact): "`"+field+"`" + (" = '"+text+"'" if exact else " LIKE '%"+text+"%'"),where))

  return whereStr


def getAdditionalDataSql(experiment_id):
  addDataSql = """SELECT * FROM (SELECT key AS Property, value AS Value FROM extra_metadata WHERE experiment_id = '"""+experiment_id+"""' ORDER BY Property ASC)
  UNION SELECT '' AS Property, '' AS Value
  UNION SELECT * FROM (SELECT key AS Property, value AS Value FROM sample_info s JOIN experiments e ON (e.sample_id = s.sample_id AND e.experiment_id = '"""+experiment_id+"""') ORDER BY Property ASC)
  """
  print addDataSql
  return addDataSql