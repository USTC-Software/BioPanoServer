# API document

## Instruction

All the following API(expect OAUTH) must have access_token parameter. 

For GET request, it should be added in URL, like:

	GET /projects&access_token=7dbd428f731035f771b8d15063f61864

For POST request, it should be added as a POST form parameter in request body.

The default response is in json, if you want the response in other format, please add parameter "format=XML", "format=YAML", etc. 

If anything goes south, you will get a error response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}

## DIRECTORY

	POST	/auth/oauth/(baidu|google)/login
	GET		/auth/oauth/(baidu|google)/complete&...
	GET		/user/<uid>
	GET		/project
	POST	/project
	GET		/project/<pid>
	POST	/project/<pid>/collaborator
	DELETE	/project/<pid>/collaborator/<uid>
	GET		/species
	POST	/species
	GET		/species/<sid>
	GET		/data/(node|link)/<ref_id>
	POST	/data/(node|link)
	DELETE	/data/(node|link)/<ref_id>
	GET		/data/(node|link)/<ref_id>/link
	POST	/search/(node|link)
	POST	/search/user
	POST	/search/project
	POST	/algorithm/shortestpath
	POST	/algorithm/blastn

## OAUTH LOGIN:

request:

	POST /auth/oauth/(baidu|google)/login

When the user login in sucessfully, the pages will redict to the /auth/oauth/<baidu|google>/complete

## OAUTH COMPLETE

request(automaticlly):

	GET /auth/oauth/(baidu|google)/complete&....

success :

	{
		"status": "success",
	 	"token": "16517d0809f225b7b65a79ef1dc8c552441bf58a", 
	 	"uid": 8
	}	
	
## LIST PROJECT

request:

	GET /project

response:

	{
		'projects':
		[
			<pid>
		]
	}


## ADD PROJECT

request:

	POST /project
	
	project_name:<string>
	species:<string>
	description:<string>

response:

	{
		'pid':...
	}


## PROJECT INFO

request:

	GET /project/<pid>

success response:

	{
		'pid':....,
		'prooject_name':...,
		'species':...,
		'description':...,
		'collaborators':
		[
		]
	}

## DELETE PROJECT

request:

	DELETE /project/<pid>

response:

	{
		'status':'success'
	}

## ADD COLLABORATOR

request:

	POST /project/<pid>/collaborator
	collaborator:<uid>

response:

	{
		'status':'success'
	}

## DELETE COLLABORATOR

request:

	DELETE /project/<pid>/collaborator/<uid>

response:

	{
		'status':'success'
	}

## LIST SPECIES

request:

	GET /species

response:

	{
		'species':
		[
			{
				'species_id': <string>,
				'species_name':'Ecolo'
			},
			{
				'species_id': <string>,
				'species_name':'Pseudomonas'
			}
		]
	}


## ADD SPECIES

request:

	POST /species
	
	species_name: <string>

response:

	{
		'species_id': <string>
	}

	
## LOGOUT:

request:
	
	POST /auth/logout

response:

	{
		'status': 'success‘,
	}
	

	
## DETAIL

request:

	GET /data/(node|link)/<ref_id>

response:

	{
		I'm results
	}


## ADD

request:

	POST /data/(node|link)
	
	info: 
	{
		'TYPE': 'Gene',
		'NAME': 'trnL',
		...
	}
		
response:

	{
		'ref_id': '<ref_id>'	
	}
	

## REFERENCE

request:

	POST /data/(node|link)
	
	'info':
	{
		'id': '123'
	}

response:

	{
		'ref_id': '<ref_id>'	
	}

## DELETE

request:

	DELETE /data/(node|link)/<ref_id>

response:

	{
		'status': 'success‘,
	}
		

## NODE TO LINK

request:

	GET /data/node/<ref_id>/link

response:

	{
		'links':
		[
			7dbd428f731428f703,
			5f771b8d158d157063,
			...
		]
	}
	
## SEARCH NODE|LINK

request:

	POST /search/(node|link)
	
	method:query
	spec:{}
	fields:{}
	skip:[INTEGER]
	limit:[INTEGER]

default:

	skip:0
	limit:infinite

response:

	{
		results:
		[
			{
				'_id':'53f455e1af4bd63ddccee4a3',
				'NAME':'ehrL',
				'TYPE':'Gene',
				'....':'...'

			},
			{
				'_id':'53f455e1af4bd63ddccee4a4'
				'NAME':'thrA',
				'TYPE':'Gene',
				'....':'...'
			}
		]
	}

### ex1

request :

	POST /search/(node|link)
		
	'spec':
	{
		"$and":
		[
			{"$or":
			[
				{"key1":"abc"},
				{"key2":123},
				{"key3":"sfda"}
			]},
			{"key4":"feiyicheng"}
		]
	}
	
explain: 
	
	(key1 || key2 || key3) && key4
	
### ex2

request:

	POST /search/(node|link)
	
	'spec':
	{
		"age":
		{
			"$gt":18
		}
	}


explain:

	< : "$lt"
	> : "$gt"
	<= : "$le"
	>= : "$ge"
	!= : "$ne"

### ex3

only return ID, NAME and TYPE fileds

request:

	POST /search/(node|link)
	
	spec:
	{
	}
	field:
	{
		'NAME':True,
		'TYPE':True
	}



### ex4

return all fileds except NAME

request:

	POST /search/(node|link)
	
	'spec':
	{
	}
	'field':
	{
		'NAME':False
	}

## SEARCH USER

request:

	POST /search/user
	
response:

	//TODO


## SEARCH PROJECT

request:

	POST /search/project

response:

	//TODO

## SHORTESTPATH

request:
	
	POST /algorithm/shortestpath
	
	ID1:<string>
	ID2:<string>
	global:[boolean]

default:

	global:False

response:

	{
		results:
		[
			{
				node:[1,2,3,4,5],
				link:[12,23,34,45]
			},
			{
				node:[1,2,7,8,9,10,11],
				link:[......]
			}
		]
	}

## BLASTN

request:

	POST /algorithm/blastn
	//TODO