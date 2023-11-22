from common.constants import BASE_FOLDER, FOLDER_SEPARATOR, FILE_SEPARATOR

def split_file(prefix:str, sufix:str, file_name:str):
  splitted = file_name.split(prefix)
  splitted = splitted[1].split(sufix)
  return splitted[0]

def get_uniques(prefix:str, sufix:str, file_names:list):
  trimmed = []
  for file_name in file_names:
    trimmed.append(split_file(prefix, sufix,file_name))
  return list(dict.fromkeys(trimmed))

def build_prefix(**kwargs):
  ret = BASE_FOLDER + FOLDER_SEPARATOR

  if (not 'file_format' in kwargs): return ret
  ret += kwargs['file_format'] + FOLDER_SEPARATOR

  if (not 'company' in kwargs): return ret
  ret += kwargs['company'] + FILE_SEPARATOR

  if (not 'year' in kwargs): return ret
  ret += kwargs['year'] + FILE_SEPARATOR

  if (not 'month' in kwargs): return ret
  ret += kwargs['month'] + FILE_SEPARATOR

  if (not 'state' in kwargs): return ret
  ret += kwargs['state']

  return ret
