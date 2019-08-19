const express = require('express')
var cors = require('cors')
var fs = require("fs");
//var cookieParser = require('cookie-parser');
var app = express()
const port = 3000
var mysql = require('mysql');
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cors())
//app.use(cookieParser)

app.get('/', (req, res) => res.send('Hello World!'))

function findIndex (list, search){
    for(var i=0;i<list.length;i++){
        one = list[i];
        two = search;
        if(JSON.stringify(one) === JSON.stringify(two)){
            var index = i;
        }
        delete one;
        delete two;
    }
    return index;
}


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

app.post('/add_register_request', function(req,res){
    console.log("ADDDD")
    var request = req.body
    console.table(request)
    if(request['category']=='student'){
        var sql = `INSERT INTO students VALUES ('${request['name']}', '${request['username']}', '${request['class']}', '${request['section']}', ${request['admission_no']}, '${request['club']}', '${request['vpa']}');`
    }else if (request['category']=='teacher'){
        var subjects = request['subjects'];
        //subjects = Array(subjects)
        var id = request['teacher_id']
        var sql = `INSERT INTO teachers VALUES ('${request['name']}', '${request['username']}', '${request['class_teacher']}', ${request['teacher_id']})`
        var con = mysql.createConnection({
            host: "localhost",
            port: "3306",
            database: "wizlearn",
            user: "root",
            password: "pokemon2345"
        })
        con.connect();
        console.log("SUBJECTS IS")
        console.log(subjects)
        for (var x=0;x<subjects.length;x++){
            console.log(`%c${x}`,"color:red;")
            console.log("X is ")
            console.log(subjects[x])
            y = subjects[x].split(" ")
            console.log(y)
            temp = y[0].match(/[a-zA-Z]+|[0-9]+(?:\.[0-9]+|)/g);
            console.log(temp)
            var sqlt = `INSERT INTO subjects (subject, grade, section, teacher_id) VALUES ('${y[1]}', '${temp[0]}', '${temp[1]}', ${id})`
            console.log(sqlt)
            delete y;
            delete temp;
            con.query(sqlt)
            con.commit()
        }
        con.end()
    }else{console.log('ERROR')}
    console.log(sql)
    var connection = mysql.createConnection({
        host: "localhost",
        port: "3306",
        database: "wizlearn",
        user: "root",
        password: "pokemon2345"
    });
    connection.connect();
    connection.query(sql)
    connection.end();
    var file = JSON.parse(fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json'))
    var index = findIndex(file,request);
    file.splice(index, 1)
    fs.writeFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json', JSON.stringify(file))
})

app.post('/delete_register_request', function(req,res){
    var request = req.body
    var file = JSON.parse(fs.readFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json'))
    var index = findIndex(file,request);
    file.splice(index, 1)
    fs.writeFileSync('C:/Users/Anirudh/Desktop/Hackathon/app/databases/add_studentRequests.json', JSON.stringify(file))   
})

app.post('/delete_doubt', function(req,res){
    var request = req.body;
    console.log("IN DELETE DOUBT")
    var con = mysql.createConnection({
        host: "localhost",
        port: "3306",
        database: "wizlearn",
        user: "root",
        password: "pokemon2345"
    })
    con.connect();
    console.log("CONNECTION CONNECTED")
    var sql = `DELETE FROM doubts WHERE id = ${JSON.parse(request[0])}`
    console.log(sql)
    con.query(sql)
    con.commit()
    con.end()
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))