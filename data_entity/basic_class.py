from typing import Any
from logs import logging_operation
from types import NoneType
import traceback
import data_entity
from capacities.basic.file import tp_file
# import data_entity.message, data_entity.user, data_entity.task

class Base():
    '''
        # Introduction
        The Base Class for all data related classes in ASKAI 
        
        # Attributes
        
        # Functions
    
    '''
    def __init__(self, attribute_dict:dict):
        logging_operation.write_log(f"In class {__class__} __init__()", source = __name__, level = 1)

        initial_attribute_list = __class__.__annotations__.items()
        for initial_attribute in initial_attribute_list:
            if not attribute_dict.get(initial_attribute[0],"No keys") == "No Keys":
                exec(f"self.{initial_attribute[0]} = attribute_dict['{initial_attribute[0]}']")
                attribute_dict.pop(initial_attribute[0])
        
        logging_operation.write_log(f"{__class__}Initial over!", source = __name__, level = 1)
    
    def to_dict(self) -> dict:
        '''
            # Introduction
            Parse the attribute and value to dict
            
            # Returns
            - attribute_dict: attribute name and value pairs 
        
        '''
        
        attribute_dict = self.__class__.get_attribute_annotition()
        for key in attribute_dict.keys():
            exec(f"attribute_dict['{key}']=self.{key}")
        return attribute_dict
    
    @classmethod
    def get_attribute_annotition(cls):
        '''
            # Introduction
            Get all the attributes annotition of the class(father class included)
            
            # Returns
            attribute annotation{name:type}
        '''
        attribute_annotation = dict()
        class_type = cls
        logging_operation.write_log("The calling class is \n" + str(class_type), source = __name__, level = 1)

        # Add the attribute in attribute_annotition and find the base/father class
        while not class_type in [Base,object,None]:
            attribute_annotation.update(class_type.__annotations__)
            # base/father class
            class_type = class_type.__base__
        return attribute_annotation
    
    @classmethod
    def get_class_function(cls):
        return [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("__")]
    
    @classmethod
    def check_attribute_name(cls, attribute_dict:dict):    
        '''
            # Introduction
            Check all the attributes to ensure if all are included(by attribute name)
            
            # Attribute
            - attribute_dict: the target attribute and value to check, each item should have key-value pairs(attribute_name,attribute_value)
            
            # Returns
            - True: Each Attribute is included in the attribute_dict. Ignore the redundant attributes in the input attribute_dict
            - False: Miss ore or more attribute, 
        '''
        
        attribute_annotation = cls.get_attribute_annotition()
        # logging_operation.write_log(f"In check_attribute, the target attributes are\n{attribute_annotation}\nThe attributes to check are {attribute_dict}", source = __name__, level = 1)
        # The attribute match result: will in the dict attribute_annotation_matching_result if not match
        attribute_annotation_matching_result = attribute_annotation.copy()
        for target_attribute in attribute_annotation.items():
            logging_operation.write_log(f"{not attribute_dict.get(target_attribute[0],"No keys") == 'No keys'}", source = __name__, level = 1)
            if not attribute_dict.get(target_attribute[0],"No keys") == 'No keys':
                logging_operation.write_log(f"{target_attribute[0]} -- same attribute name", source = __name__, level = 1)
                attribute_annotation_matching_result.pop(target_attribute[0])
            # elif target_attribute[0] in cls.accept_None():
            #     logging_operation.write_log(f"{target_attribute[0]} -- same attribute name", source = __name__, level = 1)
            #     attribute_annotation_matching_result.pop(target_attribute[0])
        # Check the result
        if len(attribute_annotation_matching_result) == 0:
            logging_operation.write_log("All attribute name match", source = __name__, level = 1)
            return True
        else:
            logging_operation.write_log(f"Not all attribute name match, the following attributes match unsuccessfully, \n{attribute_annotation_matching_result}", source = __name__, level = 1)
            return False
    
    @classmethod
    def tn_all(cls, origin_attribute:dict):
        '''
            # Introduction
            Check all the attributes to ensure if all are included(by attribute name) and if the attribute value can format to the annotation type
            
            # Attribute
            - attribute_dict: the target attribute and value to check, each item should have key-value pairs(attribute_name,attribute_value)
            
            # Returns
            - type:tuple(bool, list[cls])
            - True: Each Attribute is included in the attribute_dict and the attribute value can formate to the target type. Ignore the redundant attribute in the input attribute_dict
            - False: Miss one or more attribute or get a unformated value
            - list[cls]: if True - The dict of the normalized attributes, if False - the dict of the attributes which can not be normalized 
        '''
        attribute_annotation = cls.get_attribute_annotition()
        # logging_operation.write_log(f"In check_attribute, the target attributes are\n{attribute_annotation}\nThe attributes to check are {attribute_dict}", source = __name__, level = 1)
        # The returning list[cls]
        attribute_fail_to_normalize = attribute_annotation.copy()
        attribute_success_to_normalize = dict()
        
        if cls.check_attribute_name(origin_attribute):
            for target_attribute in attribute_annotation.items():
                # value(type) match or convertable 
                if isinstance(origin_attribute[target_attribute[0]],target_attribute[1]):
                    # Same value, delete it from the result dict 'attribute_annotation_matching_result' and add it to the result dict 'attribute_success_to_match'
                    logging_operation.write_log(f"{target_attribute[0],origin_attribute[target_attribute[0]]} -- same attribute value type", source = __name__, level = 1)
                    attribute_fail_to_normalize.pop(target_attribute[0])
                    attribute_success_to_normalize[target_attribute[0]] = origin_attribute[target_attribute[0]]
                elif (target_attribute[0] in cls.accept_None()) and tp_file.is_None_value(origin_attribute[target_attribute[0]]):
                    # None, delete it from the result dict 'attribute_annotation_matching_result' and add it to the result dict 'attribute_success_to_match'
                    logging_operation.write_log(f"{target_attribute[0],origin_attribute[target_attribute[0]]} -- NoneType", source = __name__, level = 1)
                    attribute_fail_to_normalize.pop(target_attribute[0])
                    attribute_success_to_normalize[target_attribute[0]] = origin_attribute[target_attribute[0]]
                elif not (normal_attribute_value := eval(f"cls.tn_{target_attribute[0]}")(origin_attribute[target_attribute[0]])) == None:
                    # type convertable, delete it from the result dict 'attribute_annotation_matching_result' and add it to the result dict 'attribute_success_to_match'
                    logging_operation.write_log(f"convert {target_attribute[0]}:{origin_attribute[target_attribute[0]]},from type {type(origin_attribute[target_attribute[0]])} to type {target_attribute[1]}-- convertable value type", source = __name__, level = 1)
                    attribute_fail_to_normalize.pop(target_attribute[0])
                    attribute_success_to_normalize[target_attribute[0]] = origin_attribute[target_attribute[0]]
                else:
                    # value match fail, set the result dict(attribute_annotation_matching_result) value of the attribute to (origin_attribute,target_attribute)
                    attribute_fail_to_normalize[target_attribute[0]] = (type(origin_attribute[target_attribute[0]]),target_attribute[1])
            logging_operation.write_log(f"Attribute {target_attribute} match over", source = __name__, level = 1)
        
        else:
            logging_operation.write_log(f"Fail to match attribute name", source = __name__, level = 1)

        # Check the result
        if len(attribute_fail_to_normalize) == 0:
            logging_operation.write_log("All attribute match", source = __name__, level = 1)
            return (True,attribute_success_to_normalize)
        else:
            logging_operation.write_log(f"Not all attribute match, the following attributes match unsuccessfully, \n{attribute_fail_to_normalize}", source = __name__, level = 1)
            return (False,attribute_fail_to_normalize)

    @classmethod
    def get_child_class(cls):
        '''
            Introduction:
            Get all the subclassed of DB_Table
        '''
        return cls.__subclasses__()
    
    @classmethod
    def primary_key(cls):
        '''
            # Introduction
            Get the primary key attribute name of the class entity
            
            # Returns
            The string name of the primary key
        '''
        primary_key:str = None
        return primary_key

    @classmethod    
    def auto_increase(cls):
        '''
            # Introduction
            Get the auto_increase attribute name list of the class entity
            
            # Returns
            The list of the attribute name that are auto increase
        '''
        auto_increase_list:list = []
        return auto_increase_list

    @classmethod
    def accept_None(cls):
        '''
            # Introduction
            Get the attribute name list of the class entity which can be None
            
            # Returns
            The list of the attribute name which can be None
        '''
        accept_None_list:list = []
        return accept_None_list
    
class DB_Table():
    
    pass
    