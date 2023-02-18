# Build the FakeAPI Docker container
SOURCE=~/Documents/Projets/Programming/Python/Sources/REST_API/MongoDB
cp $SOURCE/* ./src/.
cp $SOURCE/.env ./src/.
docker build -t fakeapi .
