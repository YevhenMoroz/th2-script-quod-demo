import os

dirname = "."
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)

dirs = []

for file in fullpaths:
    if os.path.isdir(file):
        if "__" in file: pass
        else: dirs.append(file)

tc_count = 0
for i in dirs:
    path, dirs, files = next(os.walk(f"{i}"))
    tc_count += len(files)

print(tc_count)
