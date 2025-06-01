FROM node:22-slim

WORKDIR /app

# キャッシュをクリアして依存関係をクリーンインストール
COPY package.json ./
RUN npm cache clean --force && npm install --no-package-lock --force

# アプリケーションのソースコードをコピー
COPY . .

# ビルド
RUN npm run build

# ポートの公開
EXPOSE 3000

# アプリケーションの起動
CMD ["npm", "start"]
