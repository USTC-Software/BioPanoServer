#NEW API
##ADD_URL:

POST

	^$host/api/node/add/$
	
request:
	
	'info': 
	{
		'TYPE': 'Gene',
		'NAME': 'trnL',
		...
	}
	
	'group':
	<group_name>	
		
response:

	{
		'status': 'success',
		'ref_id': '<ref_id>'	
	}
	
	OR
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}

	
##DELETE_URL:

POST

	^$host/api/node/delete/<ref_id>/$

request:

	{
		'ref_id': '<ref_id>'
	}			
	
response:

	{
		'status': 'success‘,
	}
	
	OR
	
	OR
	
	{
		'status': 'error',
		'reason': '<err_reason>',
	}
			
			
##SEARCH_URL

	POST
	^$host/api/search/$

###request(json)
	
	'query':
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
	

####others usages:

	'query':
	{
		"age":
		{
			"$gt":18
		}
	}
	
	age>18
	< : "$lt"
	> : "$gt"
	<= : "$le"
	>= : "$ge"
	!= : "$ne"
	
	
	
###response

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
  	

	
	
	
	
	
	
	

			
			
			
			
			
			
			