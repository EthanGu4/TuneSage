# TuneSage

Music bot that generates random songs based on user specifications; used primarily to discover new tracks

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
