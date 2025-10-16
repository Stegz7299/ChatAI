<h1>This is my personal project</h1> 

Making personal ChatBot AI using Redis, FastAPI with Python and HuggingFace for the model

The base of this project is from the creator on the same title<br>
Stephen Sanwo (Thank You So Much)

all the base i got is from the codecamp he made
but since what he does is very old and have a lot of errors, and not mostly compatible for windows,
i made one here. it all work. but still research some features here

i follow and did some tweaks to make it work. overall the backend is from his tutorial.
took 2 years till this fully work (yeah since im still new)

if you want to take the repository and make this work n run, there are some things you need to add.
1. .env
   that contain<br>
   export REDIS_URL=<REDIS URL PROVIDED IN REDIS CLOUD><br>
   export REDIS_USER=<REDIS USER IN REDIS CLOUD><br>
   export REDIS_PASSWORD=<DATABASE PASSWORD IN REDIS CLOUD><br>
   export REDIS_HOST=<REDIS HOST IN REDIS CLOUD><br>
   export REDIS_PORT=<REDIS PORT IN REDIS CLOUD><br>
   export HF_TOKEN=<YOUR TOKEN FROM HF><br>
   export HF_MODEL=<YOUR MODEL THAT YOU TAKE FROM HF><br>

   make sure those in /worker and /server/src folders
   also make sure if your model is text generation (yeah it still text generation)

2. make sure you run env\Scripts\Activate.ps1 first (in windows powershell terminal and create one if none)
3. before running main.py in /server, make sure do $env:APP_ENV="development" first. (after steps 2 and no need to that for worker main.py)
4. ALWAYS run both main.py

<footer>Thank You</footer>
