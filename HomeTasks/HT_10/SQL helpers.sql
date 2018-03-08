-- Select column names for table
select column_name from information_schema.columns where table_name='jobstories'

-- Select tablenames in Database
SELECT table_name
FROM information_schema.tables
where table_schema = 'public'
