docker run --name mysqlex --link biopano:mysql -e MYSQL_ROOT_PASSWORD=SyntheticBiology -d mysql

docker run --name mongoex --link biopano:mongo -d mongo

docker run -d -p 8080 dockerfile/python-runtime

docker run --name nginxex -v /some/nginx.conf:/etc/nginx.conf:ro -d nginx