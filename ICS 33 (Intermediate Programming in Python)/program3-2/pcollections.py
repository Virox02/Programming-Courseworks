# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for ln_number, text_of_ln in enumerate(s.split('\n'),1):     
            print(f' {ln_number: >3} {text_of_ln.rstrip()}')
    
    if (type(type_name) != str) or (re.match('[A-Za-z]\w*$', type_name) == None) or (type_name in keyword.kwlist):
        raise SyntaxError(f'{type_name} is not a legal type name')
    if (type(field_names) != str) and (type(field_names) != list):
        raise SyntaxError('Field names must be in a list or string')
    if type(field_names) == str:
        field_names = field_names.replace(' ', '').split(',') if ',' in field_names else field_names.split()
    for name in field_names:
        if (re.match('[A-Za-z]\w*$', name) == None) or (name in keyword.kwlist):
            raise SyntaxError(f'{name} is not a legal field name')
    if defaults != {}:
        for key in defaults:
            if key not in field_names:
                raise SyntaxError(f'{key} is not a field name')
            
    class_template = f'''\
class {type_name}:
    _fields = {field_names}
    _mutable = {mutable}\n
'''
    
    init_template = '''\
    def __init__(self,'''
    
    init_template2 = ''
    
    repr_template = f'''\
    def __repr__(self):
        return f'{type_name}('''
    
    get_template = '\n\n'
    
    getitem_template = '''\
    def __getitem__(self, index):
        if (type(index) == str) and (index in self._fields):
            return self.__dict__[index]
        elif (type(index) == int) and (index < len(self._fields)):
'''''
    
    eq_template = '''\
    def __eq__(self, other):
        if (type(self) == type(other))'''
    
    asdict_template = '''\
    def _asdict(self):
        return_dict = {}
        for name in self._fields:
            return_dict[name] = self.__getitem__(name)
        return return_dict\n\n'''
    
    make_template = f'''\
    def _make(iterable):
        return {type_name}('''
    
    replace_template = f'''\
    def _replace(self, **kargs):
        for name in kargs:
            if name not in self._fields:
                raise TypeError('Field name does not exist')
        if self._mutable:
            for field, value in kargs.items():
                self.__dict__[field] = value
            return None
        else:
            new_fields = []
            for name in self._fields:
                if name in kargs:
                    new_fields.append(kargs[name])
                else:
                    new_fields.append(self.__dict__[name])
            return {type_name}._make(new_fields)\n
'''
    
    setattr_template = '''\
    def __setattr__(self, name, value):
        if (name in self._fields) and (name not in self.__dict__):
            self.__dict__[name] = value
        elif self._mutable:
            self.__dict__[name] = value
        else:
            raise AttributeError('Class is not mutable')
'''
    
    i = 0
    
    for name in field_names:
        if name in defaults:
            init_template += f' {name}={defaults[name]},' if i + 1 < len(field_names) else f' {name}={defaults[name]}):\n'
        else:
            init_template += f' {name},' if i + 1 < len(field_names) else f' {name}):\n'
        init_template2 += f'        self.{name} = {name}\n' if i + 1 < len(field_names) else f'        self.{name} = {name}\n\n'
        repr_template += f'{name}=[self.{name}],' if i + 1 < len(field_names) else f'{name}=[self.{name}])\''
        get_template += f'''\
    def get_{name}(self):
        return self.{name}\n\n'''
        if i == 0:
            getitem_template += f'''\
            if index == {i}:
                return self.get_{name}()\n'''
        else:
            getitem_template += f"""\
            elif index == {i}:
                return self.get_{name}()\n""" if i + 1 < len(field_names) else f"""\
            elif index == {i}:
                return self.get_{name}()
        else:
            raise IndexError('Invalid index')\n\n"""
        eq_template += f" and (self.__getitem__('{name}') == other.__getitem__('{name}'))" if i + 1 < len(field_names) else f""" and (self.__getitem__('{name}') == other.__getitem__('{name}')):
            return True
        else:
            return False\n\n"""
        make_template += f'{name}=iterable[{i}],' if i + 1 < len(field_names) else f'{name}=iterable[{i}])\n\n'
        i += 1

    class_definition = class_template + init_template + init_template2 + repr_template.replace('[', '{').replace(']', '}') + get_template + getitem_template + eq_template + asdict_template + make_template + replace_template + setattr_template
    

    # put your code here
    # bind class_definition (used below) to the string constructed for the class



    # Debugging aid: uncomment show_listing here so always display source code
    # show_listing(class_definition)
    
    # Execute class_definition's str inside name_space; followed by binding the
    #   attribute source_code to the class_definition; after the try/except then
    #   return the created class object; if any syntax errors occur, show the
    #   listing of the class and also show the error in the except clause
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )              
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                  
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')
    Point=pnamedtuple('Point','x,y', defaults = {'y':0})
    #driver tests
    import driver
    driver.default_file_name = 'bscp3S21.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
