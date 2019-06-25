from .parser import OrmParser
import traceback
class OrmHandler:

    def __init__(self):
        self.error_list = []
        self.affected_object = []
        self.parser = OrmParser()

    """
    Filtering all type of fields(one to one, one to many,many to one)
    """

    def delete_functionality(self, object_to_delete, deletion_set, parent_set_dict, exception_list):
        try:
            """
            Filtering one to many fields
            """
            all_related_fields = self.parser._get_all_object_field(object_to_delete)
            field_list = self.parser._get_one_to_many_field(all_related_fields)

            for i in range(len(field_list)):
                to_be_called_name = field_list[i].name
                if to_be_called_name[-1] == '+':
                    to_be_called_name = to_be_called_name[0:-1]
                to_be_called_name_passed = ''.join(e for e in to_be_called_name if e.isalnum()).lower()
                field_to_test = to_be_called_name.lower() + '_set'
                if hasattr(object_to_delete, field_to_test):
                    to_be_called = getattr(object_to_delete, field_to_test)
                    data = to_be_called.count()
                    if data > 0:
                        deletion_set, parent_set_dict = self.parser._process_operation(data,object_to_delete,
                                                                                       to_be_called_name_passed,
                                                                                       deletion_set, parent_set_dict)
                else:
                    if (field_list[i].__dict__['related_name']):
                        to_be_called_name = field_list[i].__dict__['related_model'].__name__
                        to_be_called_name_passed = ''.join(e for e in to_be_called_name if e.isalnum()).lower()
                        if hasattr(object_to_delete, field_list[i].__dict__['related_name']):
                            to_be_called = getattr(object_to_delete, field_list[i].__dict__['related_name'])
                            data = to_be_called.count()
                            if data > 0:
                                deletion_set, parent_set_dict = self.parser._process_operation(data,object_to_delete,
                                                                                               to_be_called_name_passed,
                                                                                               deletion_set,
                                                                                               parent_set_dict)
                        else:
                            if (to_be_called_name == ''):
                                continue
                            exception_list.append({"Error message": "Data from " + to_be_called_name + " with dependencies on this will be deleted"})
                            continue
                if (to_be_called_name.lower() == object_to_delete._meta.model.__name__.lower()):
                    continue
                to_be_iterated = to_be_called.model.objects.filter(**to_be_called.core_filters)

                """
                Filtering many to many fields
                """
                manytomanylist = object_to_delete._meta.__dict__['local_many_to_many']
                for i in manytomanylist:
                    to_be_called_name_passed = i.model.__name__ + '_' + i.__dict__['name']
                    to_be_called_name = i.__dict__['name']
                    if (hasattr(object_to_delete, to_be_called_name)):
                        to_be_called = getattr(object_to_delete, to_be_called_name)
                        data = to_be_called.count()
                        if data > 0:
                            if (to_be_called_name_passed in deletion_set):
                                deletion_set[to_be_called_name_passed] += data
                            else:
                                deletion_set[to_be_called_name_passed] = data

                for item_obj in to_be_iterated:
                    deletion_set, parent_set_dict = self.delete_functionality(item_obj, deletion_set, parent_set_dict,
                                                                              exception_list)

            """
            Filtering one to one fields
            """
            iter_all_fields = object_to_delete._meta.fields
            one_to_one_list = []
            for i in iter_all_fields:
                if i.one_to_one:
                    if hasattr(i, 'rel') and i.rel.on_delete.__name__ != 'DO_NOTHING':
                        one_to_one_list.append(i)
                    elif hasattr(i, 'remote_field') and i.rel.on_delete.__name__ != 'DO_NOTHING':
                        one_to_one_list.append(i)

            for i in one_to_one_list:
                primary_id = getattr(object_to_delete, i.__dict__['column'])
                to_be_called_name = i.related_model.__name__.lower()
                if to_be_called_name in deletion_set:
                    deletion_set[to_be_called_name] += 1
                else:
                    deletion_set[to_be_called_name] = 1
                item_obj = i.__dict__['related_model'].objects.get(pk=primary_id)
                deletion_set, parent_set_dict = self.delete_functionality(item_obj, deletion_set,
                                                                          parent_set_dict,
                                                                          exception_list)
        except Exception as e:
            self.error_list.append({'Error message': str(traceback.format_exc())})
        return deletion_set, parent_set_dict

    """
    Building exception list of effected objects
    """

    def get_exception_list(self, deletion_set, parent_set_dict, exception_list):

        for key, val in list(deletion_set.items()):
            model_display_name = key
            message = "This object has been used in " + key + " " + str(
                val) + " times."
            parent_models = ''
            if (key in parent_set_dict):

                def get_parents(parent_set_dict, key):
                    if key in parent_set_dict:
                        return parent_set_dict[key]
                    return ''

                def get_list_for_list(parent_set_dict, key_list):
                    list_a = []
                    for i in key_list:
                        list_b = get_parents(parent_set_dict, i)
                        list_a = list(set(list_a).union((set(list_b) - set(list_a))))
                    return list_a

                def string_a_list(list_a):
                    parent_str = ''
                    for i in list_a:
                        if (parent_str == ''):
                            parent_str = i
                        else:
                            parent_str = parent_str + ',' + i
                    return parent_str

                parent_models = string_a_list(parent_set_dict[key])
                other_list = []
                query_list = parent_set_dict[key]
                while (1):
                    list_to_append = get_list_for_list(parent_set_dict, query_list)
                    if (other_list == []):
                        other_list.append(list_to_append)
                        query_list = list_to_append
                    elif (set(list_to_append) - set(other_list[-1])):
                        other_list.append(list_to_append)
                        query_list = list_to_append

                    else:
                        break
                for i in other_list:
                    if (string_a_list(i) != ''):
                        parent_models = parent_models + ' which is under ' + string_a_list(i)

            exception_list.append(
                {"message": message, "model_name": model_display_name, "Parent models": parent_models, "count": val})

        return exception_list

    """
    Deletion of one to one objects
    """

    def delete_one_to_one(self, delete_element, id):
        element_fields = delete_element._meta.__dict__['fields']
        for field in element_fields:
            if field.one_to_one:
                parent_model = field.__dict__['related_model']
                parent_id = getattr(delete_element, field.column)
                parent_element = parent_model.objects.filter(id=parent_id).first()
                parent_element.delete()

    """
    Processing deletion based on parameters passed
    """

    def delete_service(self, data, handler, exception_list):
        try:
            deletion_set = {}
            parent_set_dict = {}
            id = data['id'] if 'id' in data else None
            force_delete = data['force_delete'] if 'force_delete' in data else False
            object_to_delete =handler.objects.filter(id=id)
            delete_element = object_to_delete.first()
            if not delete_element:
                raise Exception(str(delete_element) + ' element not found with id %s' % (id))
            element_fields = delete_element._meta.__dict__['fields']
            flag = 0
            for field in element_fields:
                if field.one_to_one and field.rel.on_delete.__name__ != 'DO_NOTHING':
                    flag = 1
            if force_delete:
                if flag == 1:
                    self.delete_one_to_one(delete_element, id)
                else:
                    object_to_delete.delete()
            else:
                deletion_set, parent_set_dict = self.delete_functionality(delete_element, deletion_set, parent_set_dict,
                                                                          exception_list)
                self.affected_object = self.get_exception_list(deletion_set, parent_set_dict, exception_list)
        except Exception as e:
            self.error_list.append({'Error message': str(e)})
        return self.error_list, self.affected_object

    
    """
    Updating foreign/Many-to-Many field dependencies from one to another object
    """
    def update_dependencies(self, source, destination):
        try:
            all_related_fields = self.parser._get_all_object_field(source)
            field_list = self.parser._get_one_to_many_field(all_related_fields)
            for iter in range(0, len(field_list)):
                to_be_called_name = field_list[iter].name
                if to_be_called_name[-1] == '+':
                    to_be_called_name = to_be_called_name[0:-1]
                field_to_test = to_be_called_name.lower() + '_set'
                field_name = None
                if hasattr(source, field_to_test):
                    reference_objs = getattr(source, field_to_test)
                    ids = reference_objs.values_list('id')
                    for iter_in in reference_objs.model._meta._get_fields():
                        if hasattr(iter_in, 'related_model') and iter_in.related_model == source.__class__:
                            field_name = iter_in.column
                    for iter_in in ids:
                        reference_objs.model.objects.filter(id=iter_in[0]).update(**{field_name: destination.id})
                else:
                    if field_list[iter].__dict__['related_name']:
                        if hasattr(source, field_list[iter].__dict__['related_name']):
                            reference_objs = getattr(source, field_list[iter].__dict__['related_name'])
                            ids = reference_objs.values_list('id')
                            for iter_in in reference_objs.model._meta._get_fields():
                                if hasattr(iter_in,'related_model') and (
                                        (hasattr(iter_in.related_model,'model') and
                                         iter_in.related_model.model == source.__class__) or
                                        (hasattr(iter_in.related_model,'_meta') and
                                         hasattr(iter_in.related_model._meta,'model')
                                         and iter_in.related_model._meta.model == source.__class__)):
                                    field_name = iter_in.column
                            for iter_in in ids:
                                reference_objs.model.objects.filter(id=iter_in[0]).update(**{field_name: destination.id})
                    else:
                        continue
                if (to_be_called_name.lower() == source._meta.model.__name__.lower()):
                    continue
                manytomany = source._meta.__dict__['local_many_to_many']
                for iter in manytomany:
                    to_be_called_name = iter.__dict__['name']
                    if hasattr(source, to_be_called_name):
                        reference_objs = getattr(source, to_be_called_name)
                        field_name = source._meta.model_name + '_id'
                        ids = reference_objs.through.objects.filter(**{field_name:source.id}).values_list('id')
                        for iter_in in ids:
                            reference_objs.through.objects.filter(id=iter_in[0]).update(**{field_name:destination.id})
        except Exception as e:
            self.error_list.append({'Error message': str(e)})
        return self.error_list