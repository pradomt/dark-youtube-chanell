const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:800},deviceScaleFactor:2});
for(const [m,c] of [['h','claro'],['h','escuro'],['icone','claro'],['icone','escuro']]){await p.goto(`file://${__dirname}/logo.html?m=${m}&c=${c}`);await p.waitForTimeout(400);
await p.locator('.row').screenshot({path:`logo-${m==='h'?'horizontal':'icone'}-${c}.png`,omitBackground:true});}
await b.close();})();
