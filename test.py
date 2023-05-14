f=open("input_file.txt")
cmd_list=f.readlines()

if len(cmd_list) > 256:
    print("Lines exceed 256")
    exit()
print(cmd_list)  