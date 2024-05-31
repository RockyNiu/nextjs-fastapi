# nextjs-fastapi
This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`]

## Getting Started
- cd docker
- docker-compose -f docker-compose.yml -f docker-compose-frontend.yml up -d --build

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Development
- cd backend
- follow instructions in backend/README.md
- cd docker
- docker-compose -f docker-compose.yml -f docker-compose-deubg.yml up -d --build #backend
- # debug backend in vscode

- cd ../frontend
- follow instructions in frontend/README.md
- # modify frontend code in vscode