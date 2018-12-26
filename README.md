# django_util
### Delete, Update functionality for normalised models


## Use-Case : 

  * `Django util` provide statefull delete, update functionality for ORM(object relational mapping)level.
  
## Table of Content :
  
  * [Statefull Delete/Update](#statefull)
     * [Get Affected Objects](#get-affected-objects)
     * [Delete Object](#delete-object)
     * [Update Object](#update-object)
  * [Installation](#installation)


## Statefull Delete/Update
  * Below are functions inorder to get the statefull delete/update
 
  ### Get Affected Objects
   * List out all dependent objects(Prompt-Messages).
   * `getAffectedObjects` takes input dict with id as key and reference of model.
   
   ```
   Sample Input : ({'id':1},model_reference)
   Output : Error_list(list),prompt messages(list)
   ```
   
  ### Delete Object
   * Delete object with all the dependent objects. 
   * `deleteObject` takes input dict with id and force_delete as key and reference of model.
   
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

## Installation
  * Use Pip to install the module
  
    ```
    pip install draup-django
    ```
    
## Usage :
  * Sample model : 
      
          class parent(models.Model):
            name = models.CharField(max_length=100)
            
          class child(models.Model):
            parent = models.ForeignKey(parent, on_delete=models.CASCADE) 
            name = models.CharField(max_length=100)
      
  *  Parent Table :
  
     | id     | Name      |
     | ------ | --------- |
     |  1     |  Alice    |
     |  2     |  Tom      |
  
 * Child Table :
  
     | id          | Name       |  parent_id    |
     | ----------- |  --------- |-------------- |
     |  1          |  Bob       |     1         |
     |  2          |  Jack      |     2         | 

  
  * Code :
         
         from draup_django import utility
         m = models.parent

         """
         Get Prompt Message
         """

         error_list,prompt_message = utility.getAffectedObjects({'id':1},m)

         """
         Deletion with all dependent objects
         """
         error_list = utility.deleteObject({'id':1,'force_delete':True},m)

         """
         Transferring Object dependencies
         """

         source = m.objects.filter(id=1).first()
         destination = m.objects.filter(id=2).first()
         error_list = utility.updateObjectDependencies(source,destination)
         
  * Output :
        Prompt Message of `getAffectedObjects` function
        
        [{'message': 'This object has been used in child 1 times.', 'model_name': 'child', 'Parent models': '', 'count': 1}] 
         
  * **Note** : 
       -  Every function returns error_list so if its empty than only operation is successfull. 
       -  According to above Child/Parent Table `updateObjectDependencies` function will transafer object dependency from `id:1` to `id:2` so parent_id of `Bob` will become `2`. 
   
## Limitation :
   * `updateObjectDependencies` will not work in case of unique constraint,one to one field in model
   
