const express = require('express');
const prisma = require('../db');
const { hashPassword } = require('../utils/password');

const router = express.Router();

router.get('/health', (req, res) => {
  res.status(200).json({ ok: true, message: 'Backend is running' });
});

router.get('/users', async (req, res) => {
  try {
    const users = await prisma.user.findMany();
    res.json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Failed to fetch users', details: error.message });
  }
});

router.post('/users', async (req, res) => {
    const { username, email, password } = req.body;
    try {
        const hashedPassword = await hashPassword(password);
        const newUser = await prisma.user.create({
            data: { username, email, password: hashedPassword },
        });
        res.status(201).json(newUser);
        } catch (error) {
        console.error('Error creating user:', error);
        res.status(500).json({ error: 'Failed to create user', details: error.message });
    }
}); 



module.exports = router;
