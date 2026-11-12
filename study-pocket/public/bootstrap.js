// Surface initialization failures instead of leaving apparently clickable, inactive controls.
function startupError(message) {
  const target = document.querySelector('#message');
  if (!target) return;
  target.hidden = false; target.className = 'error';
  target.textContent = '앱을 시작하지 못했습니다. ' + message + ' 새로고침하거나 Chrome·Edge·Safari의 일반 탭에서 다시 열어주세요. 저장한 PDF는 삭제하지 마세요.';
}
window.addEventListener('error', event => startupError(event.message || '필요한 파일을 불러오지 못했습니다.'));
window.addEventListener('unhandledrejection', event => startupError(event.reason?.message || '기기 저장소 또는 앱 초기화를 확인하세요.'));
import('/app.js?v=server-session-1').then(() => {
  const target=document.querySelector('#message');
  if(target?.dataset.starting==='true'){target.hidden=true;delete target.dataset.starting;}
}).catch(error => startupError(error.message));
