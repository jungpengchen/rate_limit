#run container with bash
#docker run --rm -it -p 8000:8000 -v /Users/chenam/Documents/work/git_repo/LexiQuiz:/home/lexiquiz/LexiQuiz --name lexiquiz-server --env-file=.env lexiquiz:test bash
#run container
#docker run --rm -it -p 8000:8000 --env-file=.env --name lexiquiz-server lexiquiz:test
uvicorn test_app:app --host 0.0.0.0 --port 8000 --reload