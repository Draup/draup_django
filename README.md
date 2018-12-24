# django_util
### Delete, Update functionality for normalised models


## Use-Case : 

  * `Django util` provide state-full delete, update functionality for ORM(object relational mapping)level.
  
## Table of Content :
  
  * [State-full Delete/Update](#statefull)
     * [Get Affected Objects](#get-affected-objects)
     * [Delete Object](#delete-object)
  * [Installation](#installtion)


## State-full Delete/Update
  * Below are functions inorder to get the state-full delete/update 
  ### Get Affected Objects
   * List out all objects which are affected because of object which is going to be deleted(Prompts).
  ### Delete Object
   * Delete object with all the dependent objects. 
## Usage :
  * `Sample model` : 
      
          class parent:
            name = models.CharField(max_length=100)
            
          class child:
            parent = models.ForeignKey(parent, on_delete=models.CASCADE) 
            name = models.CharField(max_length=100)
          
    
    
