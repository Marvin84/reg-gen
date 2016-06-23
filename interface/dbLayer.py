def getGenomesSql():
  genomesSql = "SELECT '-- all --' AS genome UNION SELECT DISTINCT genome FROM experiments ORDER BY genome ASC"
  return genomesSql

def getProjectsSql():
  projectsSql = "SELECT '-- all --' AS project UNION SELECT DISTINCT project FROM experiments ORDER BY project ASC"
  return projectsSql

sortByString = "0"
sortSelByString = "0"
order = 0
orderSel = 0

experiment_fields = ["experiment_id","name","description","genome","epigenetic_mark","technique","project","data_type","biosource_name"]
def getDataSql():
  dataSql = """SELECT """+",".join(experiment_fields)+"""
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)"""

  return dataSql


def buildSqlWhere(ui):
  where = []

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
  columnWhere = ""
  if len(where) > 0:
    columnWhere = " AND ".join(map(lambda (field,text,exact): "`"+field+"`" + (" = '"+text+"'" if exact else " LIKE '%"+text+"%'"),where))

  # general search over all fields
  generalSearchWhere = ""
  generalSearchContent = ui.lineEditGeneralSearch.text()
  if generalSearchContent.length() >= 3:
    content = str(generalSearchContent).strip()
    metadataSearchWhere = """experiment_id IN (
      SELECT experiment_id FROM extra_metadata_fts WHERE value MATCH '"+content+"' 
      UNION SELECT e.experiment_id FROM sample_info_fts s JOIN experiments e ON (e.sample_id = s.sample_id) WHERE s.value MATCH '"+content+"'
    )"""
    generalSearchWhere = "(" + " OR ".join(map(lambda fieldName: fieldName+" LIKE '%"+content+"%'", experiment_fields)) + " OR "+metadataSearchWhere+")"

  res = ""
  if len(columnWhere+generalSearchWhere) > 0:
    res = " WHERE ("+ " AND ".join(filter(lambda s: len(s)>0, [columnWhere, generalSearchWhere]))+")"

  return res


def getAdditionalDataSql(experiment_id):
  addDataSql = """SELECT 10,'---------------' AS Property, 'Add. Meta Data' AS Value
  UNION SELECT 11,'' AS Property, '' AS Value
  UNION SELECT 20,Property,Value FROM (SELECT key AS Property, value AS Value FROM extra_metadata WHERE experiment_id = '"""+experiment_id+"""' ORDER BY Property ASC)
  UNION SELECT 21,'' AS Property, '' AS Value
  UNION SELECT 22,'---------------' AS Property, 'Sample Information' AS Value
  UNION SELECT 23,'' AS Property, '' AS Value
  UNION SELECT 30,Property,Value FROM (SELECT key AS Property, value AS Value FROM sample_info s JOIN experiments e ON (e.sample_id = s.sample_id AND e.experiment_id = '"""+experiment_id+"""') ORDER BY Property ASC)
  """
  
  return addDataSql


def getSelectedExpSql(selectedExperimentIds):
  selectedExpSql = """SELECT """+",".join(experiment_fields)+"""
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)
        WHERE e.experiment_id IN ('"""+"','".join(selectedExperimentIds)+"""')
  """

  return selectedExpSql

def sortSql(ui):
  sortBy = ui.dataTable.horizontalHeader().sortIndicatorSection()+1
  sortByString = str(sortBy)
  order = ui.dataTable.horizontalHeader().sortIndicatorOrder()

  # order: 0 means Ascending, 1 means Descending
  if(order == 0):
    sortDataSql = " ORDER BY "+sortByString+" ASC"
  else:
    sortDataSql = " ORDER BY "+sortByString+" DESC"

  return sortDataSql

def sortSelectedSql(ui):
  sortSelBy = ui.dataTableSelected.horizontalHeader().sortIndicatorSection()+1
  sortSelByString = str(sortSelBy)
  orderSel = ui.dataTableSelected.horizontalHeader().sortIndicatorOrder()

  # order: 0 means Ascending, 1 means Descending
  if(orderSel == 0):
    sortSelDataSql = " ORDER BY "+sortSelByString+" ASC"
  else:
    sortSelDataSql = " ORDER BY "+sortSelByString+" DESC"

  return sortSelDataSql

def getSelectedExpForExportSql(selectedExperimentIds):
  selectedExpSql = """SELECT e.experiment_id, e.data_type, e.epigenetic_mark, e.project, bs.biosource_name, f.file AS blueprint_url, u.url AS roadmap_url, u2.original_file_url AS encode_url
        FROM experiments e 
        JOIN (SELECT sample_id,value AS biosource_name FROM sample_info WHERE key='biosource_name') bs ON (bs.sample_id = e.sample_id)
        LEFT JOIN (SELECT experiment_id,value AS file FROM extra_metadata WHERE key='FILE') f ON (f.experiment_id = e.experiment_id)
        LEFT JOIN (SELECT experiment_id,value AS url FROM extra_metadata WHERE key='url') u ON (u.experiment_id = e.experiment_id)
        LEFT JOIN (SELECT experiment_id,value AS original_file_url FROM extra_metadata WHERE key='original_file_url') u2 ON (u2.experiment_id = e.experiment_id)
        WHERE e.experiment_id IN ('"""+"','".join(selectedExperimentIds)+"""')
  """
  
  return selectedExpSql