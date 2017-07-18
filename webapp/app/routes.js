// create a new express router
const express = require('express'),
    router = express.Router(),
    messagesController = require('./controllers/messages.controller');

// export router
module.exports = router;

// define routes
// main routes
//router.get('/', mainController.showHome);
// get messages
router.get('/', messagesController.getDailyActivity);
// get daily activity
router.get('/all', messagesController.getMessages);
// seed messages
router.get('/messages/seed', messagesController.seedMessages);
// create message
router.post('/messages/create', messagesController.processCreate);
