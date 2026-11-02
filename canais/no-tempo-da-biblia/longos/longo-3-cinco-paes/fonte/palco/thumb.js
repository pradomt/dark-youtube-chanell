const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+__dirname+'/thumb.html');await p.waitForTimeout(500);await p.screenshot({path:'/tmp/w/l3/thumbnail.png'});await b.close();})();
