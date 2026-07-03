const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname;
http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]);
  if(p==='/')p='/index.html';
  const fp=path.join(root,p);
  fs.readFile(fp,(e,d)=>{
    if(e){res.writeHead(404);res.end('nf');return;}
    const ext=path.extname(fp);
    const ct=ext==='.html'?'text/html; charset=utf-8':ext==='.css'?'text/css':'text/plain';
    res.writeHead(200,{'Content-Type':ct});res.end(d);
  });
}).listen(8777,()=>console.log('up on 8777'));
