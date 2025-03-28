FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build
RUN npm install -g serve

EXPOSE 3000

CMD ["npx", "serve", "-s", "dist", "-l", "3000"]

