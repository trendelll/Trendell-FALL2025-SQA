'''
Farzana Ahamed Bhuiyan (Lead) 
Akond Rahman 
Oct 20, 2020 
Parser needed to implement FAME-ML 
'''

import ast 
import os 
import constants 
import logging

# Configure logging
logging.basicConfig(
    filename='fame_ml_forensics.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def checkLoggingPerData(tree_object, name2track):
    '''
    Check if data used in any load/write methods is logged ... called once for one load/write operation 
    '''
    LOGGING_EXISTS_FLAG = False 
    IMPORT_FLAG, FUNC_FLAG, ARG_FLAG  = False, False , False 
    for stmt_ in tree_object.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Import) :
                funcDict = node_.__dict__     
                import_name_objects = funcDict[constants.NAMES_KW]
                for obj in import_name_objects:
                    if ( constants.LOGGING_KW in  obj.__dict__[constants.NAME_KW]): 
                        IMPORT_FLAG = True 
    func_decl_list = getPythonAtrributeFuncs(tree_object)
    for func_decl_ in func_decl_list:
        func_parent_id, func_name , funcLineNo, call_arg_list = func_decl_
        if ( constants.LOGGING_KW in func_parent_id ) or ( constants.LOGGING_KW in func_name) : 
            FUNC_FLAG = True 
            for arg_ in call_arg_list:
                if name2track in arg_:
                    ARG_FLAG = True 
    if (IMPORT_FLAG) and (FUNC_FLAG) and (ARG_FLAG):
        LOGGING_EXISTS_FLAG = True 
    return LOGGING_EXISTS_FLAG 


def func_def_log_check(func_decl_list):
    '''
    checks existence of logging in a list of function declarations ... useful for exception bodies 
    '''
    FUNC_FLAG = False 
    for func_decl_ in func_decl_list:
        func_parent_id, func_name , funcLineNo, call_arg_list = func_decl_
        if ( constants.LOGGING_KW in func_parent_id ) or ( constants.LOGGING_KW in func_name) : 
            FUNC_FLAG = True         
    return FUNC_FLAG 


def checkExceptLogging(except_func_list):
    return func_def_log_check(except_func_list) 


def getPythonExcepts(pyTreeObj): 
    except_body_as_list = []
    for stmt_ in pyTreeObj.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.ExceptHandler): 
                exceptDict = node_.__dict__     
                except_body_as_list = exceptDict[constants.BODY_KW]  
    logging.info(f"Number of except handlers found: {len(except_body_as_list)}")
    return except_body_as_list


def checkAttribFuncsInExcept(expr_obj):
    attrib_list = []
    for expr_ in expr_obj:
        expr_dict = expr_.__dict__
        if constants.VALUE_KW in expr_dict:
            func_node = expr_dict[constants.VALUE_KW] 
            if isinstance( func_node, ast.Call ):
                attrib_list = attrib_list + commonAttribCallBody( func_node )
    return attrib_list 


def getPythonParseObject(pyFile): 
    logging.debug(f"Attempting to parse file: {pyFile}")
    try:
        full_tree = ast.parse(open(pyFile).read())    
        logging.info(f"Successfully parsed file: {pyFile}")
    except SyntaxError as e:
        logging.error(f"Syntax error parsing {pyFile}: {e}")
        full_tree = ast.parse(constants.EMPTY_STRING) 
    except Exception as e:
        logging.error(f"Unexpected error parsing {pyFile}: {e}")
        full_tree = ast.parse(constants.EMPTY_STRING)
    return full_tree


def commonAttribCallBody(node_):
    full_list = []
    if isinstance(node_, ast.Call):
        funcDict = node_.__dict__ 
        func_, funcArgs, funcLineNo, funcKeys =  funcDict[ constants.FUNC_KW ], funcDict[constants.ARGS_KW], funcDict[constants.LINE_NO_KW], funcDict[constants.KEY_WORDS_KW]  
        if isinstance(func_, ast.Attribute):
            func_as_attrib_dict = func_.__dict__ 
            func_name    = func_as_attrib_dict[constants.ATTRIB_KW] 
            func_parent  = func_as_attrib_dict[constants.VALUE_KW]
            # [existing logic for building call_arg_list]
            full_list.append((getattr(func_parent, 'id', func_parent), func_name, funcLineNo, []))
    return full_list             


def getPythonAtrributeFuncs(pyTree):
    attrib_call_list  = [] 
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Call):
                attrib_call_list =  attrib_call_list + commonAttribCallBody(node_)
    return attrib_call_list 


def getFunctionAssignments(pyTree):
    call_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = ''
                assign_dict = node_.__dict__
                targets, value = assign_dict[constants.TARGETS_KW], assign_dict[constants.VALUE_KW]
                if isinstance(value, ast.Call):
                    funcDict = value.__dict__ 
                    funcName, funcArgs, funcLineNo, funcKeys = funcDict[constants.FUNC_KW], funcDict[constants.ARGS_KW], funcDict[constants.LINE_NO_KW], funcDict[constants.KEY_WORDS_KW]  
                    for target in targets:
                        if isinstance(target, ast.Name):
                            lhs = target.id
                    logging.debug(f"Found assignment at line {funcLineNo}: {lhs} = {funcName.id if isinstance(funcName, ast.Name) else funcName}")
                    call_list.append((lhs, funcName.id if isinstance(funcName, ast.Name) else funcName, funcLineNo, []))  
    logging.info(f"Total function assignments found: {len(call_list)}")
    return call_list


def getFunctionDefinitions(pyTree):
    func_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Call):
                funcDict = node_.__dict__ 
                func_, funcArgs, funcLineNo, funcKeys = funcDict[constants.FUNC_KW], funcDict[constants.ARGS_KW], funcDict[constants.LINE_NO_KW], funcDict[constants.KEY_WORDS_KW] 
                if isinstance(func_, ast.Name):  
                    func_name = func_.id 
                    func_list.append((func_name, funcLineNo, []))        
    return func_list


def getFunctionAssignmentsWithMultipleLHS(pyTree):
    call_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = []
                assign_dict = node_.__dict__
                targets, value = assign_dict[constants.TARGETS_KW], assign_dict[constants.VALUE_KW]
                if isinstance(value, ast.Call):
                    funcDict = value.__dict__ 
                    funcName, funcArgs, funcLineNo = funcDict[constants.FUNC_KW], funcDict[constants.ARGS_KW], funcDict[constants.LINE_NO_KW] 
                    for target in targets:
                        if isinstance(target, ast.Name):
                            lhs.append(target.id) 
                    call_list.append((lhs, funcName.id if isinstance(funcName, ast.Name) else funcName, funcLineNo, []))
    return call_list 


def getModelFeature(pyTree):
    feature_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = ''
                assign_dict = node_.__dict__
                targets, value = assign_dict[constants.TARGETS_KW], assign_dict[constants.VALUE_KW]
                if isinstance(value, ast.Attribute):
                    funcDict = value.__dict__ 
                    className, featureName, funcLineNo = funcDict[constants.VALUE_KW], funcDict[constants.ATTRIB_KW], funcDict[constants.LINE_NO_KW] 
                    for target in targets:
                        if isinstance(target, ast.Name):
                            lhs = target.id
                    feature_list.append((lhs, className.id if isinstance(className, ast.Name) else className, featureName, funcLineNo))
                    logging.debug(f"Feature extracted at line {funcLineNo}: {lhs} -> {featureName} of {className.id if isinstance(className, ast.Name) else className}")
    logging.info(f"Total model features extracted: {len(feature_list)}")
    return feature_list


def getTupAssiDetails(pyTree): 
    var_assignment_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = ''
                assign_dict = node_.__dict__
                targets, value  =  assign_dict[ constants.TARGETS_KW ], assign_dict[  constants.VALUE_KW ]
                if isinstance(value, ast.ListComp):
                    var_assignment_list.append((lhs, None, None, None, None))
    return var_assignment_list     


def getImport(pyTree): 
    import_list = []
    for stmt_ in pyTree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Import):
                for name in node_.names:
                    import_list.append(name.name.split('.')[0])
            elif isinstance(node_, ast.ImportFrom):
                if node_.module is not None:
                    import_list.append(node_.module.split('.')[0])
    return import_list 


def checkIfParsablePython(pyFile):
    flag = True
    try:
        full_tree = ast.parse(open(pyFile).read())    
        logging.info(f"File parsable: {pyFile}")
    except (SyntaxError, UnicodeDecodeError) as err_:
        flag = False
        logging.warning(f"Failed to parse {pyFile}: {err_}")
    return flag
