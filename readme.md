### Mysql with Docker

```dockerfile
docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD=kolotodos2 -e MYSQL_DATABASE=todos -d -v todos:/db --name todos mysql:8.0 
# -e MYSQL_ROOT_PASSWORD=todos: mysql root pwd setting
# -e MYSQL_DATABASE=todos: database create and naming is todos
# -d: background option
# -v: volume option 
# --name: container name
# mysql:8.0: git pull mysql v8.0
```

### Redis with Docker
```dockerfile
docker run -d --name my_redis -p 11548:6379 -e REDIS_PASSWORD=yourpassword redis
```
