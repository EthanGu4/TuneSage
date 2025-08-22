# TuneSage

A music discovery bot that generates personalized or random song recommendations based on user-selected genres and time periods, helping users explore and discover new tracks effortlessly

# SET-UP BACKEND

git clone repository

cd backend

activate virtual environment
.venv\Scripts\activate

pip install -r requirements.txt

add .env variables (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)

run backend server
uvicorn app:app --reload

test with http://127.0.0.1:8000/

# SET-UP FRONTEND

cd frontend
npm install

npm start

should open local host automatically
