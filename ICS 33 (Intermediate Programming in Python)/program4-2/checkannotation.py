# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect
import copy

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Begin by binding the class attribute to True allowing checking to occur
    #   (only if the object's attribute self._checking_on is also bound to True)
    checking_on  = True
  
    # To check the decorated function f, begin by binding self._checking_on to True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Begin by comparing check's function annotation with its arguments
        def check_sequence(type_name, type_str):
            assert isinstance(value, type_name), repr(param) + ' failed annotation check(wrong type): value = ' + repr(value) + '\n  was type ' + type_as_str(value) + ' ...should be type ' + type_str + '\n' + check_history
            
            if len(annot) == 1:
                i = 0
                for v in value:
                    self.check(param, annot[0], v, check_history + type_str + '[' + str(i) + '] check: ' + str(annot[0]) + '\n')
                    i += 1
            else:
                assert len(annot) == len(value), repr(param) + ' failed annotation check(wrong number of elements): value = ' + repr(value) + '\n  annotation had ' + str(len(annot)) + ' elements' + str(annot) + '\n' + check_history                 
                i = 0
                for a, v in zip(annot, value):
                    self.check(param, a, v, check_history + type_str + '[' + str(i) + '] check: ' + str(annot[i]) + '\n')
                    i += 1
        
        def check_dict():
            assert isinstance(value, dict), repr(param) + ' failed annotation check(wrong type): value = ' + repr(value) + '\n  was type ' + type_as_str(value) + ' ...should be type dict\n' + check_history                 
            if len(annot) != 1:
                assert False, repr(param) + ' annotation inconsistency: dict should have 1 item but had ' + str(len(annot)) + '\n  annotation = ' + str(annot) + '\n' + check_history                 
            else:
                annot_key, annot_value = list(annot.items())[0]
                for k, v in value.items():
                    self.check(param, annot_key, k, check_history + 'dict key check: ' + str(annot_key) + '\n')
                    self.check(param, annot_value, v, check_history + 'dict value check: ' + str(annot_value) + '\n')
        
        def check_set(type_name,type_str):
            assert isinstance(value, type_name), repr(param) + ' failed annotation check(wrong type): value = ' + repr(value) + '\n  was type ' + type_as_str(value) + ' ...should be type ' + type_str + '\n' + check_history                 
            if len(annot) != 1:
                assert False, repr(param) + ' annotation inconsistency: ' + type_str + ' should have 1 value but had ' + str(len(annot)) + '\n  annotation = ' + str(annot) + '\n' + check_history                 
            else:
                annot_thing = list(annot)[0]
                for thing in value:
                    self.check(param, annot_thing, thing, check_history + type_str + ' value check: ' + str(annot_thing) + '\n')
        
        def check_predicate():
            assert len(inspect.signature(annot).parameters) == 1, repr(param) + ' annotation inconsistency: predicate should have 1 parameter but had ' + str(len(inspect.signature(annot).parameters)) + '\n  annotation = ' + str(annot) + '\n' + check_history                 
            try:
                test = annot(value)
            except Exception as message:
                assert False, repr(param) + ' annotation predicate(' + str(annot) + ') raised exception' + '\n  exception = ' + str(message.__class__)[8:-2] + ': ' + str(message) + '\n' + check_history                 
            else:
                assert test, repr(param) + ' failed annotation check: value = ' + repr(value) + '\n  predicate = ' + str(annot) + '\n' + check_history
        
        def check_str():
            try:
                args = copy.deepcopy(self._args)
                test = eval(annot, args)
            except Exception as message:
                assert False, repr(param) + ' annotation str(' + str(annot) + ') raised exception' + '\n  exception = ' + str(message.__class__)[8:-2] + ': ' + str(message) + '\n' + check_history                 
            else:
                assert test, repr(param) + ' failed annotation check(str predicate: ' + repr(annot) + ')\n  args for evaluation: ' + ', '.join([str(k) + '->' + str(v) for k, v in self._args.items()]) + '\n' + check_history
        
        if annot == None:
            pass
        elif type(annot) is type:
            assert isinstance(value, annot), repr(param) + ' failed annotation check(wrong type): value = ' + repr(value) + '\n  was type ' + type_as_str(value) + ' ...should be type ' + str(annot)[8:-2] + '\n' + check_history                 
        elif isinstance(annot, list):
            check_sequence(list, 'list')
        elif isinstance(annot, tuple):
            check_sequence(tuple, 'tuple')
        elif isinstance(annot, dict):
            check_dict()
        elif isinstance(annot, set):
            check_set(set, 'set')
        elif isinstance(annot, frozenset):
            check_set(frozenset, 'frozenset')
        elif inspect.isfunction(annot):
            check_predicate()
        elif isinstance(annot, str):
            check_str()
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError: 
                assert False, repr(param) + ' annotation undecipherable: ' + str(annot) + '\n' + check_history                 
            except Exception as message:
                if message.__class__ is AssertionError:
                    raise
                else:
                    assert False, repr(param) + ' annotation protocol(' + str(annot) + ') raised exception' + '\n  exception = ' + str(message.__class__)[8:-2] + ': ' + str(message) + '\n' + check_history
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return the argument/parameter bindings in an OrderedDict (it's derived
        #   from a dict): bind the function header's parameters in its order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not self._checking_on:
            return self._f(*args, **kargs)
        
        self._args = param_arg_bindings()
        annot = self._f.__annotations__
        
        try:
            # For each found annotation, check it using the parameter's value
            for argument in self._args:
                if argument in annot:
                    self.check(argument, annot[argument], self._args[argument])
            # Compute/remember the value of the decorated function
            dec_func = self._f(*args, **kargs)
            # If 'return' is in the annotation, check it
            if 'return' in annot:
                self._args['_return'] = dec_func
                self.check('return', annot['return'], dec_func)
            # Return the decorated answer
            return dec_func
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
        #    print(80*'-')
        #    for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
        #        print(l.rstrip())
        #    print(80*'-')
            raise

if __name__ == '__main__':     
    # an example of testing a simple annotation  
    def f(x:int): pass
    f = Check_Annotation(f)
    f(3)
    #f('a')
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S21.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
