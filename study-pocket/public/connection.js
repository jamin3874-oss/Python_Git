// Only a signed HttpOnly cookie is remembered. API keys and access codes stay out of storage.
export function createConnection(fetcher = globalThis.fetch) {
  let state = {server_configured: false, authenticated: false}, pending;
  async function request(options = {}) {
    const response = await fetcher('/api/ai', {
      credentials: 'same-origin', cache: 'no-store', signal: AbortSignal.timeout(12000), ...options
    });
    if (options.method !== 'POST' && response.status === 405) return {server_configured: false, authenticated: false};
    let body;
    try { body = await response.json(); } catch { throw new Error('AI 연결 정보를 읽지 못했습니다. 앱을 새로고침하세요.'); }
    if (!response.ok) throw new Error(body.error || 'AI 서버 연결을 확인하세요.');
    return body;
  }
  function refresh() {
    return pending ||= request().then(result => {
      state = {server_configured: result.server_configured === true, authenticated: result.authenticated === true};
      return state;
    }).finally(() => { pending = null; });
  }
  return {
    get state() { return {...state}; }, refresh,
    async login(access_code) {
      if (pending) await pending.catch(()=>{});
      await request({method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'login',access_code})});
      if (pending) await pending.catch(()=>{});
      const status = await refresh();
      if (!status.authenticated) throw new Error('로그인 쿠키를 저장하지 못했습니다. 일반 브라우저에서 쿠키 설정을 확인하세요.');
      return status;
    },
    async logout() {
      if (pending) await pending.catch(()=>{});
      await request({method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'logout'})});
      state = {...state, authenticated:false}; return {...state};
    }
  };
}
