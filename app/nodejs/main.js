const express = require('express')
var cors = require('cors')
var fs = require("fs");
//var cookieParser = require('cookie-parser');
var app = express()
const port = 3000
var mysql = require("mssql");
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cors())
//app.use(cookieParser)

app.get('/', (req, res) => res.send('Hello World!'))

app.get('/teacher_requests', function(req,res){
    var msg = req.query.msg
    msg = JSON.parse(msg)
    var data = JSON.parse(fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json'))
    data.push(msg)
    fs.writeFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json', JSON.stringify(data));
})

app.get('/student_requests', function(req,res){
    var msg = req.query.msg
    msg = JSON.parse(msg)
    var data = JSON.parse(fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json'))
    data.push(msg)
    fs.writeFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json', JSON.stringify(data));
})

app.get('/which_login', function(req,res){
    var admin_status = fs.readFileSync("admin.json");
    res.send(admin_status)
    console.log("WHICH LOGIN")
})

app.get('/retrieve_register_requests', function(req,res){
    var requests = fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json')
    res.send(requests)
    console.log("RETRIEVE REQUESTS")
})

app.get('/add_register_request', function(req,res){
    console.log("ADDDD")
    var request = req.query.request
    console.log(`SQL is` + JSON.stringify(sql.name))
    var config = {
        host: "localhost",
        port: "3306",
        database: "wizlearn",
        user: "root",
        password: "pokemon2345"
    };
    mysql.connect(config, function (err) {
        var query = new mysql.Request()
        query.query(sql, function(err,recordset){console.log(sql)})
    })
    mysql.close()
})

app.get('/delete_register_request', function(req,res){
    var request = req.query.request;
    var requests = JSON.parse(fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json'))
    console.log(request,requests)   
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))