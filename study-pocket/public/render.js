// Shared production renderer. The optional factory is used for native-canvas tests.
export async function renderPDFPage(page,dpi=155,crop=null,createCanvas=()=>document.createElement('canvas'),annotationMode=1){
  const base=page.getViewport({scale:1});
  const side=crop?Math.max(base.width*crop.width,base.height*crop.height):Math.max(base.width,base.height);
  const scale=Math.min(dpi/72,(crop?1800:2400)/side),viewport=page.getViewport({scale});
  const canvas=createCanvas(),left=crop?crop.x*viewport.width:0,top=crop?crop.y*viewport.height:0;
  canvas.width=Math.ceil(crop?crop.width*viewport.width:viewport.width);canvas.height=Math.ceil(crop?crop.height*viewport.height:viewport.height);
  const ctx=canvas.getContext('2d',{alpha:false});ctx.fillStyle='#ffffff';ctx.fillRect(0,0,canvas.width,canvas.height);
  await page.render({canvasContext:ctx,viewport,transform:crop?[1,0,0,1,-left,-top]:undefined,annotationMode}).promise;
  const text=crop?'':(await page.getTextContent()).items.map(i=>i.str||'').join(' ').slice(0,6500);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.87));page.cleanup();if(!blob)throw new Error('페이지 이미지 변환에 실패했습니다.');
  return{canvas,text,blob};
}
