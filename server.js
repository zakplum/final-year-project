const express = require('express');
var ejs = require('ejs')
const app = express();
const port = 8000; 

app.use(express.static('public'));


//CSS
app.use(express.static(__dirname + '/public'));

//Express commands
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', ejs.renderFile);

// Start the web app listening
app.listen(port, () => console.log(`Listening on port ${port}!`))