# Chatapp Backend (Basic Skeleton)

Osnovna backend struktura za real-time chat projekt.

## Tehnologije
- Node.js
- Express
- Nodemon
- PostgreSQL
- Prisma

## Struktura

```txt
backend/
  src/
    config/
    controllers/
    db/
    middlewares/
    routes/
    services/
    sockets/
    utils/
    app.js
    server.js
  .env.example
  .gitignore
  package.json
```

## Hiter zagon

1. Namesti odvisnosti:
   ```bash
   npm install
   ```
2. Ustvari `.env` iz template:
   ```bash
   cp .env.example .env
   ```
3. Generiraj Prisma client:
   ```bash
   npm run prisma:generate
   ```
4. Zaženi razvojni strežnik:
   ```bash
   npm run dev
   ```

## Baza (PostgreSQL + Prisma)

- Connection string je v `.env` pod `DATABASE_URL`.
- Inicialna Prisma shema je v `prisma/schema.prisma`.
- Ko boš dodal modele, zaženi migracijo:

```bash
npm run prisma:migrate -- --name init
```

- Prisma Studio (pregled baze):

```bash
npm run prisma:studio
```

## Osnovni endpoint
- `GET /api/health`
