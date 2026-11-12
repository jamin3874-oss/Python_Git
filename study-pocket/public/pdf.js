import * as pdfjs from '/vendor/pdfjs/pdf.min.mjs';
import {get} from './storage.js';
import {renderPDFPage} from './render.js';
pdfjs.GlobalWorkerOptions.workerSrc='/vendor/pdfjs/pdf.worker.min.mjs';
let cachedId, cachedDocument;
export async function openPDF(fileId) {
  if (fileId===cachedId && cachedDocument) return cachedDocument;
  if(cachedDocument)await cachedDocument.destroy();cachedDocument=null;cachedId=null;
  const record=await get('files',fileId);if(!record)throw new Error('원본 PDF를 찾지 못했습니다. 자료를 다시 선택하세요.');
  const doc=await pdfjs.getDocument({data:new Uint8Array(await record.blob.arrayBuffer()),cMapUrl:'/vendor/pdfjs/cmaps/',cMapPacked:true,standardFontDataUrl:'/vendor/pdfjs/standard_fonts/',wasmUrl:'/vendor/pdfjs/wasm/',isEvalSupported:false}).promise;
  cachedId=fileId;cachedDocument=doc;return doc;
}
export async function closePDF(){if(cachedDocument)await cachedDocument.destroy();cachedDocument=null;cachedId=null;}
export async function renderPage(fileId, pageNumber, dpi=155, crop=null) {
  const doc=await openPDF(fileId);if(pageNumber<1||pageNumber>doc.numPages)throw new Error(`페이지는 1~${doc.numPages}쪽 중에서 선택하세요.`);
  return renderPDFPage(await doc.getPage(pageNumber),dpi,crop,undefined,pdfjs.AnnotationMode.ENABLE);
}
export function base64(blob){return new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(String(r.result).split(',')[1]);r.onerror=()=>reject(new Error('이미지를 읽지 못했습니다.'));r.readAsDataURL(blob);});}
