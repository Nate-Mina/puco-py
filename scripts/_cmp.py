
const { PNG } = require('pngjs');
const fs = require('fs');

function load(file){
  return PNG.sync.read(fs.readFileSync(file));
}
function analyze(file){
  const p = load(file);
  let rs=0,gs=0,bs=0,n=0;
  // sample every 7th pixel
  for(let y=0;y<p.height;y+=4){
    for(let x=0;x<p.width;x+=4){
      const i=(p.width*y+x)<<2;
      rs+=p.data[i]; gs+=p.data[i+1]; bs+=p.data[i+2]; n++;
    }
  }
  return {w:p.width,h:p.height,r:(rs/n/255).toFixed(3),g:(gs/n/255).toFixed(3),b:(bs/n/255).toFixed(3)};
}
const real=analyze('cmp_real.png');
const live=analyze('cmp_live.png');
console.log('REAL', JSON.stringify(real));
console.log('LIVE', JSON.stringify(live));
// crude similarity: compare avg RGB distance
const dr=Math.abs(real.r-live.r), dg=Math.abs(real.g-live.g), db=Math.abs(real.b-live.b);
console.log('RGB_DELTA', dr.toFixed(3), dg.toFixed(3), db.toFixed(3));
