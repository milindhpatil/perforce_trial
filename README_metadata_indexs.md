### PostgreSQL CREATE INDEX Statements

Based on the P4 Server Schema Documentation (2025.1), I've generated `CREATE INDEX` statements for various tables. These focus on:

- **Primary indexes**: Already handled as PRIMARY KEY in the CREATE TABLE statements (based on "Indexed on" fields).
- **Secondary indexes**: For fields commonly used in queries (e.g., `user`, `change`, `client`, `date`, `depotFile` where not part of PK). Inferred from table descriptions, field types, and relationships (e.g., foreign key-like fields to `db.change.change`, `db.user.user`).
- **Explicit secondary tables**: Tables like `db.changeidx` and `db.revcx` are indexes themselves, so no additional indexes needed beyond their PK.
- **Selection**: Focused on "various" key tables (e.g., changelists, revisions, users, domains) for brevity. Indexes are non-unique unless specified. Use B-tree for general use; adjust for GIN/GiST if text search needed.

Run these after CREATE TABLE. Consider partial indexes for status='pending' etc., if query patterns are known.

```sql
-- Indexes for db.change (Changelists) - Secondary on user, client, status, stream, date
CREATE INDEX idx_db_change_user ON db.change (user);
CREATE INDEX idx_db_change_client ON db.change (client);
CREATE INDEX idx_db_change_status ON db.change (status);
CREATE INDEX idx_db_change_stream ON db.change (stream);
CREATE INDEX idx_db_change_date ON db.change (date);

-- Indexes for db.changex (Pending changelists) - Mirror db.change
CREATE INDEX idx_db_changex_user ON db.changex (user);
CREATE INDEX idx_db_changex_client ON db.changex (client);
CREATE INDEX idx_db_changex_status ON db.changex (status);
CREATE INDEX idx_db_changex_stream ON db.changex (stream);
CREATE INDEX idx_db_changex_date ON db.changex (date);

-- Indexes for db.rev (Revision records) - Secondary on change, action, type (db.revcx handles change+depotFile)
CREATE INDEX idx_db_rev_change ON db.rev (change);
CREATE INDEX idx_db_rev_action ON db.rev (action);
CREATE INDEX idx_db_rev_type ON db.rev (type);
CREATE INDEX idx_db_rev_date ON db.rev (date);

-- Indexes for db.rev* variants (e.g., archived, deleted, shelved) - Mirror db.rev where applicable
CREATE INDEX idx_db_revbx_change ON db.revbx (change);
CREATE INDEX idx_db_revbx_action ON db.revbx (action);
CREATE INDEX idx_db_revdx_change ON db.revdx (change);
CREATE INDEX idx_db_revhx_change ON db.revhx (change);
CREATE INDEX idx_db_revpx_change ON db.revpx (change);
CREATE INDEX idx_db_revsh_change ON db.revsh (change);
CREATE INDEX idx_db_revstg_change ON db.revstg (change);
CREATE INDEX idx_db_revsx_change ON db.revsx (change);
CREATE INDEX idx_db_revtr_change ON db.revtr (change);
CREATE INDEX idx_db_revtx_change ON db.revtx (change);
CREATE INDEX idx_db_revux_change ON db.revux (change);

-- Indexes for db.user (User specifications) - Secondary on type, auth, updateDate
CREATE INDEX idx_db_user_type ON db.user (type);
CREATE INDEX idx_db_user_auth ON db.user (auth);
CREATE INDEX idx_db_user_update_date ON db.user (updateDate);

-- Indexes for db.domain (Domains: depots, clients, etc.) - Secondary on type, owner, updateDate
CREATE INDEX idx_db_domain_type ON db.domain (type);
CREATE INDEX idx_db_domain_owner ON db.domain (owner);
CREATE INDEX idx_db_domain_update_date ON db.domain (updateDate);

-- Indexes for db.depot (Depot specifications) - Secondary on type
CREATE INDEX idx_db_depot_type ON db.depot (type);

-- Indexes for db.group (Group specifications) - Secondary on type
CREATE INDEX idx_db_group_type ON db.group (type);

-- Indexes for db.have (Have-list for clients) - Secondary on depotFile, type, time
CREATE INDEX idx_db_have_depot_file ON db.have (depotFile);
CREATE INDEX idx_db_have_type ON db.have (type);
CREATE INDEX idx_db_have_time ON db.have (time);

-- Mirror for replica/partitioned variants
CREATE INDEX idx_db_have_pt_depot_file ON db.have_pt (depotFile);
CREATE INDEX idx_db_have_rp_depot_file ON db.have_rp (depotFile);
CREATE INDEX idx_db_haveg_depot_file ON db.haveg (depotFile);

-- Indexes for db.resolve (Pending integration records) - Secondary on how, state
CREATE INDEX idx_db_resolve_how ON db.resolve (how);
CREATE INDEX idx_db_resolve_state ON db.resolve (state);

-- Mirror for variants
CREATE INDEX idx_db_resolvex_how ON db.resolvex (how);
CREATE INDEX idx_db_resolvex_state ON db.resolvex (state);
CREATE INDEX idx_db_resolveg_how ON db.resolveg (how);
CREATE INDEX idx_db_resolveg_state ON db.resolveg (state);

-- Indexes for db.working (Work in progress) - Secondary on depotFile, client, user, change, action
CREATE INDEX idx_db_working_depot_file ON db.working (depotFile);
CREATE INDEX idx_db_working_client ON db.working (client);
CREATE INDEX idx_db_working_user ON db.working (user);
CREATE INDEX idx_db_working_change ON db.working (change);
CREATE INDEX idx_db_working_action ON db.working (action);

-- Mirror for variants
CREATE INDEX idx_db_workingx_depot_file ON db.workingx (depotFile);
CREATE INDEX idx_db_workingg_depot_file ON db.workingg (depotFile);

-- Indexes for db.locks (Locked files) - Secondary on user, action, change
CREATE INDEX idx_db_locks_user ON db.locks (user);
CREATE INDEX idx_db_locks_action ON db.locks (action);
CREATE INDEX idx_db_locks_change ON db.locks (change);

-- Mirror for graph
CREATE INDEX idx_db_locksg_user ON db.locksg (user);

-- Indexes for db.fix (Fix records) - Secondary on change, status, user (db.fixrev handles change+job)
CREATE INDEX idx_db_fix_status ON db.fix (status);
CREATE INDEX idx_db_fix_user ON db.fix (user);
CREATE INDEX idx_db_fix_date ON db.fix (date);

-- Indexes for db.label (Label revisions) - Secondary on haveRev
CREATE INDEX idx_db_label_have_rev ON db.label (haveRev);

-- Indexes for db.review (User review mappings) - Secondary on depotFile, type
CREATE INDEX idx_db_review_depot_file ON db.review (depotFile);
CREATE INDEX idx_db_review_type ON db.review (type);

-- Indexes for db.property (Properties) - Secondary on type, scope, user, date
CREATE INDEX idx_db_property_type ON db.property (type);
CREATE INDEX idx_db_property_scope ON db.property (scope);
CREATE INDEX idx_db_property_user ON db.property (user);
CREATE INDEX idx_db_property_date ON db.property (date);

-- Indexes for db.protect (Protections) - Secondary on user, host, perm, depotFile
CREATE INDEX idx_db_protect_user ON db.protect (user);
CREATE INDEX idx_db_protect_host ON db.protect (host);
CREATE INDEX idx_db_protect_perm ON db.protect (perm);
CREATE INDEX idx_db_protect_depot_file ON db.protect (depotFile);

-- Indexes for db.job (Job records) - Secondary on xstatus, xdate
CREATE INDEX idx_db_job_xstatus ON db.job (xstatus);
CREATE INDEX idx_db_job_xdate ON db.job (xdate);

-- Indexes for db.stream (Stream specifications) - Secondary on parent, type, status
CREATE INDEX idx_db_stream_parent ON db.stream (parent);
CREATE INDEX idx_db_stream_type ON db.stream (type);
CREATE INDEX idx_db_stream_status ON db.stream (status);

-- Indexes for db.remote (Remote specifications) - Secondary on owner, update, access
CREATE INDEX idx_db_remote_owner ON db.remote (owner);
CREATE INDEX idx_db_remote_update ON db.remote (update);
CREATE INDEX idx_db_remote_access ON db.remote (access);

-- Indexes for db.repo (Repository specifications) - Secondary on owner, created
CREATE INDEX idx_db_repo_owner ON db.repo (owner);
CREATE INDEX idx_db_repo_created ON db.repo (created);

-- Indexes for db.config (Server configurations) - Secondary on value (if queried)
CREATE INDEX idx_db_config_value ON db.config (value);

-- Indexes for db.counters (Counters) - Secondary on value
CREATE INDEX idx_db_counters_value ON db.counters (value);

-- Indexes for db.monitor (Server processes) - Secondary on user, startDate, runstate
CREATE INDEX idx_db_monitor_user ON db.monitor (user);
CREATE INDEX idx_db_monitor_start_date ON db.monitor (startDate);
CREATE INDEX idx_db_monitor_runstate ON db.monitor (runstate);
```

### Notes
- **Rationale**: Indexes target high-cardinality fields (e.g., `user`, `change`) for JOINs/WHERE clauses. Avoided over-indexing (e.g., no index on low-cardinality `type` unless specified). For text fields like `description`, consider GIN for full-text search if needed: `CREATE INDEX ... USING GIN (to_tsvector('english', description));`.
- **Performance**: Monitor with `EXPLAIN ANALYZE` in production. Drop unused indexes to save space.
- **Coverage**: Covers ~20 key tables; extend for others (e.g., `db.bod*` on `text` for search). If you need indexes for specific tables or full-text, provide details!
