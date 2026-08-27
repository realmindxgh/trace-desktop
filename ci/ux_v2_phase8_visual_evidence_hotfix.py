from pathlib import Path

p=Path('tests/ux_foundation_visuals.mjs')
p.write_text(r'''import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const base=process.env.TRACE_TEST_URL||'http://127.0.0.1:4173';
const out=path.resolve('test-artifacts/ux-visuals');
fs.mkdirSync(out,{recursive:true});

const refs=[
  {id:'r1',codeId:'c1',sourceId:'s1',coderId:'u1',segmentId:'seg1',text:'Access to support was difficult at first',participantId:'p1'},
  {id:'r2',codeId:'c2',sourceId:'s1',coderId:'u1',segmentId:'seg1',text:'peer help changed the experience',participantId:'p1'},
];
const fixture={
  project:{id:'visual',title:'Community support interview study',methodology:'Reflexive Thematic Analysis',codingMode:'manual',researchQuestions:['How do participants describe access to support?'],researchQuestionRecords:[{id:'rq1',position:0,text:'How do participants describe access to support?'}]},
  activeSection:'Data',dataContext:'sources',activeParticipant:'P01',activeSourceId:'s1',openSourceTabs:['s1'],
  participants:[{id:'P01',internalId:'p1',role:'Participant'}],
  transcript:[
    {speaker:'P01',time:'00:00',text:'Access to support was difficult at first, but peer help changed the experience.',segmentId:'seg1',sourceId:'s1',startChar:0,endChar:75},
    {speaker:'P01',time:'00:18',text:'Once I knew who to ask, the process felt more manageable.',segmentId:'seg2',sourceId:'s1',startChar:76,endChar:133},
  ],
  importedSources:[{id:'s1',name:'Interview 01.txt',kind:'text',participantId:'p1',segments:[{id:'seg1',source_id:'s1',position:0,text:'Access to support was difficult at first, but peer help changed the experience.',start_char:0,end_char:75},{id:'seg2',source_id:'s1',position:1,text:'Once I knew who to ask, the process felt more manageable.',start_char:76,end_char:133}],codings:[...refs]}],
  codes:[{id:'c1',name:'Access barriers',description:'Difficulties obtaining needed support',color:'#4466aa'},{id:'c2',name:'Peer support',description:'Support from peers',color:'#669977'}],
  coders:[{id:'u1',name:'Researcher'}],activeCoderId:'u1',
  allCodingRefs:[...refs],codingRefs:[...refs],
  themes:[{id:'t1',name:'Pathways to support',description:'Access changes through relational support.',codeIds:['c1','c2'],source:'Researcher created'}],
  variables:[],variableValues:[],
  findingsSections:[{id:'f1',targetType:'theme',targetId:'t1',title:'Pathways to support',body:'Participants described initial access barriers, with peer support changing how support was experienced.',updatedAt:1700000000000}],
  findingsEvidence:[],memos:[{id:'m1',name:'Access memo',text:'Peer support changes the access story.'}],annotations:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},analysisTab:'matrix',writeTarget:{type:'theme',id:'t1'},savedAt:1700000000000,
};

const browser=await chromium.launch({headless:true});
const failures=[];
async function snap(name,setup,arg,viewport={width:1600,height:900},deviceScaleFactor=1){
  const ctx=await browser.newContext({viewport,deviceScaleFactor});
  if(setup)await ctx.addInitScript(setup,arg);
  const page=await ctx.newPage();
  await page.goto(base,{waitUntil:'networkidle'});
  await page.evaluate(()=>{document.documentElement.style.caretColor='transparent';});
  const meta=await page.evaluate(()=>{
    const visible=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
    const textNodes=[...document.querySelectorAll('button,input,textarea,label,p,small,b,span,h1,h2,h3,h4,summary')].filter(visible);
    const sizes=textNodes.map(e=>parseFloat(getComputedStyle(e).fontSize)||0).filter(Boolean);
    const horizontalOverflow=document.documentElement.scrollWidth-document.documentElement.clientWidth;
    return {
      title:document.querySelector('h1')?.textContent?.trim()||'',
      horizontalOverflow,
      focusables:[...document.querySelectorAll('button,input,textarea,[tabindex="0"]')].filter(visible).length,
      minimumVisibleFontPx:sizes.length?Math.min(...sizes):0,
      codingStripes:document.querySelectorAll('.coding-stripes i').length,
      inspectorVisible:[...document.querySelectorAll('.inspector')].some(visible),
      contextPaneVisible:[...document.querySelectorAll('.context-pane')].some(visible),
    };
  });
  if(meta.horizontalOverflow>1)failures.push(`${name}: page has ${meta.horizontalOverflow}px horizontal overflow`);
  if(meta.minimumVisibleFontPx>0&&meta.minimumVisibleFontPx<12)failures.push(`${name}: visible UI text fell below 12px (${meta.minimumVisibleFontPx}px)`);
  fs.writeFileSync(path.join(out,`${name}.json`),JSON.stringify({viewport,deviceScaleFactor,...meta},null,2));
  await page.screenshot({path:path.join(out,`${name}.png`),fullPage:false});
  await ctx.close();
  return meta;
}

await snap('01-home');
await snap('02-empty-project',()=>localStorage.setItem('trace-v010-state',JSON.stringify({project:{id:'p',title:'New qualitative study',methodology:'',codingMode:'manual',researchQuestions:[],researchQuestionRecords:[]},activeSection:'Overview',participants:[],importedSources:[],codes:[],themes:[],allCodingRefs:[],codingRefs:[],memos:[],annotations:[],sourceProperties:[],sourceCollections:[],importQueue:[],backups:[],audit:[],mediaSelections:[],mediaCodings:[],mediaPayloads:{},savedAt:1700000000000})));
const screens={};
for(const [ix,section] of ['Data','Code','Themes','Analyse','Write'].entries()){
  screens[section]=await snap(`${String(ix+3).padStart(2,'0')}-${section.toLowerCase()}`,({fixture,section})=>{const x=JSON.parse(JSON.stringify(fixture));x.activeSection=section;localStorage.setItem('trace-v010-state',JSON.stringify(x));},{fixture,section});
}
if((screens.Code?.codingStripes||0)<2)failures.push('04-code: populated Code evidence did not visibly show both coding markers');
for(const section of ['Data','Themes','Analyse','Write']){
  if(!screens[section]?.contextPaneVisible)failures.push(`${section}: contextual pane is not visible in deterministic evidence`);
  if(!screens[section]?.inspectorVisible)failures.push(`${section}: inspector is not visible in deterministic evidence`);
}

// A second realistic laptop-size capture protects the shell against screenshot-only workstation success.
await snap('08-code-laptop',({fixture})=>{const x=JSON.parse(JSON.stringify(fixture));x.activeSection='Code';localStorage.setItem('trace-v010-state',JSON.stringify(x));},{fixture},{width:1366,height:768},1.25);

await browser.close();
const required=['01-home','02-empty-project','03-data','04-code','05-themes','06-analyse','07-write','08-code-laptop'];
for(const name of required){
  if(!fs.existsSync(path.join(out,`${name}.png`)))failures.push(`missing visual evidence ${name}.png`);
  if(!fs.existsSync(path.join(out,`${name}.json`)))failures.push(`missing visual evidence ${name}.json`);
}
if(failures.length){console.error(failures.join('\n'));process.exit(1)}
console.log(`Trace UX visual evidence: ${required.length} deterministic screens captured and checked`);
''',encoding='utf-8')
print('Deterministic UX visual-evidence browser script staged with populated coding and laptop evidence')
