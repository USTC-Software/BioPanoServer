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

	POST	/auth/oauth/authorize
	GET		/project
	POST	/project
	GET		/project/<project_id>
	GET		/species
	POST	/species
	GET		/species/<species_id>
	GET		/data/(node|link)/<ref_id>
	POST	/data/(node|link)
	DELETE	/data/(node|link)/<ref_id>
	GET		/data/(node|link)/<ref_id>/link
	POST	/batch/(node|link)
	POST	/search/(node|link|node_ref|link_ref)
	POST	/algorithm/shortestpath

## OAUTH:

request:

	POST /auth/oauth/authorize
	
	'client_id':保留参数
	'response_type':'token'
	'redirect_uri':回调地址

When the user login in sucessfully, the pages will redict to the “redict_url” with the following parameters:
success :

	'status': 'success‘,
	‘access_token': '...',
	'refresh_token': '...',
	'expires_in':'18000'
	
	
## LIST PROJECT

request:

	GET /project

response:

	{
		'projects':
		[
			{
				'project_name':'staff',
				'species_id':'Ecoli'
			},
			{
				‘project_name':'regulation',
				'species_id':'Pseudomonas'
			}
		]
	}


## ADD PROJECT

request:

	POST /project
	
	project_name:<string>
	species:<string>

response:

	{
		'status': 'success‘
	}


## CHOOSE PROJECT

request:

	GET /project/<gname>

success response:

	{
		'status': 'success‘
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


## LOGIN(overdue):

request:

	POST /auth/login
	
	'username':'...'
	'password':'...'

response:

	{
		'status': 'success‘,
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

	GET /data/(node|link)/<ref_id>/link

response:

	{
		'links':
		[
			7dbd428f731428f703,
			5f771b8d158d157063,
			...
		]
	}
	
## BATCH QUERY

request:

	POST /batch/(node|link)
	
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

	POST /batch/(node|link)
		
	'spec':
	{
		"$and":
		{
			"$or":
			{
				"key1":"abc",
				"key2":123,
				"key3":"sfda"
			},
			"key4":"feiyicheng"
		}
	}
	
explain: 
	
	(key1 || key2 || key3) && key4
	
### ex2

request:

	POST /batch/(node|link)
	
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

	POST /batch/(node|link)
	
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

## SEARCH

request:

	POST /search/(node|link|node_ref|link_ref)

instructions:

	find record in the database directly

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