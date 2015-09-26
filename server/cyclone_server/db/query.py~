_GET_USER_BY_EMAIL = \
    'SELECT Person.id, Person.email, pw_hash, display_name,' \
    ' user_name, Person.guid, Person.start_date,'\
    ' Person.last_login'\
    ' FROM Person INNER JOIN PersonEmail' \
    ' ON Person.id = PersonEmail.person_id' \
    ' WHERE PersonEmail.email = %s'
    
_INSERT_NEW_MAIL_ID = \
    'INSERT INTO PersonEmail(person_id, email)' \
    ' VALUES(%s, %s)'
    
_ADD_USER_ASYNC =\
    'INSERT INTO Person'\
    ' (guid, email,pw_hash,display_name, user_name, time_zone)'\
    ' VALUES(%s, %s, %s, %s, %s, %s) RETURNING id, guid;'

_ADD_TEMP_USER =\
    'INSERT INTO tempemail'\
    ' (email,pw_hash,display_name,user_name,guid)'\
    ' VALUES(%s, %s, %s, %s, %s) RETURNING *;'

_GET_TEMP_USER_BY_EMAIL = \
    'SELECT person_id, email, pw_hash, display_name, user_name,' \
    ' guid FROM  tempemail' \
    ' WHERE email = %s '

_GET_TEMP_USER_BY_GUID = \
    'SELECT * FROM tempemail' \
    ' WHERE guid = %s '

GET_DISQUERY_BY_USER = \
    'SELECT DISTINCT d.* FROM disquery d'\
    ' WHERE d.person_id = %s ORDER BY d.created_on DESC'

GET_DISQUERY_BY_GUID = \
    'SELECT * FROM DisQuery WHERE guid = %s'

GET_DISQUERY_META_BY_GUID = \
    'SELECT name, project_guid, person_id FROM DisQuery WHERE guid = %s'

GET_PLAYBACK_BY_GUID = \
    'SELECT playbackdata FROM DisQuery WHERE guid = %s'

INSERT_NEW_DISQUERY = \
    'INSERT INTO DisQuery(guid, name, person_id) VALUES (%s, %s, %s) RETURNING *'

UPDATE_DISQUERY_DATA = \
    'UPDATE DisQuery SET document_count = %s, location_count = %s,'\
    ' person_count = %s, organisation_count = %s, keyword_count = %s'\
    ' WHERE guid = %s AND person_id = %s'

UPDATE_PLAYBACK_DATA = \
    'UPDATE DisQuery SET playbackdata = array_append(playbackdata, %s)'\
    ' WHERE guid = %s AND person_id = %s'

UPDATE_DISQUERY_NAME = \
    'UPDATE DisQuery SET name = %s WHERE guid = %s AND person_id = %s RETURNING *'

UPDATE_NEW_DISQUERY_NAME = \
    'UPDATE DisQuery SET name = %s WHERE id = %s RETURNING *'

_GET_CUST_REPORT = \
    'select user_name,count(*) from person p,disquery d where p.id = d.person_id group by user_name;'

INSERT_NEW_PUBLIC_DISQUERY = \
    'INSERT INTO publicdisquery(dq_id, user_name,'\
    ' dq_name, dq_hash, jsondata, playbackdata, notes, document_count,'\
    ' location_count, person_count, organisation_count, keyword_count)'\
    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING guid;'

GET_PUBLIC_DISQUERY_BY_GUID = \
    'SELECT * FROM publicdisquery WHERE user_name = %s AND guid = %s'

GET_PUBLIC_DISQUERY_META_BY_GUID = \
    'SELECT dq_name, user_name FROM publicdisquery WHERE user_name = %s AND guid = %s'

GET_PUBLIC_DISQUERY_BY_HASH = \
    'SELECT * FROM publicdisquery WHERE user_name = %s AND dq_hash = %s'

GET_VER_GUIDS_FROM_IDS = \
    "SELECT id FROM documentversion WHERE guid IN %s"

_UPDATE_COMMENT_DELETE_STATUS = \
    'UPDATE Comment SET deleted = true, updated_on = utc_now() WHERE'\
    ' annotation_id IN %s;'

RM_DQ_WITH_PUBLIC = \
    'DELETE FROM Disquerynote WHERE dq_id ='\
    ' (SELECT id from disQuery WHERE guid = %s);'\
    ' DELETE FROM publicdisquery WHERE dq_id ='\
    ' (SELECT id from disQuery WHERE guid = %s) AND user_name = %s;'\
    ' DELETE FROM disquery WHERE guid = %s AND person_id = %s RETURNING *;'

RM_DQ_WITHOUT_PUBLIC = \
    'DELETE FROM Disquerynote WHERE dq_id ='\
    ' (SELECT id from disQuery WHERE guid = %s);'\
    ' UPDATE publicdisquery SET dq_id = null WHERE dq_id = '\
    ' (SELECT id from disQuery WHERE guid = %s) AND user_name = %s;'\
    ' DELETE FROM disquery WHERE guid = %s AND person_id = %s RETURNING *;'

ADD_DISQUERY_NOTE = \
    'INSERT INTO disquerynote (dq_id, note_key, fragment, type, created_by)'\
    ' VALUES ((SELECT id FROM disquery WHERE guid = %s), %s, %s, %s, %s)'\
    ' RETURNING *'

GET_DISQUERY_NOTES = \
    'SELECT * FROM disquerynote WHERE'\
    ' dq_id = (SELECT id FROM disquery WHERE guid = %s)'

GET_DQ_GUID_FROM_NOTE = \
    'SELECT guid FROM disquery'\
    ' WHERE id = (SELECT dq_id FROM disquerynote WHERE guid = %s)'

_UPDATE_DQ_OWNER =\
    'UPDATE Disquery SET person_id = %s WHERE project_guid = (SELECT guid FROM UserProject WHERE id=%s)'\
    ' AND person_id = %s RETURNING guid;'

_GET_CONSECUTIVE_INVALID_LOGINS_COUNT =\
    'SELECT failed_attempts FROM Person WHERE id=%s AND blocked_on IS NULL'

_GET_LOGIN_BLOCKED_ON =\
    'SELECT blocked_on FROM Person WHERE id=%s'

_SET_BLOCK_LOGIN_TIME =\
    'UPDATE Person SET (blocked_on, failed_attempts) = (utc_now(), 0) WHERE id=%s'

_RESET_INVALID_LOGIN_INFO =\
    'UPDATE Person SET (blocked_on, failed_attempts) = (NULL, 0) WHERE id=%s'

_INCR_FAILED_LOGIN =\
    'UPDATE Person SET failed_attempts = failed_attempts + 1 WHERE id=%s AND failed_attempts < 4'

_INSERT_FEED_SUBSCRIPTION =\
    ' INSERT INTO Feed (feed_id, title, feed_url, thumbnail)'\
    ' SELECT %s, %s, %s, %s WHERE NOT EXISTS'\
    ' (SELECT 1 FROM Feed WHERE feed_id = %s) RETURNING feed_id;'

_INSERT_FEED_SUBSCRIPTION_BY_USER_ID =\
    'UPDATE FeedSubscription SET subscribed_on = utc_now() WHERE'\
    ' feed_id = %s and person_id = %s;'\
    'INSERT INTO FeedSubscription (feed_id, person_id)'\
    ' SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM'\
    ' FeedSubscription WHERE feed_id = %s and person_id = %s) RETURNING feed_id;'

_GET_USER_SUBSCRIPTION_BY_USER_ID =\
    'SELECT f.* FROM Feed f INNER JOIN FeedSubscription fs ON f.feed_id'\
    ' = fs.feed_id WHERE fs.person_id = %s ORDER BY fs.subscribed_on ASC;'

_REMOVE_FEED_SUBSCRIPTION =\
    'DELETE FROM FeedSubscription WHERE feed_id = %s AND person_id = %s;'

_GET_FEED_SUBSCRIPTION_BY_FEED_ID =\
    'SELECT f.* FROM Feed f INNER JOIN FeedSubscription fs ON f.feed_id'\
    ' = fs.feed_id WHERE fs.person_id = %s ORDER BY fs.subscribed_on ASC;'

GET_LAST_LOGIN = \
    'SELECT last_login FROM Person WHERE id = %s'

SET_LAST_LOGIN = \
    'UPDATE Person SET last_login = %s WHERE id = %s'

SET_LAST_LOGIN_BY_GUID = \
    'UPDATE Person SET last_login = %s WHERE guid = %s'

_INSERT_TEMP_FILE =\
    "INSERT INTO TempFile (file_data, parent_guid, file_type)"\
    " VALUES (%s, %s, %s) RETURNING id;"

_UPDATE_TEMP_FILE = \
    'UPDATE TempFile Set parent_guid = %s '\
    'where id = %s'

_DELETE_TEMP_FILE = \
    'DELETE FROM TempFile WHERE parent_guid = %s'

_GET_TEMP_FILE =\
    'SELECT file_data FROM Tempfile WHERE id = %s;'

_GET_TEMP_FILE_BY_PARENT_GUID =\
    'SELECT * FROM TempFIle WHERE parent_guid = %s'

GET_WATCH_WORDS =\
    'SELECT * FROM watchkeyword WHERE person_id = %s ORDER BY type'
    
ADD_WATCH_WORD =\
    'INSERT INTO watchkeyword(person_id, watchterm, type)'\
    ' VALUES(%s, %s, %s)'

RM_WATCH_WORD_CUSTOM_ONLY =\
    'DELETE FROM matchedkeyword WHERE keyword_id IN'\
    ' (SELECT id FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s);'\
    ' DELETE FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s'

RM_WATCH_WORD =\
    'DELETE FROM matchedkeyword WHERE keyword_id IN'\
    ' (SELECT id FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s);'\
    'DELETE FROM matchedkeyword WHERE keyword_id IN'\
    ' (SELECT id FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s);'\
    ' DELETE FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s;'\
    ' DELETE FROM watchkeyword WHERE person_id = %s AND lower(watchterm) = %s AND type = %s'

_LIST_USER_PROJECTS =\
    'SELECT DISTINCT up.* FROM UserProject up LEFT JOIN ProjectCollaborator pc'\
    ' ON up.id = pc.project_id WHERE pc.person_id = %s'\
    ' OR up.person_id=%s ORDER BY up.updated_on'

_USER_DOCS_DQ =\
    'SELECT DISTINCT d.*, dv.uploaded_on AS update, dv.thumbnails, dv.guid AS ver_guid'\
    ' FROM Document d INNER JOIN'\
    ' UserProject up ON d.project_id = up.id'\
    ' INNER JOIN DocumentVersion dv ON d.id = dv.document_id'\
    ' LEFT JOIN ProjectCollaborator pc ON up.id=pc.project_id'\
    ' WHERE up.person_id = %s OR pc.person_id = %s'\
    ' ORDER BY dv.uploaded_on DESC LIMIT %s OFFSET %s'

_ADD_TO_GRAPH_QUEUE = \
    'INSERT INTO GraphQueue' \
    ' (data, url, deletion)' \
    ' VALUES (%s, %s, %s) returning id'

CHECK_ACCESS_TO_PROJECT_BY_GUID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.guid = %s'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_PROJECT_BY_ID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id = %s'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id = up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_DOCUMENT_BY_GUID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Document d where d.guid = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_DOCUMENT_BY_ID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Document d where d.id = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_DOCUMENT_VERSION_BY_GUID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Document d INNER JOIN DocumentVersion dv'\
    ' ON d.id = dv.document_id WHERE dv.guid = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_DOCUMENT_VERSION_BY_ID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Document d INNER JOIN DocumentVersion dv'\
    ' ON d.id = dv.document_id WHERE dv.id = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_TASK_BY_GUID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Task t where t.guid = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_TASK_BY_ID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT project_id from Task t where t.id = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_ANNOTATION_BY_GUID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT CASE WHEN ann.project_id IS NULL THEN d.project_id'\
    ' ELSE ann.project_id END FROM Annotation ann'\
    ' LEFT JOIN DocumentVersion dv ON ann.version_id = dv.id'\
    ' LEFT JOIN document d ON d.id = dv.document_id where ann.guid = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id'\
    ' and  pj.person_id = %s))'

CHECK_ACCESS_TO_ANNOTATION_BY_ID =\
    'SELECT 1 AS access FROM UserProject up WHERE up.id =('\
    ' SELECT CASE WHEN ann.project_id IS NULL THEN d.project_id'\
    ' ELSE ann.project_id END FROM Annotation ann'\
    ' LEFT JOIN DocumentVersion dv ON ann.version_id = dv.id'\
    ' LEFT JOIN document d ON d.id = dv.document_id where ann.id = %s)'\
    ' AND (up.person_id = %s OR EXISTS'\
    ' (SELECT 1 FROM ProjectCollaborator pj where pj.project_id=up.id))'

# FIX-ME - This query is not ideal when document versioning is implemented
_PROJECT_DOCS =\
    'SELECT DISTINCT d.*, dv.updated_on as update, dv.thumbnails'\
    ' FROM Document d INNER JOIN'\
    ' UserProject up ON d.project_id = up.id'\
    ' INNER JOIN DocumentVersion dv ON d.id = dv.document_id'\
    ' WHERE up.guid = %s'\
    ' ORDER BY dv.updated_on asc'

_PROJECT_DOCS_WITH_LIMIT =\
    'Select * from ('\
    ' SELECT DISTINCT d.*, dv.updated_on as update, dv.thumbnails'\
    ' FROM Document d INNER JOIN'\
    ' UserProject up ON d.project_id = up.id'\
    ' INNER JOIN DocumentVersion dv ON d.id = dv.document_id'\
    ' WHERE up.guid = %s ORDER BY dv.updated_on desc'\
    ' LIMIT %s OFFSET %s) as docVer'\
    ' order by update asc'

_DOC_VERSIONS = \
    'SELECT * FROM DocumentVersion'\
    ' WHERE document_id = %s ORDER BY version DESC'

_GET_SOURCE_TYPE_BY_VERSION_ID = \
    'SELECT type FROM SourceMetaData WHERE version_id = %s;'

_ADD_TO_INDEX_QUEUE = \
    'INSERT INTO IndexQueue' \
    ' (index_data, index_url, deletion)' \
    ' VALUES (%s, %s, %s) returning id'

_GET_DOC_VERSION_SUMMARY = \
    'SELECT guid, summary from DocumentVersion '\
    ' where guid = %s '

_USER_LATEST_DOCS =\
    'SELECT * FROM ('\
    ' SELECT DISTINCT d.id, d.guid, d.title, d.owner_id, d.deleted,'\
    ' d.project_id, d.document_type,dv.uploaded_on'\
    ' FROM Document d INNER JOIN DocumentVersion dv ON d.id = dv.document_id'\
    ' INNER JOIN UserProject up ON d.project_id=up.id'\
    ' WHERE d.deleted <> true AND (up.person_id = %s OR up.isglobal = TRUE)'\
    ' ORDER BY dv.uploaded_on DESC LIMIT %s OFFSET %s) AS docs'\
    ' ORDER BY uploaded_on ASC'

_GET_ALL_DOCUMENTS_COUNT_BY_USER_ID =\
    'SELECT count(*) FROM Document d INNER JOIN DocumentVersion dv ON d.id ='\
    ' dv.document_id INNER JOIN UserProject up ON d.project_id = up.id WHERE'\
    ' d.deleted <> true AND (up.person_id = %s OR up.isglobal = TRUE )'
    
_GET_DOCUMENT_COUNT_BY_PROJECT_ID = \
    'select count(*) as count from Document where project_id = %s'\
    ' and deleted = false;'

_GET_FAILED_DOC_RETRY_COUNT = \
    'select count(*) as count from VersionImportState where version_id = %s'    
    
_INSERT_NEW_FTP_AC = \
    'INSERT INTO documentsource(person_id, project_id, source_type, access_token, access_token_secret, source_path, port, sync, title)' \
    ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) returning *'
    
_GET_FTP_SETTINGS =\
    'SELECT * FROM documentsource WHERE person_id = %s '
    
_REMOVE_FTP_SETTING =\
    'DELETE FROM documentsource WHERE guid = %s and person_id = %s;'

_CREATE_MY_FEED = \
    'INSERT INTO UserProject (person_id, project_name, color)'\
    ' VALUES(%s, %s, %s) returning *'

_GET_PROJECT_BY_ID = \
    'SELECT * FROM UserProject WHERE id = %s;'

_GET_DOCUMENT_SOURCE_BY_USER_ID = \
   'SELECT ds.id, ds.guid, ds.person_id, ds.title, ds.type, ds.access_token,' \
   'ds.access_token_secret, ds.user_id, ds.user_name, ds.email, ec.server,' \
   'ec.port, ec.usessl, ec.password, ds.added_on, ds.updated_on, ds.folder_id, ds.data_id, ds.status, f.url' \
   ' FROM documentsource ds FULL JOIN' \
   ' emailconfiguration ec ON ds.id=ec.document_source_id RIGHT OUTER JOIN' \
   ' ftp f on f.person_id = ds.person_id' \
   ' WHERE (ds.person_id = %s OR f.person_id = %s)'
    
_GET_PROJECT_BY_GUID = \
    'SELECT * FROM UserProject WHERE' \
    ' guid = %s;'

_USER_PROJS = \
    'SELECT * ' \
    ' FROM UserProject WHERE person_id = %s' \
    ' ORDER BY id ASC'
    
_ADD_SYNC_SLOTS = \
    'INSERT INTO syncperiod(sync_mins, ds_id)'\
    ' VALUES(%s, %s)'
    
_REMOVE_SYNC_SLOT =\
    'DELETE FROM syncperiod WHERE ds_id = %s;'
    
_GET_FTP_SETTINGS_GUID =\
    'SELECT * FROM documentsource WHERE guid = %s '

_GET_SEARCH_TERMS_BY_USER_ID =\
    'SELECT search_term FROM savedsearch WHERE person_id = %s'\
    ' ORDER BY last_search DESC LIMIT %s OFFSET %s;'

_INSERT_OR_UPDATE_SEARCH_TERMS_BY_USER_ID =\
    'UPDATE savedsearch SET last_search = utc_now() WHERE'\
    ' person_id = %s AND search_term = %s;'\
    ' INSERT INTO savedsearch (person_id, search_term)'\
    ' SELECT %s, %s WHERE NOT EXISTS'\
    ' (SELECT 1 FROM savedsearch WHERE person_id = %s AND search_term = %s);'

_GET_ARTICLE_SENTENCE_BY_ARTICLE_ID =\
    'SELECT a.id, a.article_date, a.source_url, a.title, ase.sentence, ase.lexicon_match, ase.id as'\
    ' sentence_id, ase.lexicon_acq, ase.lexicon_vnsp, ase.lexicon_nc, ase.lexicon_job FROM Article a'\
    ' INNER JOIN ArticleSentence ase ON a.id = ase.article_id WHERE a.id = %s;'

_INSERT_OR_UPDATE_CLASSIFIED_SENT =\
    'UPDATE SentenceClassification SET ACQ = %s, VNSP = %s, JOB = %s, NC = %s,'\
    ' subjective = %s, is_ignored = %s WHERE person_id = %s AND sentence_id = %s;'\
    ' INSERT INTO SentenceClassification (ACQ, VNSP, JOB, NC, subjective, is_ignored, person_id, sentence_id)'\
    ' SELECT %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS'\
    ' (SELECT 1 FROM SentenceClassification WHERE person_id = %s AND sentence_id = %s);'

_GET_ARTICLE_SENTENCES =\
    'SELECT a.id, a.article_date, a.source_url, a.title, ase.sentence, ase.lexicon_match, ase.id as'\
    ' sentence_id, ase.lexicon_acq, ase.lexicon_vnsp, ase.lexicon_nc, ase.lexicon_job FROM Article a'\
    ' INNER JOIN ArticleSentence ase ON a.id = ase.article_id WHERE a.id = (Select Min(id) from Article);'

_GET_ARTICLE_WITH_DATE_RANGE =\
    'SELECT a.id, a.article_date, a.source_url, a.title, ase.sentence, ase.lexicon_match, ase.id as'\
    ' sentence_id, ase.lexicon_acq, ase.lexicon_vnsp, ase.lexicon_nc, ase.lexicon_job FROM Article a'\
    ' INNER JOIN ArticleSentence ase ON a.id = ase.article_id WHERE a.id = (Select id from article'\
    ' where a.article_date::date = %s ORDER BY a.article_date LIMIT 1);'
    
_GET_LIST_OF_MERCHANT =\
    'SELECT * FROM Merchant;'
    
_GET_FEMALE_CUSTOMER_FOR_MERCHANT =\
     "Select count(*) from Merchant m inner join MerchantProduct mp on mp.merchantid = m.id inner join"\
     "TransactionHistory th on th.merchant_product_id = mp.productId inner join Person p on p.id = th.user_id"\
     " and p.sex = 'female' where m.id = %s;"
     
_GET_MALE_CUSTOMER_FOR_MERCHANT =\
     "Select count(*) from Merchant m inner join MerchantProduct mp on mp.merchantid = m.id inner join"\
     "TransactionHistory th on th.merchant_product_id = mp.productId inner join Person p on p.id = th.user_id"\
     " and p.sex = 'male' where m.id = %s;"

