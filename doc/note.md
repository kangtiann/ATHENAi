# Note

## Useful DB SQLs

All researchs:
```sql
select r.id, v.vision, r.research, r.research_desc, r.status
    from research r
    left join vision v on r.vision_id=v.id;
```

All Deepthinks:
```sql
select v.vision, r.research, t.deepthink, t.deepthink_desc, t.status
    from deepthink t
    left join research r on t.research_id=r.id
    left join vision v on r.vision_id=v.id;
```

Accept Researchs:
```sql
update research set status = 'ready' where status='proposed';
```