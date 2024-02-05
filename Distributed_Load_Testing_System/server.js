let http = require('http')

console.log('Starting server')

let requests_served = 0
let max_requests = 4
let active_requests = 0
let httpserver = http.createServer((req, res)=>{
    requests_served += 1
    active_requests += 1
    if (active_requests == max_requests){
        httpserver.closeAllConnections()
    }
    console.log(requests_served)
    
    if (requests_served == 5000){
        console.log('Server limit reached, exiting...')
        httpserver.close()
    }
    res.write('Hello')
    res.end()
    active_requests -= 1
}).listen(5052)

