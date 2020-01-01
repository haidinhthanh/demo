import os
dir_path = os.path.dirname(os.path.realpath(__file__))
train_dir_path = os.path.join(dir_path, "Test/url")
remove_path = os.path.join(dir_path, "Test/content")
files = [name for name in os.listdir(train_dir_path) if os.path.isfile(os.path.join(train_dir_path, name))]
delete_files = []
# for file in files:
#     with open(train_dir_path+"/"+file, "r", encoding="UTF-8") as f:
#         line = f.read().strip()
#         if len(line) < 45 :
#             delete_files.append(train_dir_path+"/"+file)
#             print(train_dir_path+"/"+file)
# for file in delete_files:
#     os.remove(file)
# print(len([name for name in os.listdir(train_dir_path) if os.path.isfile(os.path.join(train_dir_path, name))]))
print("start fill")
fil_content = []
for file in files:
    with open(train_dir_path+"/"+file, "r", encoding="UTF-8") as f:
        print("run")
        fil_content.append(f.read().strip())
print("end fill")
files = [name for name in os.listdir(remove_path) if os.path.isfile(os.path.join(remove_path, name))]
for file in files:
    with open(remove_path+"/"+file, "r", encoding="UTF-8") as f:
        print("run")
        if f.read().strip() in fil_content:
            delete_files.append(remove_path+"/"+file)
print("start choose")
for file in delete_files:
    print("remove file " + file)
    os.remove(file)