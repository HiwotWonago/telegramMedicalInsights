import os

def print_tree(start_path, prefix="", max_depth=1, current_depth=0):
    if current_depth > max_depth:
        return
    items = sorted(os.listdir(start_path))
    pointers = ['├── '] * (len(items) - 1) + ['└── ']
    for pointer, item in zip(pointers, items):
        path = os.path.join(start_path, item)
        print(prefix + pointer + item)
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            print_tree(path, prefix + extension, max_depth, current_depth + 1)

if __name__ == "__main__":
    root_folder = "." 
    print(root_folder)
    print_tree(root_folder)
