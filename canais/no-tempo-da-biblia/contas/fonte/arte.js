const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [m,w,h,sw,out] of [['avatar',800,800,0,'foto-perfil-800.png'],['banner',2560,1440,1546,'banner-youtube-2560x1440.png'],['banner',1600,900,1400,'banner-x-capa-1600x900.png']]){
const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(`file://${__dirname}/arte.html?m=${m}&w=${w}&h=${h}&sw=${sw}`);await p.waitForTimeout(600);await p.screenshot({path:out});await p.close();}
await b.close();})();
