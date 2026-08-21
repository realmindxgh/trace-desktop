from pathlib import Path
import sqlite3, time, uuid

ROOT=Path(__file__).resolve().parents[1]
schema=(ROOT/'database/schema.sql').read_text(encoding='utf-8')
con=sqlite3.connect(':memory:')
con.execute('PRAGMA foreign_keys=ON')
con.executescript(schema)

def cols(table):
    return {r[1] for r in con.execute(f'PRAGMA table_info({table})')}

required={
 'projects':{'id','title','coding_mode'},
 'research_questions':{'id','project_id','position','text'},
 'participants':{'id','project_id','label'},
 'sources':{'id','project_id','participant_id','kind','plain_text'},
 'transcript_segments':{'id','source_id','start_char','end_char','text'},
 'codes':{'id','project_id','parent_id','origin'},
 'coding_references':{'id','code_id','source_id','start_offset','end_offset','ai_suggestion_id'},
 'media_selections':{'id','project_id','source_id','selection_type','begin_ms','end_ms','page','first_x','first_y','second_x','second_y'},
 'media_codings':{'id','project_id','selection_id','code_id'},
 'variables':{'id','project_id','value_type'},
 'variable_values':{'id','variable_id','owner_type','owner_id'},
 'evidence_anchors':{'id','source_id','start_offset','end_offset','exact_text'},
 'evidence_links':{'id','from_type','from_id','to_type','to_id','relation'},
 'ai_suggestions':{'id','stage','suggestion_json','status'},
 'ai_provenance':{'id','suggestion_id','action','actor_type'},
 'audit_events':{'id','actor_type','event_type'},
 'source_properties':{'source_id','project_id','archived','favourite','notes'},
 'source_collections':{'id','project_id','name'},
 'source_collection_members':{'collection_id','source_id'},
 'backup_policies':{'project_id','enabled','interval_minutes','keep_count','last_backup_at'},
}
for table,need in required.items():
    missing=need-cols(table)
    assert not missing,(table,missing)

now=int(time.time()*1000); uid=lambda:str(uuid.uuid4())
pid,part,sid,seg,cid,aid=[uid() for _ in range(6)]
con.execute('INSERT INTO projects(id,title,methodology,coding_mode,created_at,updated_at) VALUES(?,?,?,?,?,?)',(pid,'Contract test','Reflexive Thematic Analysis','ai',now,now))
con.execute('INSERT INTO participants(id,project_id,label,created_at) VALUES(?,?,?,?)',(part,pid,'P01',now))
text='The class has fifty-eight students.'
con.execute('INSERT INTO sources(id,project_id,participant_id,kind,original_name,display_name,plain_text,imported_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',(sid,pid,part,'text','p01.txt','P01',text,now,now))
con.execute('INSERT INTO transcript_segments(id,source_id,position,speaker,start_char,end_char,text) VALUES(?,?,?,?,?,?,?)',(seg,sid,0,'P01',0,len(text),text))
con.execute('INSERT INTO codes(id,project_id,name,is_codable,origin,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,pid,'Large class size',1,'ai_suggested',now,now))
con.execute('INSERT INTO ai_suggestions(id,project_id,stage,target_type,target_id,prompt_context_json,suggestion_json,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(aid,pid,'coding','segment',seg,'{}','{"name":"Large class size"}','pending',now))
ref=uid(); start=text.index('fifty-eight'); end=start+len('fifty-eight')
con.execute('INSERT INTO coding_references(id,project_id,code_id,source_id,segment_id,start_offset,end_offset,exact_text,origin,ai_suggestion_id,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(ref,pid,cid,sid,seg,start,end,text[start:end],'researcher_approved_ai',aid,now))
anchor=uid();con.execute('INSERT INTO evidence_anchors(id,project_id,source_id,segment_id,start_offset,end_offset,exact_text,origin,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(anchor,pid,sid,seg,start,end,text[start:end],'researcher',now))
rqid=uid();con.execute('INSERT INTO research_questions(id,project_id,position,text) VALUES(?,?,?,?)',(rqid,pid,0,'What barriers do teachers experience?'))
link=uid();con.execute('INSERT INTO evidence_links(id,project_id,from_type,from_id,to_type,to_id,relation,created_at) VALUES(?,?,?,?,?,?,?,?)',(link,pid,'evidence_anchor',anchor,'research_question',rqid,'supports',now))
var=uid();con.execute('INSERT INTO variables(id,project_id,name,value_type,created_at,updated_at) VALUES(?,?,?,?,?,?)',(var,pid,'Experience years','Integer',now,now))
con.execute('INSERT INTO variable_values(id,project_id,variable_id,owner_type,owner_id,value_integer,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',(uid(),pid,var,'participant',part,6,now,now))
con.execute('INSERT INTO ai_provenance(id,project_id,suggestion_id,action,actor_type,after_json,created_at) VALUES(?,?,?,?,?,?,?)',(uid(),pid,aid,'generated','trace_ai','{}',now))
con.commit()
assert con.execute('SELECT exact_text FROM coding_references WHERE id=?',(ref,)).fetchone()[0]=='fifty-eight'
assert con.execute('SELECT value_integer FROM variable_values WHERE variable_id=?',(var,)).fetchone()[0]==6
assert con.execute('SELECT relation FROM evidence_links WHERE id=?',(link,)).fetchone()[0]=='supports'
ms=uid();mc=uid();con.execute('INSERT INTO media_selections(id,project_id,source_id,selection_type,begin_ms,end_ms,origin,created_at) VALUES(?,?,?,?,?,?,?,?)',(ms,pid,sid,'audio',1200,3900,'researcher',now));con.execute('INSERT INTO media_codings(id,project_id,selection_id,code_id,origin,created_at) VALUES(?,?,?,?,?,?)',(mc,pid,ms,cid,'researcher',now));assert con.execute('SELECT end_ms-begin_ms FROM media_selections WHERE id=?',(ms,)).fetchone()[0]==2700
con.execute('INSERT INTO source_properties(source_id,project_id,favourite,updated_at) VALUES(?,?,?,?)',(sid,pid,1,now));con.execute('INSERT INTO backup_policies(project_id,enabled,interval_minutes,keep_count) VALUES(?,?,?,?)',(pid,1,15,20));assert con.execute('SELECT favourite FROM source_properties WHERE source_id=?',(sid,)).fetchone()[0]==1;assert con.execute('SELECT interval_minutes FROM backup_policies WHERE project_id=?',(pid,)).fetchone()[0]==15
print('Trace v0.6 SQLite schema contract passed')
