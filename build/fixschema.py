import os.path as path

file = path.join(path.abspath(path.join(path.abspath(__file__),'..')),'fixschema.sql')
queries = ''
queryTmpl = 'ALTER TABLE import.{0} SET SCHEMA public;\n'
tables = open(file).read().split('\n')

for t in tables:
	if 'import' in t:
		tableName = t.split('|')[1].strip()
		query = queryTmpl.format(tableName)
		queries += query

with open(file, 'w') as ofile:
	ofile.write(queries)
