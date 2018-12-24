# django_util
Delete, Update functionality for normalised models


## Use-Case : 

  * `Django util` provide state-full delete, update functionality for ORM(object relational mapping)level.
  
## Table of Content :
  
  * [State-full Delete/Update](#statefull)
     * [get_affected_objects](#get-objects)
     * [delete_object](#delete-object)

 
## Usage :
  * `Sample model` : 
      
          class parent:
            name = models.CharField(max_length=100)
            
          class child:
            parent = models.ForeignKey(parent, on_delete=models.CASCADE) 
            name = models.CharField(max_length=100)
          
    
    
