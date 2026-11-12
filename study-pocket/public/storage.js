let connection;
export async function db() {
  if (!connection) connection = new Promise((resolve,reject) => {
    const request = indexedDB.open('study-pocket-v1',1);
    let settled=false;
    const fail=message=>{if(settled)return;settled=true;clearTimeout(timer);reject(new Error(message));};
    const timer=setTimeout(()=>fail('기기 저장소 응답이 없습니다. 이 앱의 다른 탭을 닫고 일반 브라우저에서 다시 열어주세요.'),15000);
    request.onupgradeneeded=()=>{const d=request.result; d.createObjectStore('projects',{keyPath:'id'});d.createObjectStore('files',{keyPath:'id'});d.createObjectStore('preferences',{keyPath:'id'});};
    request.onsuccess=()=>{if(settled){request.result.close();return;}settled=true;clearTimeout(timer);const opened=request.result;opened.onversionchange=()=>{opened.close();connection=undefined;};resolve(opened);};request.onerror=()=>fail('기기 저장소를 열지 못했습니다. 일반 브라우저에서 저장 공간을 확인하세요.');
    request.onblocked=()=>fail('다른 앱 탭이 기기 저장소를 사용하고 있습니다. 이 앱의 다른 탭을 닫고 다시 열어주세요.');
  }).catch(error=>{connection=undefined;throw error;});
  return connection;
}
export async function transaction(stores, callback) {
  const d = await db(); return new Promise((resolve,reject)=> {
    const tx=d.transaction(stores,'readwrite');let timedOut=false;const timer=setTimeout(()=>{timedOut=true;try{tx.abort();}catch{}reject(new Error('PDF 저장 응답이 지연되어 중단했습니다. 다른 앱 탭을 닫고 저장 공간을 확인한 뒤 다시 올려주세요.'));},90000);
    tx.oncomplete=()=>{clearTimeout(timer);resolve();};tx.onerror=()=>{clearTimeout(timer);reject(new Error(tx.error?.name==='QuotaExceededError'?'기기 저장 공간이 부족합니다. 다른 자료를 정리하거나 용량이 작은 PDF로 시도하세요.':'기기 저장에 실패했습니다. 일반 브라우저에서 저장 공간을 확인하세요. 기존 자료는 유지됩니다.'));};tx.onabort=()=>{clearTimeout(timer);reject(new Error(timedOut?'PDF 저장 시간이 초과되었습니다. 저장 공간과 다른 앱 탭을 확인하세요.':'기기 저장이 중단되었습니다. 기존 자료는 유지됩니다.'));};
    try {callback(Object.fromEntries(stores.map(name=>[name,tx.objectStore(name)])));} catch(e){tx.abort();reject(e);}
  });
}
export async function get(store, id) {const d=await db();return new Promise((resolve,reject)=>{const r=d.transaction(store).objectStore(store).get(id);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});}
export async function listProjects() {const d=await db();return new Promise((resolve,reject)=>{const r=d.transaction('projects').objectStore('projects').getAll();r.onsuccess=()=>resolve(r.result.sort((a,b)=>b.updatedAt-a.updatedAt));r.onerror=()=>reject(r.error);});}
export function saveProject(p) {p.updatedAt=Date.now();return transaction(['projects'], s=>s.projects.put(p));}
export async function saveStudy(project, expected) {
  const d=await db();return new Promise((resolve,reject)=>{
    const tx=d.transaction('projects','readwrite'),s=tx.objectStore('projects');let reason;
    tx.oncomplete=()=>resolve();tx.onerror=()=>reject(new Error('읽기 결과 저장에 실패했습니다. 저장 공간을 확인하세요.'));tx.onabort=()=>reject(reason||new Error('저장이 중단되었습니다.'));
    const request=s.get(project.id);request.onsuccess=()=>{const latest=request.result;
      if(!latest||JSON.stringify([latest.revision,latest.instructions||'',Number(latest.quality||155)])!==expected){reason=new Error('다른 창에서 자료 또는 요청이 변경되었습니다. 변경된 자료를 다시 열어 진행하세요.');tx.abort();return;}
      s.put({...latest,files:project.files,run:project.run||null,note:project.note,noteModel:project.noteModel,noteSignature:project.noteSignature,noteAt:project.noteAt,updatedAt:Date.now()});
    };
  });
}
export function insertProject(project, files) {return transaction(['projects','files'],s=>{s.projects.put(project);for(const f of files)s.files.put(f);});}
export function removeProject(project) {return transaction(['projects','files'],s=>{s.projects.delete(project.id);for(const f of project.files)s.files.delete(f.id);});}
export function removeFile(project, fileId) {return transaction(['projects','files'],s=>{s.projects.put(project);s.files.delete(fileId);});}
