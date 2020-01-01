import shutil
import os
import glob


def moveAllFilesinDir(src_dir, train_dst_dir, test_dst_dir):
    # Check if both the are directories
    if os.path.isdir(src_dir) and os.path.isdir(train_dst_dir) and os.path.isdir(test_dst_dir):
        no_files = len([name for name in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, name))])
        split_val = no_files*4/5
        count_val = 1
        # Iterate over all the files in source directory
        for filePath in glob.glob(src_dir + '\*'):
            # Move each file to destination Directory
            if count_val < split_val:
                shutil.move(filePath, train_dst_dir)
            else:
                shutil.move(filePath, test_dst_dir)
            count_val += 1
    else:
        print("srcDir & dstDir should be Directories")


dir_path = os.path.dirname(os.path.realpath(__file__))
file_names = [name for name in os.listdir(dir_path)
              if os.path.isdir(os.path.join(dir_path, name))
              and name not in ["Train", "Test"]]
# file_names = file_names[10:11]
print(file_names)
# print(file_names)
for file_name in file_names:
    print(file_name)
    source_dir = file_name
    train_dst_dir = 'Train/' + file_name
    test_dst_dir = 'Test/' + file_name
    moveAllFilesinDir(os.path.join(dir_path, source_dir),
                      os.path.join(dir_path, train_dst_dir),
                      os.path.join(dir_path, test_dst_dir))
    print("Move " + file_name + " Done")