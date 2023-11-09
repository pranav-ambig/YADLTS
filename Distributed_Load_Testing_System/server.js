let http = require('http')

console.log('Starting server')

let requests_served = 0
let httpserver = http.createServer((req, res)=>{

    requests_served += 1
    console.log(requests_served)
    
    if (requests_served == 1000){
        console.log('Server limit reached, exiting...')
        httpserver.close()
    }
    res.write('Hello')
    res.end()
}).listen(5052)
