import re, collections, base64, bz2

FILE_PY_ORIGINAL = 'pyordle.py'
FILE_PY_SINGLE   = 'pyordle_single_file.py'
SUFFIX_O         = collections.OrderedDict([('answers', ''), ('valid', '.union(answer_s)')])
out_l            = ['import base64, bz2']
for suffix in SUFFIX_O:
  with open('pyordle_{}.txt'.format(suffix), 'rb') as f:
    var = '{}_s'.format(suffix.rstrip('s'))
    out_l.append('''
{} = set([line.strip().upper() for line in bz2.decompress(base64.b64decode('{}')).decode('utf-8').strip().split('\\\\n')]){}
# print(len({}), list({})[0])'''.format(var, base64.b64encode(bz2.compress(f.read())),
                                        SUFFIX_O[suffix], var, var))
with open(FILE_PY_ORIGINAL, 'rb') as f:
  out = re.sub(r'with open\(.*?(?=\n\n## )', ''.join(out_l), f.read(), flags=re.DOTALL)
with open(FILE_PY_SINGLE, 'wb') as f:
  f.write(out)
