import os

class CookBook:
    def __init__(self):
        self.recipes = {}

    def __str__(self):
        recipes_str = ''
        for recipe in self.recipes:
            recipes_str += recipe + '\n'
        return recipes_str

    def add_recipes(self, new_recipes, replace=False):
        for recipe in new_recipes:
            if recipe not in self.recipes or replace:
                self.recipes[recipe] = new_recipes[recipe]

    def get_shop_list_by_dishes(self, dishes, person_count):
        shop_dict = {}
        for dish in dishes:
            if dish in self.recipes:
                for ingredient in self.recipes[dish]:
                    if ingredient['ingredient_name'] not in shop_dict:
                        shop_dict[ingredient['ingredient_name']] = {
                            'quantity': person_count * int(ingredient['quantity']),
                            'measure': ingredient['measure']}
                    else:
                        shop_dict[ingredient['ingredient_name']]['quantity'] += person_count * int(ingredient['quantity'])
            else:
                print(f'No recipe for {dish}')
        return shop_dict

    def load_recipes_from_file(self, filename, replace=False):
        recipes = {}
        if os.path.exists(filename) and filename.endswith('.txt'):
            with open(filename, 'r', encoding='utf-8') as file:
                for recipe in file:
                    if recipe not in recipes or replace:
                        recipes[recipe.strip()] = []
                        for ingredient in range(int(file.readline().strip())):
                            recipes[recipe.strip()].append(
                                dict(zip(['ingredient_name', 'quantity', 'measure'], file.readline().strip().split(' | ')))
                            )
                        file.readline()
            self.add_recipes(recipes, replace)
        else:
            print(f'No such file {filename}')

    def load_recipes_from_dir(self, path, replace=False, reverse=False):
        for file in get_sorted_txt_files_list(path, reverse=reverse):
            self.load_recipes_from_file(os.path.join(path, file), replace=replace)

def get_sorted_txt_files_list(path, reverse=False):
    files_prop_list = []
    files = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_prop_list.append([sum(1 for line in f), file_path])
        files_prop_list = sorted(files_prop_list, reverse=reverse)
        files = []
        for file_prop in files_prop_list:
            files.append(file_prop[1])
    else:
        print(f'No such path {path}')
    return files

def merge_txt_files(path, reverse=False):
    files = get_sorted_txt_files_list(path, reverse=reverse)
    if len(files) > 0:
        with open(os.path.join(os.getcwd(), 'merged_file.txt'), 'w+', encoding='utf-8') as target:
            for file in files:
                with open(file, 'r', encoding='utf-8') as initial:
                    target.writelines(initial.readlines())
                    target.write('Full path: ' + file + '\n')


merge_txt_files(os.path.join(os.getcwd(), 'files'), reverse=False)

cook_book = CookBook()
cook_book.load_recipes_from_dir(os.path.join(os.getcwd(), 'files'), replace=False, reverse=True)
#cook_book.load_recipes_from_file(os.path.join(os.getcwd(), 'extra_recipes.txt'), replace=True)
#cook_book.load_recipes_from_file(os.path.join(os.getcwd(), 'merged_file.txt'), replace=True)

recipes_to_add = {'Вареное яйцо': [{'ingredient_name': 'Яйцо', 'quantity': 1, 'measure': 'шт.'}],
                  'Яичница': [{'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт'}]}
cook_book.add_recipes(recipes_to_add)
print(cook_book)
print(cook_book.get_shop_list_by_dishes(['Запеченный картофель', 'Вареное яйцо', 'Яичница', 'Соленая рыба'], 2))
