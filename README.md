# django_util
### Delete, Update functionality for normalised models


## Use-Case : 

  * `Django util` provide state-full delete, update functionality for ORM(object relational mapping)level.
  
## Table of Content :
  
  * [State-full Delete/Update](#statefull)
     * [Get Affected Objects](#get-affected-objects)
     * [Delete Object](#delete-object)
  * [Installation](#installation)


## State-full Delete/Update
  * Below are functions inorder to get the state-full delete/update 
  ### Get Affected Objects
   * List out all objects which are affected because of object which is going to be deleted(Prompt-Messages).
  ### Delete Object
   * Delete object with all the dependent objects. 
   
## Installation
  * Use Pip to install the module
    ```
    pip install module_name
    ```
## Usage :
  * Sample model : 
      
          class parent(models.Model):
            name = models.CharField(max_length=100)
            
          class child(models.Model):
            parent = models.ForeignKey(parent, on_delete=models.CASCADE) 
            name = models.CharField(max_length=100)
  
  * Code :
         
         from django_utils import handler
         m = models.parent
         // Get Prompt Message
         error_list,prompt_message = handler.get_affected_objects({'id':1},m)
         // For Deletion with all dependent objects
         error_list = handler.delete_object({'id':1,'force_delete':True},m)
         
  * Output :
        
        []
      
         
          
    
    
