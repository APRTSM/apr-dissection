<!-- @format -->

# APR-Dissection

## Shortcuts
- [The Data Folder](https://github.com/APRTSM/apr-dissection/tree/main/src/dissection/data)

## Run The Server
- 1) Docker
  - Requirements:
    - Docker
  - Clone the Repository.
  - Go to `apr-dissection/`
  - Run `docker-compose up -d --build`
    - If the error `docker-compose not found` accured, install docker-compose.
  - If the container runs successfully, you may visit [the page](http://127.0.0.1:8000/dissection/).
 
- 2)
  - Requirements:
    - Python 3.10
  - Go to `apr-dissection/src/`
  - Run `source init.sh`
    - You may need to change the content of `apr-dissection/src/init.sh` file (e.g. using `python `instead of `python3`) but commands are straight forward.
  - If the server runs successfully, you may visit [the page](http://127.0.0.1:8000/dissection/).
