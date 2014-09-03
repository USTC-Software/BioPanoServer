# API document

## Instruction

All the following API(expect OAUTH) must have access_token parameter. 

For GET request, it should be added in URL, like:

	GET /groups&access_token=7dbd428f731035f771b8d15063f61864

For POST request, it should be added as a POST form parameter in request body.

The default response is in json, if you want the response in other format, please add parameter "format=XML", "format=YAML", etc. 

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
	
fail:
	
	'status': 'error',
	'reason': '<err_reason>'
	
	
## LIST GROUP

request:

	GET /group

response:

	{
		'groups':
		[
			{
				'group_name':'staff',
				'species_id':'Ecoli'
			},
			{
				‘group_name':'regulation',
				'species_id':'Pseudomonas'
			}
		]
	}


## ADD GROUP

request:

	POST /group
	
	group_name:<string>
	species:<string>

success response:

	{
		'status': 'success‘
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>'
	}


## CHOOSE GROUP

request:

	GET /group/<gname>

success response:

	{
		'status': 'success‘
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>'
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

success response:

	{
		'species_id': <string>
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>'
	}


## LOGIN(overdue):

request:

	POST /auth/login
	
	'username':'...'
	'password':'...'

success response:

	{
		'status': 'success‘,
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
	
## LOGOUT:

success request:
	
	POST /auth/logout

success response:

	{
		'status': 'success‘,
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
	
## DETAIL

request:

	GET /data/(node|link)/<ref_id>

success response:

	{
		I'm results
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
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
		
success response:

	{
		'ref_id': '<ref_id>'	
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}

## REFERENCE

request:

	POST /data/(node|link)
	
	'info':
	{
		'id': '123'
	}

success response:

	{
		'ref_id': '<ref_id>'	
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}


## DELETE

request:

	DELETE /data/(node|link)/<ref_id>

success response:

	{
		'status': 'success‘,
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
			
			
## SEARCH ENTRY

request:

	POST /search/(node|link)
	
	spec:{}
	fields:{}
	skip:[INTEGER]
	limit:[INTEGER]

default:

	skip:0
	limit:infinite

response:

	{
		result:
		[
			{
				'_id':'53f455e1af4bd63ddccee4a3',
				'NAME':'ehrL',
				'TYPE':'Gene'

			},
			{
				'_id':'53f455e1af4bd63ddccee4a4'
				'NAME':'thrA',
				'TYPE':'Gene'
			}
		]
	}
	
	<results>
  		<result>
    		<NAME>thrL</NAME>
    		<TYPE>Gene</TYPE>
    		<_id>53f455e1af4bd63ddccee4a3</_id>
  		</result>
  		<result>
    		<NAME>thrA</NAME>
    		<TYPE>Gene</TYPE>
    		<_id>53f455e1af4bd63ddccee4a4</_id>
  		</result>
  	</results>

### ex1

request :

	POST /search/(node|link)
		
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
	
explanation: 
	
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

仅返回NAME和TYPE字段

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

返回除了_ID以外的所有字段

request:

	POST /search/(node|link)
	
	'spec':
	{
	}
	'field':
	{
		'_ID':False
	}

	
## SEARCH RELATION(Developing):

request:

	POST /search/relation
	
	ID:<_ID>
	spec:{}
	fields:{}
	skip:[INTEGER]
	limit:[INTEGER]

default:

	skip:0
	limit:infinite

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