#!/usr/bin/env python3
"""Independent read-only public delivery check; optional GitHub incident notice."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
import urllib.request
import urllib.error
import uuid

BASE = 'https://donarfang.github.io/SP500-tracker/'
LIVE = 'exports/official/FD-M3180125-SP500-TOP3-engine/live/'
TITLE = '[DB-step-2] Live delivery incident'
TEST_TITLE = '[DB-step-2] Notification receipt confirmation'
MARKER = 'db-step2-freshness-v1'

def expected_date(calendar, now):
    """Each market session is due at 00:45 UTC next day (08:45 Taiwan)."""
    if now.tzinfo is None:
        raise ValueError('aware time required')
    today = now.astimezone(timezone.utc).date()
    if not calendar['coverage_start'] <= today.isoformat() <= calendar['coverage_end']:
        raise ValueError('calendar coverage expired')
    closed = set(calendar['full_day_closures']) | set(calendar.get('extraordinary_full_day_closures',[]))
    day = today
    for _ in range(15):
        due = datetime.combine(day+timedelta(days=1),datetime.min.time(),timezone.utc)+timedelta(minutes=45)
        if day.weekday()<5 and day.isoformat() not in closed and now>=due:
            if day.isoformat()<calendar['coverage_start']:
                raise ValueError('calendar has no covered completed session')
            return day.isoformat()
        day -= timedelta(days=1)
    raise ValueError('no due session')

def get(path):
    url = BASE+path+'?db_step2='+uuid.uuid4().hex
    req = urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'FD-M3180125-DB-step2'})
    with urllib.request.urlopen(req,timeout=25) as response:
        return response.read()

def inspect_public(getter=get, now=None):
    now = now or datetime.now(timezone.utc)
    calendar = json.loads(getter('config/live_calendar/us_equity_calendar_v1.0.json'))
    expected = expected_date(calendar,now)
    html = getter('dashboard/index.html').decode('utf-8')
    js = getter('dashboard/db-step2-freshness.js').decode('utf-8')
    if MARKER not in html or MARKER not in js:
        raise ValueError('public dashboard freshness component not deployed')
    state = json.loads(getter(LIVE+'runtime/current/runtime_state.json'))
    rec_raw = getter(LIVE+'runtime/current/latest_recommendations.json')
    rec = json.loads(rec_raw)
    market_raw = getter(LIVE+'runtime/current/latest_market_status.json')
    market = json.loads(market_raw)
    actual = state.get('last_committed_market_date')
    if not isinstance(actual,str) or actual < expected:
        raise ValueError('stale Live: expected >= '+expected+', actual='+str(actual))
    date.fromisoformat(actual)
    if actual>now.date().isoformat():
        raise ValueError('future market date')
    if rec.get('signal_date')!=actual or market.get('date')!=actual:
        raise ValueError('current state/recommendations/market dates disagree')
    if state.get('status')!='ACTIVE' or rec.get('recommendation_only') is not True:
        raise ValueError('unexpected Live mode')
    daily=LIVE+'runtime/daily/'+actual+'/'
    manifest=json.loads(getter(daily+'manifest.json'))
    if manifest.get('market_date')!=actual or manifest.get('validation_status')!='PASS':
        raise ValueError('daily manifest not PASS')
    hashes=manifest.get('files',{})
    for name,raw in [('engine_recommendations.json',rec_raw),('market_status.json',market_raw)]:
        if hashlib.sha256(raw).hexdigest()!=hashes.get(name):
            raise ValueError('current artifact differs from daily manifest: '+name)
    return {'expected_market_date':expected,'actual_market_date':actual,'execution_date':rec.get('expected_execution_date'),'public_page_verified':True,'public_artifacts_verified':True}

def api(path,body=None,method=None):
    token=os.environ.get('GITHUB_TOKEN','')
    if not token:
        raise ValueError('GITHUB_TOKEN unavailable for notification')
    req=urllib.request.Request('https://api.github.com/repos/DonarFang/SP500-tracker/'+path,data=None if body is None else json.dumps(body).encode(),method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'DB-step2'})
    with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)

def notify(report):
    issues=[]
    receipt=[]
    for page in range(1,11):
        rows=api('issues?state=all&per_page=100&page='+str(page))
        receipt.extend(x for x in rows if x.get('title')==TEST_TITLE and x.get('user',{}).get('login')=='github-actions[bot]')
        issues.extend(x for x in rows if x.get('title')==TITLE and x.get('state')=='open' and 'pull_request' not in x and x.get('user',{}).get('login')=='github-actions[bot]')
        if len(rows)<100:break
    else:raise ValueError('issue pagination limit reached; refusing duplicate notification')
    if report['status']=='PASS':
        if not receipt:
            api('issues',{'title':TEST_TITLE,'body':'@DonarFang DB-step-2 public delivery checks are enabled. This is a one-time notification test. Please confirm that you received the GitHub/email/mobile notification; opening this issue manually alone does not prove delivery.\n\n- [ ] Notification received by the account owner\n\nThis message does not confirm a trade or change trading rules.'})
        for issue in issues:
            api('issues/'+str(issue['number'])+'/comments',{'body':'Public delivery recovered.\n```json\n'+json.dumps(report,indent=2)+'\n```'})
            api('issues/'+str(issue['number']),{'state':'closed'},'PATCH')
        return 'RECOVERY_RECORDED' if issues else 'NO_INCIDENT'
    body='@DonarFang Live update is stale or failed. Old recommendations must not be treated as current.\n\n```json\n'+json.dumps(report,indent=2)+'\n```'
    if issues:
        api('issues/'+str(issues[0]['number']),{'body':body},'PATCH')
        return 'EXISTING_INCIDENT_UPDATED'
    issue=api('issues',{'title':TITLE,'body':body})
    return 'ISSUE_CREATED:'+issue['html_url']

def main():
    p=argparse.ArgumentParser();p.add_argument('--notify',action='store_true');p.add_argument('--output',default='db-step2-monitor.json');p.add_argument('--event-file');a=p.parse_args()
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'status':'HOLD','notification_delivery':'NOT_VERIFIED'}
    try:
        report.update(inspect_public());report['status']='PASS'
    except Exception as e:report['error']=str(e)
    if a.event_file:
        event=json.loads(Path(a.event_file).read_text());run=event.get('workflow_run',{})
        if run.get('conclusion') in {'failure','cancelled','timed_out','action_required'}:
            report.update(status='HOLD',failed_workflow=run.get('name'),run_url=run.get('html_url'),conclusion=run.get('conclusion'))
    report['monitor_run']='https://github.com/DonarFang/SP500-tracker/actions/runs/'+os.environ.get('GITHUB_RUN_ID','local')
    if a.notify:
        try:report['notification_action']=notify(report)
        except Exception as e:report.update(status='HOLD',notification_error=str(e))
    Path(a.output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
    return 0 if report['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
