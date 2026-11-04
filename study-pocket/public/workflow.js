import {MAX_IMAGE_BYTES,pagePlan,planMerge,makeReadPrompt,makeMergePrompt,runSignature} from './core.js';

// One automatic workflow; adapters provide PDF rendering, API and durable storage.
export async function runNotebook(project, {model,render,send,save,onProgress=()=>{},shouldStop=()=>false}) {
  const signature=runSignature(project,model,project.quality||155);
  if(!project.run||project.run.signature!==signature){project.run={signature,pages:pagePlan(project.files),cursor:0,nodes:[],phase:'read',level:0,mergeIndex:0,next:[]};await save();}
  const run=project.run;
  if(!run.pages.length)throw new Error('읽을 PDF 페이지가 없습니다.');
  while(!shouldStop()&&run.phase==='read'&&run.cursor<run.pages.length){
    onProgress(run);let pages=[],images=[],bytes=0;
    for(let index=run.cursor;index<run.pages.length&&pages.length<4;index++){
      if(shouldStop())break;const ref=run.pages[index];onProgress(run,ref);
      const item=await render(ref);
      if(item.bytes>MAX_IMAGE_BYTES)throw new Error(`${ref.fileName} ${ref.page}쪽 이미지가 너무 큽니다. 기본 선명도를 선택하세요.`);
      if(images.length&&bytes+item.bytes>MAX_IMAGE_BYTES)break;
      bytes+=item.bytes;pages.push({...ref,text:item.text});images.push(item.block);
    }
    if(shouldStop()||!pages.length)break;
    const final=run.cursor===0&&pages.length===run.pages.length;
    const result=await send([{role:'user',content:[{type:'text',text:makeReadPrompt(pages,project.instructions,final,project.crops)},...images]}],final?7000:4500);
    run.nodes.push({text:result.text,pages:pages.length,model:result.model});run.cursor+=pages.length;run.phase=run.cursor===run.pages.length?'merge':'read';await save();onProgress(run);
  }
  while(!shouldStop()&&run.phase==='merge'){
    if(run.nodes.length===1){const result=run.nodes[0];project.note=result.text;project.noteModel=result.model;project.noteSignature=signature;project.noteAt=Date.now();project.run=null;await save();return{completed:true};}
    const groups=planMerge(run.nodes);run.level=run.level||1;onProgress(run);
    while(!shouldStop()&&run.mergeIndex<groups.length){
      const group=groups[run.mergeIndex];let node=group[0];
      if(group.length>1){const result=await send([{role:'user',content:makeMergePrompt(group,project.instructions,groups.length===1)}],7000);node={text:result.text,pages:group.reduce((n,x)=>n+x.pages,0),model:result.model};}
      run.next.push(node);run.mergeIndex++;await save();
    }
    if(run.mergeIndex===groups.length){run.nodes=run.next;run.next=[];run.mergeIndex=0;run.level++;await save();}
  }
  return{completed:false};
}
