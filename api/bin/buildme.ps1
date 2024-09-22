$version=$args[0]
# write-host $version
docker build -t steve353/weatherapi:$version .