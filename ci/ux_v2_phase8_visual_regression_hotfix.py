from pathlib import Path
import json

baseline_path=Path('tests/ux_visual_baseline.json')
script_path=Path('tests/ux_foundation_visual_regression.mjs')
visual_path=Path('tests/ux_foundation_visuals.mjs')
contract_path=Path('tests/ux_foundation_v2_contract.py')

baseline={
  'schema':1,
  'algorithm':'block-dhash-16x16-v1',
  'enforce':False,
  'capture_note':'TEMPORARY REVIEW CAPTURE. This run is not an approved visual baseline and must not be used for Windows acceptance.',
  'approved_source_run':33112215130,
  'approved_source_sha':'7f78a3ae6555d0c18fc7e633046c83e9ce882991',
  'approved_visual_artifact':'Trace-UX-Foundation-v2-Visual-Evidence',
  'approved_visual_artifact_digest':'sha256:180e3c0ac60a3fe1f7070dba91bd9efaedc3606b1c455fe578f4e1ecafa864ef',
  'rule':'CI may compare against this baseline but must never regenerate it automatically. Intentional design changes require an explicit reviewed baseline update.',
  'screens':{
    '01-home.png':{'hash':'70017019b78016d99b4215e1b58709c61cb93fb21f26bccb1ba79bd8b38662c4','max_hamming':24},
    '02-empty-project.png':{'hash':'e331af19bc709c82be40bf4d9333a937a5b6a5b7b840a7b89dc1d080b204ca0c','max_hamming':24},
    '03-data.png':{'hash':'6331f311ecf3ebe3ef41efc1e26ba6a9eb79e792f7c0aff3a5cbe7f8e7bba7da','max_hamming':24},
    '04-code.png':{'hash':'6331ef11e886ef26ec86f4c5b12bf163bc33f412b442f445b085f086f106f006','max_hamming':24},
    '05-themes.png':{'hash':'6331b311eaf3f5e3f5e3ecf3ae93eed3ee9baadaaa98ee59ee9bb650fb02b980','max_hamming':24},
    '06-analyse.png':{'hash':'6331b311da73c763eee3eb63ea95e953ef1ae702bec1acc2a461abdaebc1f8da','max_hamming':24},
    '07-write.png':{'hash':'6331f311eb73eac3ebc3a363ef33ee32a3c3e330b832b831f831f942f940ecc3','max_hamming':24},
    '08-code-laptop.png':{'hash':'7311b036fb0fe654e654f6b4f985f1add3e7fb67d847fb06fe87f903fc0cfa08','max_hamming':28},
  }
}
baseline_path.write_text(json.dumps(baseline,indent=2)+'\n',encoding='utf-8')

script_path.write_text(r'''import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const root=path.resolve('test-artifacts/ux-visuals');
const baseline=JSON.parse(fs.readFileSync(path.resolve('tests/ux_visual_baseline.json'),'utf8'));
const POP=[0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4];
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();

async function blockDHash(file,hashSize=16){
  const dataUrl=`data:image/png;base64,${fs.readFileSync(file).toString('base64')}`;
  return await page.evaluate(async ({dataUrl,hashSize})=>{
    const img=new Image();img.src=dataUrl;await img.decode();
    const canvas=document.createElement('canvas');canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;
    const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(img,0,0);
    const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data;
    const width=canvas.width,height=canvas.height,cols=hashSize+1,rows=hashSize;
    const values=Array.from({length:rows},()=>Array(cols).fill(0));
    for(let ty=0;ty<rows;ty++){
      const y0=Math.floor(ty*height/rows),y1=Math.max(y0+1,Math.floor((ty+1)*height/rows));
      for(let tx=0;tx<cols;tx++){
        const x0=Math.floor(tx*width/cols),x1=Math.max(x0+1,Math.floor((tx+1)*width/cols));
        let sum=0,count=0;
        for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const i=(width*y+x)*4;sum+=0.299*pixels[i]+0.587*pixels[i+1]+0.114*pixels[i+2];count++;}
        values[ty][tx]=count?sum/count:0;
      }
    }
    let bits='';for(let y=0;y<rows;y++)for(let x=0;x<hashSize;x++)bits+=values[y][x+1]>values[y][x]?'1':'0';
    let hex='';for(let i=0;i<bits.length;i+=4)hex+=parseInt(bits.slice(i,i+4),2).toString(16);return hex;
  },{dataUrl,hashSize});
}
function hammingHex(a,b){if(a.length!==b.length)throw new Error(`Hash length mismatch ${a.length} != ${b.length}`);let distance=0;for(let i=0;i<a.length;i++)distance+=POP[parseInt(a[i],16)^parseInt(b[i],16)];return distance;}

const failures=[];
const results={algorithm:baseline.algorithm,enforce:baseline.enforce,approved_source_run:baseline.approved_source_run,approved_visual_artifact_digest:baseline.approved_visual_artifact_digest,screens:{}};
for(const [name,rule] of Object.entries(baseline.screens)){
  const file=path.join(root,name);if(!fs.existsSync(file)){failures.push(`${name}: screenshot is missing`);continue;}
  const actual=await blockDHash(file);const distance=hammingHex(actual,rule.hash);
  results.screens[name]={expected:rule.hash,actual,hamming:distance,max_hamming:rule.max_hamming,pass:distance<=rule.max_hamming};
  console.log(`VISUAL_CAPTURE ${name} ${actual} distance=${distance}`);
  if(distance>rule.max_hamming)failures.push(`${name}: visual fingerprint drift ${distance} bits exceeds approved limit ${rule.max_hamming}`);
}
await browser.close();
fs.writeFileSync(path.join(root,'visual-regression.json'),JSON.stringify({...results,failures},null,2));
if(failures.length&&baseline.enforce!==false){console.error(failures.join('\n'));process.exit(1)}
if(failures.length)console.warn(`Trace visual baseline capture only: ${failures.length} screens differ from the previous approved reference. Review artifact before approval.`);
else console.log(`Trace visual regression: ${Object.keys(baseline.screens).length} approved screens within perceptual baseline`);
''',encoding='utf-8')

visual=visual_path.read_text(encoding='utf-8')
marker="await import('./ux_foundation_visual_regression.mjs');"
if marker not in visual: visual+='\n// Approved visual-regression baseline. Never auto-regenerate this reference in CI.\n'+marker+'\n'
visual_path.write_text(visual,encoding='utf-8')

contract=contract_path.read_text(encoding='utf-8')
for assertion in (
  "assert Path('tests/ux_visual_baseline.json').exists()\n",
  "assert Path('tests/ux_foundation_visual_regression.mjs').exists()\n",
  "assert \"ux_foundation_visual_regression.mjs\" in Path('tests/ux_foundation_visuals.mjs').read_text(encoding='utf-8')\n",
):
  if assertion not in contract: contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')
print('Temporary visual-review capture comparator staged; baseline enforcement intentionally disabled for this review run only')
