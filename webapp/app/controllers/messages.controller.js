const Message = require('../models/message');

module.exports = {
    getMessages: getMessages,
    checkNoActivity: checkNoActivity,
    seedMessages: seedMessages,
    processCreate: processCreate,
    getDailyActivity: getDailyActivity
};

/**
 * Get all messages
 */
function getMessages(req, res) {
    // get all messages
    Message.find({}, function (err, messages) {
        if (err) {
            res.status(404);
            res.send('Messages not found!');
        }

        // return a view with data
        res.render('pages/home', {
            messages: messages
        });
    });
}

/**
 * Checking if no activity ( = if time between 2 messages > 11 minutes)
 */
function checkNoActivity(req, res) {
    // get last 2 messages
    var query = Message.find({});
    query.sort({time: 'desc'});
    query.limit(1);
    query.exec(function (err, messages) {
        if (err) {
            console.log('No messages found!');
        } else {
            var now = new Date();
            var lastMessageTime = new Date(messages[0].time);

            console.log("Delta time (now - last): " + (now - lastMessageTime).toString());

            if((now - lastMessageTime) > 660000){ // 11 minutes
                var message = {
                    "device": "2D24E6",
                    "time": now.getTime(),
                    "data": "0"
                };
                var newMessage = new Message(message);
                saveMessageInDB(newMessage, res);
                console.log('Adding a 0% efficiency!');
            } else {
                console.log('No need to add a record.');
            }
        }
    });
}

/**
 * Daily activity
 */
function getDailyActivity(){
    var now = new Date();
    var today = new Date(now.setHours(0, 0, 0, 0));
    var tomorrow = new Date(today.getTime() + (24 * 60 * 60 * 1000));

    Message.find({"time": {"$gte": today, "$lt": tomorrow}}, function (err, messages) {
        if (err) {
            res.status(404);
            res.send('Messages not found!');
        }
        console.log(messages.length);
        var work = 0;
        for(var i=0; i<messages.length-1; i++){
            var currentMessage = new Message(messages[i]);
            var nextMessage = new Message(messages[i+1]);
            if(currentMessage.data != 0 && nextMessage.data != "0"){
                work += (nextMessage.time - currentMessage.time);
            }
        }

        var activity = {
            "work": work
        };
        console.log(activity);
        // return a view with data
        res.render('pages/home', {
            messages: messages,
            activity: activity
        });
    });
}

/**
 * Seed the database
 */
function seedMessages(req, res) {
    // create some messages
    const messages = [
        {device: 'AD931E', time: '1496218985020', data: '313030'},
        {device: 'AD931E', time: '1496156315783', data: '30'}
    ];

    // use the Message model to insert/save
    Message.remove({}, function () {
        for (message of messages) {
            var newMessage = new Message(message);
            saveMessageInDB(newMessage, res);
        }
        if (res.statusCode == 200)
            console.log('Database seeded!');
        else
            console.log('Error occurred!');
        res.redirect('/messages');
    });
}

/**
 * Process the creation from Sigfox Backend
 */
function processCreate(req, res) {
    // validate information
    req.checkBody('device', 'Device is required.').notEmpty();
    req.checkBody('time', 'Time is required.').notEmpty();
    req.checkBody('data', 'Data is required.').notEmpty();

    // if there are errors, redirect and save errors to flash
    const errors = req.validationErrors();
    if (errors) {
        return res.send('Data format not respected');
    }

    console.log('Adding in DB: ' + JSON.stringify(req.body));
    // create a new message
    const newMessage = new Message({
        device: req.body.device,
        time: req.body.time * 1000, // Sigfox Backend returns Epoch Time in seconds, we have to * 1000 to convert to millis
        data: decodeURIComponent(escape(hexToASCII(req.body.data))) // decode the HEX message (12 bytes)
    });

    saveMessageInDB(newMessage, res);
}




// Utils
function hexToASCII(hex) {
    var str = '';
    for (var i = 0; i < hex.length; i += 2) str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

function saveMessageInDB(newMessage, res){
    // save message
    newMessage.save(function (err) {
        if (err){
            throw err;
            console.error('Could not add messagein DB');
            res.sendStatus(404);
        } else {
            console.log('Successfully added new message in DB');
            io.sockets.emit('newMessage', newMessage);
            if(res)
                res.sendStatus(201);
        }
    });
}