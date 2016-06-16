def getGenomesSql():
  genomesSql = "SELECT '-- all --' AS genome UNION SELECT DISTINCT genome FROM experiments ORDER BY genome ASC"
  return genomesSql

def getProjectsSql():
  projectsSql = "SELECT '-- all --' AS project UNION SELECT DISTINCT project FROM experiments ORDER BY project ASC"
  return projectsSql


experiment_fields = ["experiment_id","name","description","genome","epigenetic_mark","technique","project","data_type","biosource_name"]
def getDataSql():
  dataSql = """SELECT """+",".join(experiment_fields)+"""
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)"""
  return dataSql


def buildSqlWhere(ui):
  where = []

  # general search over all fields
  generalSearchWhere = ""
  generalSearchContent = ui.lineEditGeneralSearch.text()
  if generalSearchContent.length() >= 3:
    content = str(generalSearchContent).strip()
    generalSearchWhere = "(" + " OR ".join(map(lambda fieldName: fieldName+" LIKE '%"+content+"%'", experiment_fields)) + ")"
  
  # genome selection
  if ui.comboBoxGenome.currentIndex() > 0:
    where.append(('genome',str(ui.comboBoxGenome.currentText()),True))

  # project selection
  if ui.comboBoxProject.currentIndex() > 0:
    where.append(('project',str(ui.comboBoxProject.currentText()),True))

  # build sql where clause from filter inputs
  filterInputs = [
    ("name", ui.lineEditName),
    ("description", ui.lineEditDescription),
    ("epigenetic_mark", ui.lineEditEpigenetic),
    ("technique", ui.lineEditTechnique),
    ("biosource_name", ui.lineEditBiosource),
    ("data_type", ui.lineEditDataType)]
  for (field,fIn) in filterInputs:
    content = fIn.text()
    if not content.isEmpty():
      where.append((field,str(content).strip(),False))

  # compile where query
  whereStr = ""
  if len(where) > 0:
    whereStr = " WHERE " + " AND ".join(map(lambda (field,text,exact): "`"+field+"`" + (" = '"+text+"'" if exact else " LIKE '%"+text+"%'"),where))

  return whereStr + (" AND "+generalSearchWhere if len(generalSearchWhere)>0 else "")


def getAdditionalDataSql(experiment_id):
  addDataSql = """SELECT * FROM (SELECT key AS Property, value AS Value FROM extra_metadata WHERE experiment_id = '"""+experiment_id+"""' ORDER BY Property ASC)
  UNION SELECT '' AS Property, '' AS Value
  UNION SELECT * FROM (SELECT key AS Property, value AS Value FROM sample_info s JOIN experiments e ON (e.sample_id = s.sample_id AND e.experiment_id = '"""+experiment_id+"""') ORDER BY Property ASC)
  """
  
  return addDataSql


def getSelectedExpSql(selectedExperimentIds):
  selectedExpSql = """SELECT """+",".join(experiment_fields)+"""
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)
        WHERE e.experiment_id IN ('"""+"','".join(selectedExperimentIds)+"""')
  """
  
  return selectedExpSql