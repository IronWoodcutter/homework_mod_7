import os
import re
import shutil

images = ['jpeg', 'png', 'jpg', 'svg']
video = ['mp4', 'mov', 'avi', 'mkv']
documents = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
audio = ['mp3', 'ogg', 'wav', 'amr']
archives = ['zip', 'gz', 'tar']
known_extensions = set()
unknown_extensions = set()
list_sorted_files = []
main_folder = input('Введіть шлях до папки яку будемо сортувати: ')
untouchable_folders = ['archives', 'video', 'audio', 'documents', 'images']

# створюємо словник для транслітерації строкових даних


def create_dict() -> dict:

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS


# функція нормалізацшї імен файлів та папок

def normalize(name):

    name = name.translate(create_dict())
    name = re.sub(r'[^_0-9A-Za-z]', '_', name)

    return name

# функція створення необхідних папок


def create_folder(untouchable_folders):
    for folder in untouchable_folders:
        if not os.path.exists(os.path.join(main_folder, folder)):
            os.mkdir(os.path.join(main_folder, folder))

# функція виявлення дублів файлів:


def duplication_check(new_path, norm_file_name, extension):

    n = '_'
    while True:
        path = os.path.join(new_path, f'{norm_file_name}.{extension}')
        if os.path.exists(path):
            norm_file_name = f"{norm_file_name}{n}"
        else:
            break

    return norm_file_name

# функція переміщення знайдених файлів


def move(path, new_path, file_name, extension):
    norm_file_name = normalize(file_name)
    if os.path.exists(os.path.join(new_path, f'{norm_file_name}.{extension}')):
        norm_file_name = duplication_check(new_path, norm_file_name, extension)

    shutil.move(path, os.path.join(new_path, f'{norm_file_name}.{extension}'))
    list_sorted_files.append(f'{norm_file_name}.{extension}')
    known_extensions.add(extension)

# функція нармалізації найменувань папок


def norm_name_folder(main_folder):
    for item in os.listdir(main_folder):
        path = os.path.join(main_folder, item)
        if os.path.isdir(path):
            new_path = os.path.join(main_folder, normalize(item))
            os.rename(path, new_path)
            norm_name_folder(new_path)


# функція створення списку файлів


def file_paths(main_folder, list_file_paths=[]):
    for item in os.listdir(main_folder):
        path = os.path.join(main_folder, item)
        if not os.path.isdir(path):
            list_file_paths.append(path)
        else:
            if item not in untouchable_folders:
                file_paths(path)
    return list_file_paths

# функція сортування файлів


def sort(main_folder):
    list_file_paths = file_paths(main_folder)
    for path in list_file_paths:
        full_name = os.path.basename(path)
        file_name = full_name.rsplit('.')[0]
        extension = path.split('.')[-1]

        if extension in images:
            new_path = os.path.join(main_folder, 'images')
            move(path, new_path, file_name, extension)

        elif extension in video:
            new_path = os.path.join(main_folder, 'video')
            move(path, new_path, file_name, extension)

        elif extension in documents:
            new_path = os.path.join(main_folder, 'documents')
            move(path, new_path, file_name, extension)

        elif extension in audio:
            new_path = os.path.join(main_folder, 'audio')
            move(path, new_path, file_name, extension)
        elif extension in archives:
            new_path = os.path.join(
                main_folder, 'archives', normalize(file_name))

            if not os.path.exists(new_path):
                os.mkdir(new_path)

            try:
                shutil.unpack_archive(path, new_path)
                known_extensions.add(extension)
                list_sorted_files.append(
                    f'{os.path.basename(new_path)}.{extension}')
                os.remove(path)

            except shutil.ReadError:
                print('The archive is damaged or not a registered archive', full_name)
                os.remove(new_path)
        else:
            unknown_extensions.add(extension)


# функція видалення пустих папок


def remove_empty_folders(main_folder):
    for item in os.listdir(main_folder):
        path = os.path.join(main_folder, item)
        if os.path.isdir(path):
            remove_empty_folders(path)
            if not os.listdir(path):
                os.rmdir(path)


def main():
    norm_name_folder(main_folder)
    create_folder(untouchable_folders)
    sort(main_folder)
    remove_empty_folders(main_folder)


if __name__ == '__main__':
    main()
    print('Відсортовані файли: ', list_sorted_files)
    print('Всі відомі розширення: ', known_extensions)
    print('Всі невідомі розширення: ', unknown_extensions)
