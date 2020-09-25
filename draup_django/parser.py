class OrmParser:

    def __init__(self):
        pass

    # get all related object fields

    def _get_all_object_field(self, obj):
        return obj._meta._get_fields(forward=False, reverse=True, include_hidden=True) if obj else None

    # get all one to many field

    def _get_one_to_many_field(self, all_related_fields):
        return [obj for obj in all_related_fields if not obj.hidden and not obj.field.many_to_many]

    def _process_operation(self,data,object_to_delete, to_be_called_name_passed, deletion_set, parent_set_dict):

        if (to_be_called_name_passed in deletion_set):
            deletion_set[to_be_called_name_passed] += data
        else:
            deletion_set[to_be_called_name_passed] = data
        if (to_be_called_name_passed != object_to_delete._meta.model_name):
            if (to_be_called_name_passed in parent_set_dict):
                if (parent_set_dict[to_be_called_name_passed].count(object_to_delete._meta.model_name) == 0):
                    parent_set_dict[to_be_called_name_passed].append(object_to_delete._meta.model_name)
            else:
                parent_set_dict[to_be_called_name_passed] = [object_to_delete._meta.model_name]
        return deletion_set, parent_set_dict