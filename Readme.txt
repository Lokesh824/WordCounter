                                            Word Counter

-> In this application with the given url the number of words in that page is calculated.
-> Redis Queue is used here for making the count operation async.
-> SQLLite DB is used for storing the results.

How the application works ?
    When the user enters the url in the form and submits,
    -> It is pushed to the Redis Queue by using the worker
    -> Here the user need not to wait until the count is compleated, it is async operations
    -> Once the operations (Count) is compleated then it is saved in the database.
    -> Index page shows all the jobs with the results.

How to Run the application ?
    ->Create the environment by command - py -m venv env.
    ->Activate the environment by navigating to application root folder -> env -> Scripts -> activate
    ->Create environment varibale - set FLASK_APP=app.py
    ->Install all the required libraries
    ->Run the Radix-Server by the command - 'radix-server'
    ->Important
        ->The fork() is not available in windows, then we need to have linux or have a custom worker used like - https://github.com/michaelbrooks/rq-win
    ->Then Spin up the custom worker by the command - 'rqworker -w rq_win.WindowsWorker'
    ->Now run the application by the command - flask run





