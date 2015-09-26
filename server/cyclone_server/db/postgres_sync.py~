from contextlib import closing
import query
import datetime


class PostgresDatabaseSync(object):
    def __init__(self, connection, cache=None):
        self.connection = connection

    def _got_user(self, rows):
        if rows:
            return self._got_users(rows)[0]

    def _got_users(self, rows):
        l = []
        if rows:
            for row in rows:
                l.append(
                    User(
                        self, row.id, row.email, row.pw_hash,
                        row.display_name, row.user_name))
        return l

    def get_user_by_email(self, email):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._GET_USER_BY_EMAIL, (email.lower(), ))
            obj = cursor.fetchone()
            if obj:
                return User(self, obj[0], obj[1], obj[2], obj[3], obj[4])

    def get_user_by_id(self, user_id):
        '''if isinstance(user_id, (str, unicode)):
            user_id = int(user_id)
        d = self.connection.runQuery(
                'SELECT * FROM Person'
                ' WHERE id = %s', (user_id,))
        return d.addCallback(self._got_user)'''

    def __get_cursor(self):
        return closing(self.connection.cursor())

    def _init_new_user(self, person_id, email):
        newprj = self.create_my_feed_project(person_id, color='#f48d64')
        self.add_email(person_id, email)
        return newprj

    def _person_created(self, r, email, pw_hash):
        assert len(r) == 1
        person_id = r[0].id
        self._init_new_user(person_id, email)
        return User(self, person_id, email, pw_hash)

    def _person_creation_error(self, err):
        return None

    def _got_temp_user(self, rows):
        if rows:
            return self._got_temp_users(rows)[0]

    def _got_temp_users(self, rows):
        l = []
        if rows:
            for row in rows:
                l.append(
                    User(
                        self, row.person_id, row.email,
                        row.pw_hash, row.display_name, row.user_name))
        return l

    def get_temp_user_by_email(self, email):
        '''return self.connection.runQuery(
            query._GET_TEMP_USER_BY_EMAIL, (email.lower(),)
            ).addCallback(self._got_temp_users)'''

    def get_temp_user_by_username(self, user_name):
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM tempemail WHERE'
                ' user_name = %s',
                (user_name.lower(),))
            x = cursor.fetchone()
            self.connection.commit()
            return x

    def remove_temp_user(self, email):
        with self.__get_cursor() as cursor:
            cursor.execute(
                'DELETE FROM tempemail WHERE email = %s',
                (email.lower(),))
            self.connection.commit()

    def rm_user(self, email):
        with self.__get_cursor() as cursor:
            user_id = self.get_user_by_email(email)._id
            cursor.execute(
                'DELETE FROM emailconfiguration' +
                ' WHERE document_source_id in (SELECT id FROM documentsource' +
                ' WHERE person_id = %s);', (user_id,))
            cursor.execute(
                'DELETE FROM documentsource WHERE person_id = %s;', (user_id,))
            cursor.execute(
                'DELETE FROM UserAction WHERE performed_by = %s;', (user_id,))
            cursor.execute(
                'DELETE FROM ProjectCollaborator \
                WHERE person_id = %s;', (user_id,))
            cursor.execute(
                'DELETE FROM UserProject WHERE person_id = %s;', (user_id,))
            cursor.execute(
                'DELETE FROM PersonEmail WHERE person_id = %s;', (user_id,))
            cursor.execute(
                'DELETE FROM Person WHERE id = %s;', (user_id,))
            self.connection.commit()

    def list_users(self):
        with self.__get_cursor() as cursor:
            cursor.execute('SELECT * FROM Person;')
            for record in cursor:
                yield self._got_user([record])

    def _document_created(self, r):
        assert len(r) == 1
        return self._got_document(r)

    def _doc_create_check(
            self, r, user_id, title,
            guid, file_type, project_guid):
        if len(r) != 0:
            return self._got_document(r)
        # In this case, we need to go ahead and insert it
        '''return self.connection.runQuery(
                    'INSERT INTO Document(title, owner_id, guid, project_id,'
                    ' document_type)'
                    ' VALUES(%s, %s, %s,'
                    ' (SELECT id FROM UserProject WHERE guid = %s)'
                    ' , %s)'
                    ' RETURNING *;',
                    (title, user_id, guid, project_guid, file_type)
                    ).addCallback(self._document_created)'''

    def create_document(
            self, owner, project_guid, title=None,
            guid=None, document_type='pdf'):
        if isinstance(owner, User):
            user_id = owner._id
        else:
            user_id = owner
        with self.__get_cursor() as cursor:
            cursor.execute(
                'INSERT INTO Document(title, owner_id,'
                ' project_id, document_type) VALUES(%s, %s,'
                ' (SELECT id FROM UserProject WHERE guid = %s)'
                ' , %s) RETURNING id',
                (title, user_id, project_guid, document_type))
            id = cursor.fetchone()[0]
            self.connection.commit()
            return id

        if guid:
            '''d = self.connection.runQuery(
                    'SELECT *'
                    ' FROM Document WHERE'
                    ' owner_id = %s AND guid = %s;',
                    (user_id, guid)).addCallback(
                            self._doc_create_check, user_id, title,
                            guid, document_type, project_guid)'''
        else:
            '''d = self.connection.runQuery(
                    'INSERT INTO Document(title, owner_id,'
                    ' project_id, document_type) VALUES(%s, %s,'
                    ' (SELECT id FROM UserProject WHERE guid = %s)'
                    ' , %s) '
                    ' RETURNING *;',
                    (title, user_id, project_guid, document_type)).addCallback(
                            self._document_created)
        return d'''

    def _got_project(self, r):
        x = None
        if isinstance(r, list):
            if len(r) > 0:
                x = r[0]
        else:
            x = r
        if x:
            return Project(self, x.id, x.guid, x.person_id, x.project_name)

    def get_project_by_name(self, person_id, project_name):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._GET_PROJECT_BY_NAME, (person_id, project_name))
            self.connection.commit()
            x = cursor.fetchone()
            return Project(self, x[0], x[1], x[2], x[3])

    def get_project_by_guid(self, project_guid):
        with self.__get_cursor() as cursor:
            cursor.execute(query._GET_PROJECT_BY_GUID, (project_guid,))
            self.connection.commit()
            x = cursor.fetchone()
            return Project(self, x[0], x[1], x[2], x[3])

    def _got_document(self, r):
        x = None
        if isinstance(r, list):
            if len(r) > 0:
                x = r[0]
        else:
            x = r
        if x:
            return Document(
                self, x.id,
                x.guid, x.title, x.owner_id,
                x.deleted, x.project_id,
                x.document_type)

    def get_document(self, doc_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query._GET_DOC_BY_ID, (doc_id,))
            d = cursor.fetchone()
        return Document(self, d[0], d[1], d[2], d[3], d[4], d[5], d[6])

    def get_doc_comments_from_layer_id(self, layer_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query.DOC_COMMENT_LAYER_ID, (layer_id,))
            d = cursor.fetchone()
        return d

    def rm_comment_by_guid(self, guid):
        with self.__get_cursor() as cursor:
            cursor.execute('DELETE FROM Comment WHERE guid = %s;', (guid,))
            self.connection.commit()

    def rm_document_by_id(self, doc_id):
        with self.__get_cursor() as cursor:
            cursor.execute('DELETE FROM Document WHERE id = %s;', (doc_id,))
            self.connection.commit()

    def rm_version_by_id(self, ver_id):
        with self.__get_cursor() as cursor:
            cursor.execute(
                'DELETE FROM DocumentVersion WHERE id = %s;', (ver_id,))
            self.connection.commit()

    def rm_version_by_document_id(self, doc_id):
        with self.__get_cursor() as cursor:
            cursor.execute(
                'DELETE FROM DocumentVersion WHERE document_id = %s;',
                (doc_id,))
            self.connection.commit()

    def get_document_from_guid(self, guid):
        with self.__get_cursor() as cursor:
            cursor.execute('SELECT * FROM Document WHERE guid = %s',
                           (guid,))
            x = cursor.fetchone()
            self.connection.commit()
        return x

    def get_document_from_id(self, doc_id):
        with self.__get_cursor() as cursor:
            cursor.execute('SELECT * FROM Document WHERE id = %s',
                           (doc_id,))
            x = cursor.fetchone()
            self.connection.commit()
        return x

    def get_document_collaborators(self, doc_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DOC_COLLABORATORS, (doc_id,))
            x = cursor.fetchone()
            self.connection.commit()
        return x

    def get_document_version_collaborators(self, docver_id):
        '''return self.connection.runQuery(query._DOCVER_COLLABORATORS,
                (docver_id,)).addCallback(self._got_users)'''

    def _got_doc_versions(self, r, full=False):
        l = []
        if len(r) > 0:
            for o in r:
                d = DocumentVersion(
                    self, o.id, o.guid,
                    o.version, o.file_hash,
                    _pages=o.pages, _title=o.title,
                    _author=o.author, _uploaded_by=o.uploaded_by,
                    _uploaded_on=o.uploaded_on,
                    _upload_type=o.upload_type, _s3_bucket=o.s3_bucket,
                    _s3_key=o.s3_key, _s3_url=o.s3_url,
                    _thumbnails=o.thumbnails,
                    _document_id=o.document_id)
                l.append(d)
        return l

    def get_document_versions(self, doc_id, getAll=True):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DOC_VERSIONS, (doc_id,))
            o = cursor.fetchone()
        return o[1]

    def _get_single(self, r):
        if isinstance(r, list) and len(r) > 0:
            return r[0]

    def get_document_version(self, version_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DOC_VERSION_ID, (version_id,))
            x = cursor.fetchone()
            return x

    def get_latest_document_version(self, doc_id):
        '''return self.connection.runQuery(query._DOC_VERSION_LATEST,
                (doc_id,)).addCallback(
                        self._got_doc_versions, full=True).addCallback(
                                self._get_single)'''

    def get_document_version_from_guid(self, guid):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DOC_VERSION_GUID, (guid,))
            d = cursor.fetchone()
            self.connection.commit()
            return DocumentVersion(self, d[0], d[1], d[2], d[3])

    def get_document_version_from_id(self, dv_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DOC_VERSION_ID, (dv_id,))
            d = cursor.fetchone()
            self.connection.commit()
            return DocumentVersion(self, d[0], d[1], d[2], d[3])

    def add_document_version(
            self, doc_id, guid, uploaded_by=None,
            upload_type='ios', source=None):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._DOC_VERSION_ADD,
                (guid, doc_id, doc_id, uploaded_by, upload_type, source))
            d = cursor.fetchone()
            self.connection.commit()
            return d[0]

    def _got_docid_list(self, dl):
        return map(self._got_document, dl)

    def list_documents(self, user_id):
        '''return self.connection.runQuery(query._USER_DOCS,
                (user_id,)).addCallback(self._got_docid_list)'''

    def move_doc_to_project(self, project_guid, document_guid):
        '''return self.connection.runOperation(
                query._MOVE_DOC_TO_PROJ,
                (project_guid, document_guid)
                )'''

    def add_project(self, project_guid, person_id, project_name):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._ADD_PROJ,
                (project_guid, str(person_id), project_name))
        self.connection.commit()

    def rm_project_by_guid(self, project_guid):
        with self.__get_cursor() as cursor:
            cursor.execute('DELETE FROM UserProject WHERE guid = %s;',
                           (project_guid,))
            self.connection.commit()

    def _got_projid_list(self, pl):
        return map(self._got_project, pl)

    def list_projects(self, user_id):
        '''return self.connection.runQuery(query._USER_PROJS,
                (user_id,)).addCallback(self._got_projid_list)'''

    def _got_annotations(self, r):
        l = []
        for a in r:
            l.append(
                Annotation(
                    self, a.id, a.guid, a.layer_id, a.page, a.position,
                    a.fragment, a.created_by, a.created_on, a.is_hilight))
        return l

    def get_annotations_for_layer(self, layer_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query._DANNOTATION_LIST, (layer_id,))
            d = cursor.fetchone()
        return d

    def get_annotation_from_guid(self, guid):
        '''return self.connection.runQuery(
                query._DANNOTATION_GUID, (guid,)).addCallback(
                self._got_annotations).addCallback(self._get_single)'''

    def get_annotation_from_id(self, ann_id):
        '''return self.connection.runQuery(
                query._DANNOTATION_ID, (ann_id,)).addCallback(
                self._got_annotations).addCallback(self._get_single)'''

    def get_doc_owner_from_annotation(self, ann_id):
        '''return self.connection.runQuery(query._DOWN_ANN, (ann_id,)
                ).addCallback(self._got_user)'''

    def get_Doc_Keywords(self, docVersionGuid):
        with self.__get_cursor() as cursor:
            cursor.execute(query._GET_DOC_VERSION_KEYWORDS, (docVersionGuid,))
        return cursor.fetchone()

    def rm_annotation_by_guid(self, guid):
        with self.__get_cursor() as cursor:
            cursor.execute('DELETE FROM Annotation WHERE guid = %s;', (guid,))
        self.connection.commit()

    def add_annotation(
            self, layer_id, guid, page, position,
            fragment, created_by, is_hilight):
        with self.__get_cursor() as cursor:
            guid = guid.lower()
            cursor.execute(query._DANNOTATION_LIST, (layer_id,))
            d = cursor.fetchone()
            annotations_d = dict((x.guid.lower(), x) for x in d)
            if guid in annotations_d:
                annotation_id = annotations_d[guid]._id
                d = cursor.execute(
                    query.UPDATE_ANNOTATION,
                    (annotation_id, page, position, fragment,
                        created_by, is_hilight))
            else:
                d = cursor.execute(
                    query.INSERT_ANNOTATION,
                    (layer_id, guid, page, position,
                        fragment, created_by, is_hilight))
            d = cursor.fetchone()
            self.connection.commit()

    def add_comment(
            self, annotation_id, guid, comment, is_voice,
            s3_url, commented_by, layer_id=None):
        with self.__get_cursor() as cursor:
            updated_on = datetime.utcnow()
            if layer_id:
                annotation_id = None
            cmt = cursor.execute(
                query.ANNOTATION_COMMENT_GUID, (guid,))
            if cmt:  # Update
                c_id = cmt._id
                cursor.execute(
                    query.UPDATE_COMMENT,
                    (comment, commented_by, annotation_id,
                        is_voice, s3_url, updated_on, c_id, layer_id))
            else:  # Insert
                cursor.execute(
                    query.INSERT_COMMENT,
                    (guid, comment, commented_by,
                        annotation_id, is_voice, s3_url, layer_id))
            self.connection.commit()

    def _update_annotation(
            self, annotation_id, page, position,
            fragment, created_by, is_hilight):
        '''return self.connection.runQuery(query.UPDATE_ANNOTATION,
                (page, position, fragment,
                    created_by, is_hilight,
                    annotation_id)).addCallback(
                        self._got_annotations).addCallback(self._get_single)'''

    def _insert_annotation(
            self, layer_id, guid, page, position,
            fragment, created_by, is_hilight):
        '''return self.connection.runQuery(query.INSERT_ANNOTATION,
                (guid, layer_id, page,
                    position, fragment,
                    created_by, is_hilight)).addCallback(
                        self._got_annotations).addCallback(self._get_single)'''

    def _got_new_user(self, r):
        x = r
        if isinstance(r, list):
            x = r[0]
        return User(self, None, x.email, None, x.email)

    def _got_annotation_comments(self, r):
        l = []
        for x in r:
            l.append(Comment(
                self, x.id, x.guid, x.comment,
                x.commented_by, x.annotation_id,
                x.is_voice, x.s3_bucket, x.s3_key, x.s3_url))
        return l

    def get_annotationcomment_from_guid(self, guid):
        with self.__get_cursor() as cursor:
            cursor.execute(query.ANNOTATION_COMMENT_GUID, (guid,))
        return cursor.fetchone()

    def get_annotationcomment_from_id(self, ac_id):
        with self.__get_cursor() as cursor:
            cursor.execute(query.ANNOTATION_COMMENT_ID, (ac_id,))
        return cursor.fetchone()

    def get_annotationcomments_from_annotation_id(self, ann_id):
        '''return self.connection.runQuery(
                query.ANNOTATION_COMMENT_ANNOTATION_ID, (ann_id,)
                ).addCallback(self._got_annotation_comments)'''

    _DEVICE_TOKEN_ADD, _DEVICE_TOKEN_REMOVE = range(2)

    def _dt_count_returned(self, cnt, user_id, token, op):
        '''cnt = cnt[0].count
        if op == self._DEVICE_TOKEN_ADD:
            if cnt != 0:
                return False
            query = self._DEVICE_TOKEN_INSERT_QUERY
        elif op == self._DEVICE_TOKEN_REMOVE:
            if cnt == 0:
                return False
            query = self._DEVICE_TOKEN_REMOVE_QUERY
        else:
            raise RuntimeError("Invalid op: %s" % op)
        return self.connection.runOperation(query,
                (user_id, token)).addCallback(lambda x: True)'''

    '''def add_device_token(self, token, user):
        with self.__get_cursor() as cursor:
            if isinstance(user, User):
                user_id = user._id
            else:
                user_id = user
            cursor.execute(query._DEVICE_TOKEN_RM_BEFORE_ADD,
                    (user_id, token))
            cursor.execute(query._DEVICE_TOKEN_CHECK,
                    (user_id, token))
            cursor.execute(query._DEVICE_TOKEN_INSERT,
                    (user_id=user_id, token=token, is_apns))
        self.connection.commit()

    def remove_device_token(self, token, user=None):

        #If user is None, remove the token
        #Used to remove stale tokens
        with self.__get_cursor() as cursor:
        if user is None:
            cursor.execute(
                    query._DEVICE_TOKEN_REMOVE_1,
                    (token,)).addCallback(lambda x: True)

        if isinstance(user, User):
            user_id = user._id
        else:
            user_id = user
        return self.connection.runQuery(query._DEVICE_TOKEN_CHECK,
                (user_id, token)).addCallback(self._dt_count_returned,
                    user_id=user_id, token=token,
                    op=self._DEVICE_TOKEN_REMOVE)'''

    def _got_device_tokens(self, r):
        return set(x.device_token for x in r)

    def all_device_tokens(self, user):
        '''
        #Returns all device tokens for a user
        if isinstance(user, User):
            user_id = user._id
        else:
            user_id = user
        return self.connection.runQuery(query._DEVICE_TOKEN_ALL,
                (user_id,)).addCallback(self._got_device_tokens)'''

    def add_auth_token(self, person_id, auth_type, param_values):
        '''return self.connection.runOperation(query._INSERT_AUTH_TOKEN,
                (str(person_id), str(auth_type), str(param_values))
                ).addCallback(lambda x: True)'''

    def callProcedure(self, txn, user_id, longitude, latitude):
        txn.execute("SELECT set_person_geography(%s, %s, %s)",
                    (user_id, longitude, latitude))
        return txn.fetchall()

    def set_user_geograph(self, user_id, longitude, latitude):
            '''return self.connection.runInteraction(self.callProcedure,
                user_id, longitude, latitude).addCallback(lambda x: True)'''

    def _got_user_location(self, rows):
        if rows:
            return self._got_users_location(rows)[0]

    def _got_users_location(self, rows):
        l = []
        if rows:
            for row in rows:
                l.append(UserLocation(self, row.person_id, row.last_updated))
        return l

    def get_nearby_collaborators(
            self, user_id, longitude, latitude, distanceLimit):
        '''return self.connection.runQuery(query._GET_NEAR_BY_COLLABORATORS,
                    (user_id, user_id, user_id,
                     longitude, latitude, distanceLimit)).addCallback(
                             self._got_users_location)'''

    def callProc_getPersonsInVicinity(
            self, txn, user_id, longitude,
            latitude, distanceLimit):
        txn.execute("SELECT * from get_persons_in_vicinity(%s, %s, %s, %s)",
                    (user_id, longitude, latitude, distanceLimit))
        return txn.fetchall()

    def get_persons_in_vicinity(
            self, user_id, longitude,
            latitude, distanceLimit):
        ''' return self.connection.runInteraction(
            self.callProc_getPersonsInVicinity, user_id, longitude,
            latitude, distanceLimit).addCallback(self._got_users_location)'''

    def callProc_getPersonsNotinVicinity(
            self, txn, user_id, longitude,
            latitude, distanceLimit):
        txn.execute("SELECT * from get_persons_notin_vicinity(%s, %s, %s, %s)",
                    (user_id, longitude, latitude, distanceLimit))
        return txn.fetchall()

    def get_persons_notin_vicinity(
            self, user_id, longitude,
            latitude, distanceLimit):
        '''return self.connection.runInteraction(
            self.callProc_getPersonsNotinVicinity, user_id, longitude,
            latitude, distanceLimit).addCallback(self._got_users_location)'''

    '''
    FIXME : Verify This
    '''
    def create_my_feed_project(self, person_id, color):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._CREATE_MY_FEED,
                (str(person_id), 'My Feed', color))
            self.connection.commit()
            x = cursor.fetchone()
            return Project(self, _id = x[0], guid = x[1], owner_id = x[2], project_name =  x[3], isglobal = x[4], created_on = x[5])

    def get_project_by_id(self, project_id):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._GET_PROJECT_BY_ID,
                (project_id,))
            self.connection.commit()
            x = cursor.fetchone()
            return Project(self, x[0], x[1], x[2], x[3])

    def add_email(self, person_id, email):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._INSERT_NEW_MAIL_ID, (person_id, email.lower()))
            self.connection.commit()

    def update_collaborator(self, person_id, email):
        '''return self.connection.runOperation(
                query._UPDATE_COLLABORATOR, (person_id, email.lower()))'''

    def list_user_projects(self, user_id):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._LIST_USER_PROJECTS,
                (user_id, user_id))
            self.connection.commit()
            x = cursor.fetchone()
            return Project(self, x[0], x[1], x[2], x[3])

    def got_collaborators(self, rows, user_id):
        c = []
        for r in rows:
            if r.user_id != user_id:
                c = [r.display_name]
        return c

    def get_collabs_in_layers(self, user_id):
        with self.__get_cursor() as cursor:
            cursor.execute(
                query._COLLABORATORS_IN_LAYERS,
                (user_id, user_id, user_id))
            self.connection.commit()
            x = cursor.fetchone()
            return x

    def add_reserved_username(self, user_name):
        with self.__get_cursor() as cursor:
            try:
                cursor.execute(
                    query._ADD_RESERVED_USERNAME,
                    (user_name,))
                self.connection.commit()
            except:
                print '%s already in reserved list' % (user_name,)

    def add_to_graph_queue(self, data, url, deletion):
        with self.__get_cursor() as cursor:
            cursor.execute(
               query._ADD_TO_GRAPH_QUEUE,
               (data, url, deletion))
            self.connection.commit()
            x = cursor.fetchone()
            return x[0]
