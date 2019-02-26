from .handler import OrmHandler

def getAffectedObjects(data, handler):
    return OrmHandler().delete_service(data, handler, exception_list=[])

def deleteObject(data,handler):
    error_list, affected_objects = OrmHandler().delete_service(data, handler, exception_list=[])
    return error_list

def updateObjectDependencies(source,destina sddsddsdtion):
    error_list  = OrmHandler().update_dependencies(source,destination)
    return error_list