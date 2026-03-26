const { PrismaClient } = require('@prisma/client');

const globalForPrisma = global;

const prisma = globalForPrisma.prisma || new PrismaClient();


// če je dev env, se doda Prisma client na globalni objekt, da se 
// prepreči večkratna inicializacija med hot reloadingom

if (process.env.NODE_ENV !== 'production') {
	globalForPrisma.prisma = prisma;
}

module.exports = prisma;
