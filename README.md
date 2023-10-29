## GPT Food Finder
GPT Food Finder is a chat bot that provides intelligent restaurant recommendations based on the user's preferences and location.

## Tech Stack and Tools
Our tech stack is fastAPI back end and react front end. We used Yelp API to get restaurants near the users current location, retrieved from the user's IP. We then constructed a prompt for OpenAI using relevant information from the Yelp API response. This provides the chat bot with context for the conversation, allowing it to have knowledge nearby food options. For example, the user can ask for "vegan" and the bot is intelligent enough to recommend something like "Indian".

## How to Use
- clone the project
Run frontend server:
- cd frontend/react-typescript
- npm install
- npm run dev
Run backend server:
- pip install -r requirements.txt
- uvicorn main:app --reload

## Example
![hacks](https://github.com/am831/cal_hacks/assets/59581465/0a2c11aa-2a33-4f17-a2ed-147ae10cf374)
