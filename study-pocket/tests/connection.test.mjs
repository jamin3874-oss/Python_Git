import test from 'node:test';
import assert from 'node:assert/strict';
import {createConnection} from '../public/connection.js';
const ok=body=>new Response(JSON.stringify(body),{headers:{'Content-Type':'application/json'}});
test('returning visitor uses a server cookie without entering or sending an API key',async()=>{
  const calls=[];const client=createConnection(async(url,options)=>{calls.push({url,options});return ok({server_configured:true,authenticated:true});});
  assert.equal((await client.refresh()).authenticated,true);
  assert.equal(calls[0].options.credentials,'same-origin');assert.equal(calls[0].options.cache,'no-store');
  assert.equal(calls[0].options.body,undefined);assert.equal(calls[0].options.headers,undefined);
});
test('login verifies that the browser actually retained the signed cookie',async()=>{
  const calls=[];const client=createConnection(async(_url,options)=>{calls.push(options);return ok(options.method==='POST'?{authenticated:true}:{server_configured:true,authenticated:false});});
  await assert.rejects(()=>client.login('mock-access-code'),/쿠키/);
  assert.equal(calls.length,2);assert.equal(JSON.parse(calls[0].body).action,'login');assert.equal(client.state.authenticated,false);
});
test('login, refresh and logout keep credentials out of client state',async()=>{
  let cookie=false;const client=createConnection(async(_url,options)=>{if(options.method==='POST')cookie=JSON.parse(options.body).action==='login';return ok({server_configured:true,authenticated:cookie});});
  await client.login('mock-code');assert.equal((await client.refresh()).authenticated,true);
  assert.doesNotMatch(JSON.stringify(client.state),/mock-code|api_key|access_code/);
  await client.logout();assert.equal(client.state.authenticated,false);
});
test('wrong login reports the server error and never marks the visitor connected',async()=>{
  const client=createConnection(async()=>new Response(JSON.stringify({error:'접속 코드 오류'}),{status:401}));
  await assert.rejects(()=>client.login('wrong'),/접속 코드 오류/);assert.equal(client.state.authenticated,false);
});
test('older hosting adapters keep personal key mode available',async()=>{
  const client=createConnection(async()=>new Response('{}',{status:405}));
  assert.deepEqual(await client.refresh(),{server_configured:false,authenticated:false});
});
