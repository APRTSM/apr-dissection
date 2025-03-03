# APR-Dissection

## Shortcuts
- [Data](https://github.com/APRTSM/apr-dissection/tree/main/src/dissection/data)
- [Reports](https://github.com/APRTSM/apr-dissection/blob/main/reports.md)
- [Reading List](https://github.com/APRTSM/apr-dissection/blob/main/reading-list.md)

## Run The Server
- ## 1) Docker
  - Requirements:
    - `docker` (Latest version should work.)
    - `docker-compose` (Latest version should work.)
  - Clone the Repository.
  - Go to `apr-dissection/`
  - Run `docker-compose up -d --build`
    - If the error `docker-compose not found` occurred, install docker-compose.
  - If the container runs successfully, you may visit [the page](http://0.0.0.0:8000/).
 
- ## 2) Not Using Docker
  - Requirements:
    - Python 3.10
  - Go to `apr-dissection/src/`
  - Run `source init.sh`
    - You may need to change the content of `apr-dissection/src/init.sh` file (e.g. using `python` instead of `python3`).
  - If the server runs successfully, you may visit [the page](http://127.0.0.1:8000/).
