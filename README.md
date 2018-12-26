# django_util
### Delete, Update functionality for normalised models


## Use-Case : 

  * `Django util` provide state-full delete, update functionality for ORM(object relational mapping)level.
  
## Table of Content :
  
  * [State-full Delete/Update](#statefull)
     * [Get Affected Objects](#get-affected-objects)
     * [Delete Object](#delete-object)
     * [Update Object](#update-object)
  * [Installation](#installation)


## State-full Delete/Update
  * Below are functions inorder to get the state-full delete/update 
  ### Get Affected Objects
   * List out all objects which are affected because of object which is going to be deleted(Prompt-Messages).
   * `getAffectedObjects` takes input dict with id as key and reference of model.
   ```
   Sample Input : ({'id':1},model_reference)
   Output : Error_list(list),prompt messages(list)
   ```
  ### Delete Object
   * Delete object with all the dependent objects. 
   * `deleteObject` takes input dict with id as key and reference of model.
   ```
   Sample Input : ({'id':1,'force_delete':True},model_reference)
   Output : Error_list(list)
   ```
  ### Update Object 
   * Transferring Object dependencies from one object to another object.
   * `updateObjectDependencies` takes input source,destination objects.
   ```
   Sample Input : (source,destination)
   Output : Error_list(list)
   ```
* **Note** : Every function returns error_list so if its empty than only operation is successfull. 

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
         error_list,prompt_message = handler.getAffectedObjects({'id':1},m)
         // For Deletion with all dependent objects
         error_list = handler.deleteObject({'id':1,'force_delete':True},m)
         //Transferring Object dependencies
         error_list = utility.updateObjectDependencies(source,destination)
         
  * Output :
        Prompt Message of `getAffectedObjects` function
        
        [{'message': 'This object has been used in child 2 times.', 'model_name': 'child', 'Parent models': '', 'count': 2}]
      
         
          
    
    
