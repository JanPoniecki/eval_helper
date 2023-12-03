def add_main(folder, function, f_name):
    zmienne = {'int': 'd', 'void': '0', 'char': 'c', 'unsigned int' : 'd', 'char*': 's', 'char *' : 's'} 
    rpls = ['*', 'char', 'int', 'void']
    if function[:-1] == ';':
        function == function[:-1]
    function = function.replace('\n', '')
    fun_return = re.findall(r'(.+)(?=\()', function)
    typ_zmiennej = 'NOT FOUND'
    zmienna_main = 'NOT FOUND'
    if fun_return:
        fun_return = fun_return[0]
        if '*' in fun_return and 'char' in fun_return:
            typ_zmiennej = 's'
            zmienna_main = 'char*'
        elif 'char' in fun_return:
            typ_zmiennej = 'c'
            zmienna_main = 'char'
        elif 'int' in fun_return:
            typ_zmiennej = 'd'
            zmienna_main = 'int'
        elif 'void' in fun_return:
            typ_zmiennej = None
            zmienna_main = 'void'
    args = re.findall(r'(?<=\()(.+)(?=\))', function)
    if args:
        args = args[0].split(',')
        # print(args)
    main_txt = '#include <stdio.h.>\n'
    main_txt += f'{function};\n'
    main_txt += 'int main(int argc, char** argv)\n'
    main_txt += '{\n'
    main_txt += f'''
    if (argc != {len(args) + 1})
    {{
        printf("incorrect args (expected %d)", argc);
    }}
    '''
    main_txt += 'else'
    args_to_put = ''
    function_args = []
    licznik = 1
    for a in args:
        args_to_put += f'{a} = argv[{licznik}];\n'
        for rpl in rpls:
            a = a.replace(rpl, '')
        function_args.append(f'{a}')
        licznik += 1
    function_args = ','.join(function_args)
    main_txt += f'''
    {{
        {args_to_put}
        {zmienna_main} result = {f_name}({function_args});
        printf("%{typ_zmiennej}", result);
    }}
}}
    '''
    with open(f'./ev/{folder}/main.c', 'w') as main:
        main.write(main_txt)
    return main_txt
    

def look_for_main(folder, function_name):
    with open (f'./ev/{folder}/{function_name}.c') as ex:
        is_comment = False
        i = 0
        for x in ex:
            if '/*' in x:
                is_comment = True
            if '*/' in x:
                is_comment = False
            if 'main' in x and not is_comment and '//' not in x:
                return f'\033[91mmain function dedected (line: {i})\033[0m'
            i += 1
    return False

def check_function_name(folder, function_name):
    with open (f'./ev/{folder}/{function_name}.c') as ex:
        result = None
        for x in ex:
            if f'{function_name}(' in x:
                return x
        return result

def check_name(folder, function):
    files = os.listdir(f'./ev/{folder}')
    if f'{function}.c' in files:
        print(f'filename {function}.c ok')
        return True
    else:
        print(f'\033[91mfilename {function}.c ERROR\n\033[0m')
        return False

import os
import re
import sys

arguments = sys.argv
print(arguments)
if 'am' in arguments:
    add_main_file = True
else:
    add_main_file = False

subjects = {}
with open ('exercises.txt') as file:
    for f in file:
        exs = re.findall(r'Exercise \d.', f)
        if exs:
            ex = f"ex{exs[0].split(' ')[1]}"
            functions = re.findall(r'(?<=:\s)(\w+)', f)
            if functions:
                fun = functions[0]
            else:
                fun = 'none'
            subjects[ex] = fun
folders = os.listdir('./ev')

for f in folders:
    if f in subjects:
        folder = f
        function = subjects[f]
        name_ok = check_name(folder, function)
        if name_ok:
            fun_name_ok = check_function_name(folder, function)
            if fun_name_ok:
                print(f'{fun_name_ok[:-1]}')
                found_main = look_for_main(folder, function)
                if found_main:
                    print(found_main)
                else:
                    if add_main_file:
                        add_main(folder, fun_name_ok, function)
                print(' ')
            else:
                print('\033[91mfunction name ERROR\n\033[0m')