# NEW API

## LOGIN:

request:

	POST /login/
	
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
	
	POST /logout/

success response:

	{
		'status': 'success‘,
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
	

## ADD:

request:

	POST /api/(node|link)/
	
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

## REF:

request:

	POST /api/(node|link)/
	
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
	
## DELETE:

request:

	DELETE /api/(node|link)/<ref_id>/

success response:

	{
		'status': 'success‘,
	}
	
fail response:
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
			
			
##SEARCH_URL

request:

	POST /api/(node|link)/search/
	
	'spec':{}
	'fields':{}
	'skip':[INTEGER]
	'limit':[INTEGER]

response:

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

	POST /api/(node|link)/search/
		
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

	POST /api/(node|link)/search/
	
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

	POST /api/(node|link)/search/
	
	'spec':
	{
	}
	'field':
	{
		'NAME':True,
		'TYPE':True
	}



### ex4

返回除了_ID以外的所有字段

request:

	POST /api/(node|link)/search/
	
	'spec':
	{
	}
	'field':
	{
		'_ID':False
	}

	
	
	
	
	
	
	

			
			
			
			
			
			
			