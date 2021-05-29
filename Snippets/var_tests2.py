#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


dict_of_dicts = {}

d = {'one': 'hey', 'two': 'bye'}

for i in range(3):
    dict_of_dicts[i] = dict(d)
    # dict_of_dicts[i].update_template({'three':i})
    dict.__setitem__(dict_of_dicts[i], "three", i)

print(dict_of_dicts)
# {0: {'one': 'hey', 'two': 'bye', 'three': 2}, 1: {'one': 'hey', 'two': 'bye', 'three': 2}, 2: {'one': 'hey', 'two': 'bye', 'three': 2}}
