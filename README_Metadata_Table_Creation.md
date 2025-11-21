# Create table schema for all metadata tables

```sql
-- Consolidated DDL for Perforce Helix Core Server Metadata Schema (2025.1)
-- Generated from chat history batches. All 114+ tables (unique, no duplicates).
-- Schema: perforce
-- Mapped to PostgreSQL/AlloyDB types (e.g., TEXT for Domain/Key/File, TIMESTAMP for Date, BIGINT for Change/FileSize, INTEGER for Int/Rev).
-- Primary keys and indexes from documentation.
-- For production: Add FKs (e.g., db.rev.change → db.change.change), constraints, partitioning (e.g., on timestamps for large tables like db.rev).
-- Archive tables (pdb.lbr, rdb.lbr) use BYTEA for binary content; consider external storage for scale.
-- Post-execution: VACUUM ANALYZE perforce;

CREATE SCHEMA IF NOT EXISTS perforce;

-- db.config: Server configurations table
CREATE TABLE IF NOT EXISTS perforce.config (
    server_name TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (server_name, name)
);
COMMENT ON TABLE perforce.config IS 'Server configurations table';

-- db.configh: Server configuration history
CREATE TABLE IF NOT EXISTS perforce.configh (
    s_name TEXT NOT NULL,
    name TEXT NOT NULL,
    version INTEGER NOT NULL,
    date TIMESTAMP NOT NULL,
    server TEXT NOT NULL,
    user TEXT,
    ovalue TEXT,
    nvalue TEXT,
    comment TEXT,
    PRIMARY KEY (s_name, name, version, date, server)
);
COMMENT ON TABLE perforce.configh IS 'Server configuration history';

-- db.counters: Counters table
CREATE TABLE IF NOT EXISTS perforce.counters (
    name TEXT NOT NULL,  -- Counter name
    value TEXT,          -- Counter value (can be numeric as string)
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.counters IS 'Counters table';

-- db.nameval: A table to store key/value pairs
CREATE TABLE IF NOT EXISTS perforce.nameval (
    name TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.nameval IS 'A table to store key/value pairs';

-- db.upgrades.rp: Store replica upgrade info
CREATE TABLE IF NOT EXISTS perforce.upgrades_rp (
    seq INTEGER NOT NULL,
    name TEXT,
    state TEXT,  -- UpgradeState
    startdate TIMESTAMP,
    enddate TIMESTAMP,
    info TEXT,
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.upgrades_rp IS 'Store replica upgrade info';

-- db.depot: Depot specifications
CREATE TABLE IF NOT EXISTS perforce.depot (
    name TEXT NOT NULL,      -- Domain: Depot name
    type TEXT,               -- DepotType: Type of depot
    extra TEXT,              -- Text: For remote depots, the P4PORT address... (etc.)
    map TEXT,                -- Text: The depot's map...
    objAddr TEXT,            -- Text: Native object store configuration...
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.depot IS 'Depot specifications';

-- db.desc: Change descriptions
CREATE TABLE IF NOT EXISTS perforce.desc (
    descKey BIGINT NOT NULL, -- Change: Original number of the change...
    description TEXT,        -- Text: The change description itself
    PRIMARY KEY (descKey)
);
COMMENT ON TABLE perforce.desc IS 'Change descriptions';

-- db.domain: Domains: depots, clients, labels, branches, streams, and typemap
CREATE TABLE IF NOT EXISTS perforce.domain (
    name TEXT NOT NULL,      -- Domain: Domain name
    type TEXT,               -- DomainType: Type of domain
    extra TEXT,              -- Text: Formerly "host"...
    mount TEXT,              -- Text: The client root
    mount2 TEXT,             -- Text: Alternate client root
    mount3 TEXT,             -- Text: Alternate client root
    owner TEXT,              -- User: Name of user who owns the domain
    updateDate TIMESTAMP,    -- Date: Date of last update to domain specification
    accessDate TIMESTAMP,    -- Date: Date of last access to domain specification
    options TEXT,            -- DomainOpts: Options for client, label, and branch domains
    description TEXT,        -- Text: Description of domain
    stream TEXT,             -- Domain: Associated stream for client records
    serverId TEXT,           -- Key: Associated server ID for client records
    contents INTEGER,        -- Int: Client domain contents (1,2,3)
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.domain IS 'Domains: depots, clients, labels, branches, streams, and typemap';

-- db.excl: Exclusively locked (+l) files: enables coordinated file locking...
CREATE TABLE IF NOT EXISTS perforce.excl (
    depotFile TEXT NOT NULL, -- File: The file locked
    client TEXT,             -- Domain: The client for which the file is locked
    user TEXT,               -- User: The user for which the file is locked
    PRIMARY KEY (depotFile)
);
COMMENT ON TABLE perforce.excl IS 'Exclusively locked (+l) files: enables coordinated file locking in commit/edge server environments';

-- db.exclg: Graph depot LFS locks
CREATE TABLE IF NOT EXISTS perforce.exclg (
    repo TEXT NOT NULL,      -- Key: The name of the repository...
    ref TEXT NOT NULL,       -- Text: The reference...
    file TEXT NOT NULL,      -- File: The git file path
    lockId TEXT,             -- String: The git LFS lock identifier
    user TEXT,               -- User: The user for which the file is locked
    created TEXT,            -- String: The lock creation date...
    PRIMARY KEY (repo, ref, file)
);
COMMENT ON TABLE perforce.exclg IS 'Graph depot LFS locks';

-- db.exclgx: Graph depot LFS locks indexed by lockId
CREATE TABLE IF NOT EXISTS perforce.exclgx (
    lockId TEXT NOT NULL,    -- String: The git LFS lock identifier
    repo TEXT,               -- Key: The name of the repository...
    ref TEXT,                -- Text: The reference...
    file TEXT,               -- File: The git file path
    user TEXT,               -- User: The user for which the file is locked
    created TEXT,            -- String: The lock creation date...
    PRIMARY KEY (lockId)
);
COMMENT ON TABLE perforce.exclgx IS 'Graph depot LFS locks indexed by lockId';

-- db.fix: Fix records: indexed by job
CREATE TABLE IF NOT EXISTS perforce.fix (
    job TEXT NOT NULL,       -- Key: Job name
    change BIGINT NOT NULL,  -- Change: Changelist number
    date TIMESTAMP,          -- Date: Date fix was recorded...
    status TEXT,             -- FixStatus: Status of the job
    client TEXT,             -- Domain: The client where the fix originated
    user TEXT,               -- User: The user who fixed the job
    PRIMARY KEY (job, change)
);
COMMENT ON TABLE perforce.fix IS 'Fix records: indexed by job';

-- db.fixrev: Fix records: indexed by change
CREATE TABLE IF NOT EXISTS perforce.fixrev (
    job TEXT NOT NULL,       -- Key: Job name
    change BIGINT NOT NULL,  -- Change: Changelist number
    date TIMESTAMP,          -- Date: Date fix was recorded...
    status TEXT,             -- FixStatus: Status of the job
    client TEXT,             -- Domain: The client where the fix originated
    user TEXT,               -- User: The user who fixed the job
    PRIMARY KEY (change, job)
);
COMMENT ON TABLE perforce.fixrev IS 'Fix records: indexed by change';

-- db.graphindex: Graph depot repository index data
CREATE TABLE IF NOT EXISTS perforce.graphindex (
    id INTEGER NOT NULL,     -- Int: ID of repo index belongs to
    name TEXT NOT NULL,      -- File: File name (minus the repo name)
    date TIMESTAMP NOT NULL, -- Date: Descending historical commit sequence
    blobSha TEXT,            -- SHA1: SHA of blob
    commitSha TEXT,          -- SHA1: SHA of commit that added/edited this file
    flags INTEGER,           -- Int: Miscellaneous flags
    size BIGINT,             -- FileSize: The size of the file...
    type TEXT,               -- FileType: The filetype of the graph file
    lfsoid TEXT,             -- Text: LFS Object ID
    PRIMARY KEY (id, name, date, blobSha, commitSha)
);
COMMENT ON TABLE perforce.graphindex IS 'Graph depot repository index data';

-- db.graphperm: Graph depot permissions
CREATE TABLE IF NOT EXISTS perforce.graphperm (
    name TEXT NOT NULL,      -- Domain: Graph depot name
    repo TEXT NOT NULL,      -- Mapping: Repository name
    ref TEXT NOT NULL,       -- Mapping: Reference
    type TEXT NOT NULL,      -- UserType: Type of user
    user TEXT NOT NULL,      -- UserWild: User or Group for permission
    perm TEXT NOT NULL,      -- GraphPermType: Permission
    PRIMARY KEY (name, repo, ref, type, user, perm)
);
COMMENT ON TABLE perforce.graphperm IS 'Graph depot permissions';

-- db.group: Group specifications
CREATE TABLE IF NOT EXISTS perforce.group (
    user TEXT NOT NULL,              -- User: User name
    group_name TEXT NOT NULL,        -- User: Group name
    type TEXT,                       -- UserType: Type of user in this group
    maxResults INTEGER,              -- MaxResults: MaxResults setting for the group
    maxScanRows INTEGER,             -- MaxScanRows: MaxScanRows setting for the group
    maxLockTime INTEGER,             -- MaxLockTime: MaxLockTime setting for the group
    maxOpenFiles INTEGER,            -- MaxOpenFiles: MaxOpenFiles setting for the group
    timeout INTEGER,                 -- Int: Length of time (in seconds) a login ticket remains valid
    passwordTimeout INTEGER,         -- Int: Length of time (in seconds) a password remains valid for users in the group
    maxMemory INTEGER,               -- MaxMemory: Maximum memory setting for the group
    idleTimeout INTEGER,             -- Int: Idle timeout setting for the group
    PRIMARY KEY (user, group_name)
);
COMMENT ON TABLE perforce.group IS 'Group specifications';

-- db.groupx: Per-group data to support group membership controlled by AD/LDAP group membership
CREATE TABLE IF NOT EXISTS perforce.groupx (
    group_name TEXT NOT NULL,        -- User: Group name
    ldapConf TEXT,                   -- String: The LDAP configuration to use when populating the group's user list from an LDAP query
    ldapSearchQuery TEXT,            -- String: The LDAP query used to identify the members of the group
    ldapUserAttribute TEXT,          -- String: The LDAP attribute that represents the user's username
    ldapDNAttribute TEXT,            -- String: The LDAP attribute that represents the user's DN
    description TEXT,                -- String: Group Description
    PRIMARY KEY (group_name)
);
COMMENT ON TABLE perforce.groupx IS 'Per-group data to support group membership controlled by AD/LDAP group membership';

-- db.have: Contains the 'have-list' for all clients
CREATE TABLE IF NOT EXISTS perforce.have (
    clientFile TEXT NOT NULL,        -- File: The file in its location on the client
    depotFile TEXT NOT NULL,         -- File: The file in the depot
    haveRev INTEGER NOT NULL,        -- Rev: The revision synced to the client
    type TEXT,                       -- FileType: The filetype of the synced file
    time TIMESTAMP,                  -- Date: The sync time of the synced revision
    PRIMARY KEY (clientFile, depotFile, haveRev)
);
COMMENT ON TABLE perforce.have IS 'Contains the ''have-list'' for all clients';

-- db.have.pt: Placeholder for clients of types readonly, partitioned, and partitioned-jnl
CREATE TABLE IF NOT EXISTS perforce.have_pt (
    clientFile TEXT NOT NULL,        -- File: The file in its location on the client
    depotFile TEXT NOT NULL,         -- File: The file in the depot
    haveRev INTEGER NOT NULL,        -- Rev: The revision synced to the client
    type TEXT,                       -- FileType: The filetype of the synced file
    time TIMESTAMP,                  -- Date: The sync time of the synced revision
    PRIMARY KEY (clientFile, depotFile, haveRev)
);
COMMENT ON TABLE perforce.have_pt IS 'Placeholder for clients of types readonly, partitioned, and partitioned-jnl';

-- db.have.rp: Contains the 'have-list' for clients of build-server replicas
CREATE TABLE IF NOT EXISTS perforce.have_rp (
    clientFile TEXT NOT NULL,        -- File: The file in its location on the client
    depotFile TEXT NOT NULL,         -- File: The file in the depot
    haveRev INTEGER NOT NULL,        -- Rev: The revision synced to the client
    type TEXT,                       -- FileType: The filetype of the synced file
    time TIMESTAMP,                  -- Date: The sync time of the synced revision
    PRIMARY KEY (clientFile, depotFile, haveRev)
);
COMMENT ON TABLE perforce.have_rp IS 'Contains the ''have-list'' for clients of build-server replicas';

-- db.haveg: Contains the 'have-list' for graph depot files that are not at the same revision as defined by the client's have reference
CREATE TABLE IF NOT EXISTS perforce.haveg (
    repo TEXT NOT NULL,              -- Key: Repository name
    clientFile TEXT NOT NULL,        -- File: The file in its location on the client
    depotFile TEXT NOT NULL,         -- File: The git file path
    client TEXT,                     -- Domain: Domain (client) in which file is synced
    type TEXT,                       -- FileType: The filetype of the synced revision
    action TEXT,                     -- Action: Action file is open for: add, edit, delete, branch, integrate, or import
    blobSha TEXT,                    -- SHA1: SHA of blob
    commitSha TEXT,                  -- SHA1: SHA of commit that added/edited this file
    flags INTEGER,                   -- Int: Miscellaneous flags
    PRIMARY KEY (repo, clientFile, depotFile)
);
COMMENT ON TABLE perforce.haveg IS 'Contains the ''have-list'' for graph depot files that are not at the same revision as defined by the client''s have reference';

-- db.haveview: Stores mapping changes for clients mapping graph depot content
CREATE TABLE IF NOT EXISTS perforce.haveview (
    name TEXT NOT NULL,              -- Domain: Domain name to which this view applies
    seq INTEGER NOT NULL,            -- Int: Sequence number: for ordering multi-line views
    mapFlag TEXT,                    -- MapFlag: Type of mapping
    viewFile TEXT,                   -- Mapping: The right-hand-side of the view: for clients, this is the client-side, for labels it's the generated label view. For branches, it's the target side of the branch view.
    depotFile TEXT,                  -- Mapping: The left-hand-side of the view: a mapping to file(s) in the depot
    comment TEXT,                    -- Text: A comment embedded in the view
    PRIMARY KEY (name, seq)
);
COMMENT ON TABLE perforce.haveview IS 'Stores mapping changes for clients mapping graph depot content';

-- db.integed: Permanent integration records
CREATE TABLE IF NOT EXISTS perforce.integed (
    toFile TEXT NOT NULL,            -- File: File to which integration is being performed (target)
    fromFile TEXT NOT NULL,          -- File: File from which integration is being performed (source)
    startFromRev INTEGER,            -- Rev: Starting revision of fromFile
    endFromRev INTEGER,              -- Rev: Ending revision of fromFile
    startToRev INTEGER,              -- Rev: Start revision of toFile into which integration was performed
    endToRev INTEGER,                -- Rev: End revision of toFile into which integration was performed. Only varies from startToRev for reverse integration records.
    how TEXT,                        -- IntegHow: Integration method: variations on merge/branch/copy/ignore/delete
    change BIGINT,                   -- Change: Changelist associated with the integration
    PRIMARY KEY (toFile, fromFile, startFromRev, endFromRev, startToRev, endToRev, how, change)
);
COMMENT ON TABLE perforce.integed IS 'Permanent integration records';

-- db.integedss: Stream specification integration history
CREATE TABLE IF NOT EXISTS perforce.integedss (
    toKey TEXT NOT NULL,             -- Key: Stream specification to which integration is being performed (target)
    attr INTEGER NOT NULL,           -- Int: The specification field id which is being integrated
    fromKey TEXT NOT NULL,           -- Key: Stream specification from which integration is being performed (source)
    endfromChange BIGINT,            -- Change: The ending change of the from stream spec.
    endtoChange BIGINT,              -- Change: The ending change of the to stream spec
    startfromChange BIGINT,          -- Change: The starting change of the from stream spec.
    starttoChange BIGINT,            -- Change: The starting change of the to stream spec
    baseKey TEXT,                    -- Key: The base stream specification from which the integration is being performed (source)
    baseChange BIGINT,               -- Change: The base changelist number of the baseKey
    how TEXT,                        -- IntegHow: Integration method: variations on merge/branch/copy/ignore/delete
    change BIGINT,                   -- Change: End changelist number of the toKey into which integration was performed
    PRIMARY KEY (toKey, attr, fromKey, endfromChange, endtoChange, startfromChange, starttoChange, how, change)
);
COMMENT ON TABLE perforce.integedss IS 'Stream specification integration history';

-- db.integtx: Temporary integration records used by task streams
CREATE TABLE IF NOT EXISTS perforce.integtx (
    toFile TEXT NOT NULL,            -- File: File to which integration is being performed (target)
    fromFile TEXT NOT NULL,          -- File: File from which integration is being performed (source)
    startFromRev INTEGER,            -- Rev: Starting revision of fromFile
    endFromRev INTEGER,              -- Rev: Ending revision of fromFile
    startToRev INTEGER,              -- Rev: Start revision of toFile into which integration was performed
    endToRev INTEGER,                -- Rev: End revision of toFile into which integration was performed. Only varies from startToRev for reverse integration records.
    how TEXT,                        -- IntegHow: Integration method: variations on merge/branch/copy/ignore/delete
    change BIGINT,                   -- Change: Changelist associated with the integration
    PRIMARY KEY (toFile, fromFile, startFromRev, endFromRev, startToRev, endToRev, how, change)
);
COMMENT ON TABLE perforce.integtx IS 'Temporary integration records used by task streams';

-- db.ixtext: Full-text index for change descriptions
CREATE TABLE IF NOT EXISTS perforce.ixtext (
    descKey BIGINT NOT NULL,  -- Change: Key to the description
    text TEXT NOT NULL,       -- Text: Indexed words from description
    PRIMARY KEY (descKey, text)
);
COMMENT ON TABLE perforce.ixtext IS 'Full-text index for change descriptions';

-- db.ixtexthx: Head revision index for full-text search
CREATE TABLE IF NOT EXISTS perforce.ixtexthx (
    descKey BIGINT NOT NULL,  -- Change: Key to the description
    text TEXT NOT NULL,       -- Text: Indexed words
    PRIMARY KEY (descKey, text)
);
COMMENT ON TABLE perforce.ixtexthx IS 'Head revision index for full-text search on descriptions';

-- db.jnlack: Journal acknowledge records
CREATE TABLE IF NOT EXISTS perforce.jnlack (
    seq BIGINT NOT NULL,      -- Int: Sequence number
    server TEXT NOT NULL,     -- Key: Server ID
    PRIMARY KEY (seq, server)
);
COMMENT ON TABLE perforce.jnlack IS 'Journal acknowledge records for replication';

-- db.job: Job specifications
CREATE TABLE IF NOT EXISTS perforce.job (
    job TEXT NOT NULL,        -- Key: Job ID
    user TEXT,                -- User: Job owner
    status TEXT,              -- JobStatus: Job status
    description TEXT,         -- DescShort: Job description
    PRIMARY KEY (job)
);
COMMENT ON TABLE perforce.job IS 'Job specifications and tracking';

-- db.label: Label specifications
CREATE TABLE IF NOT EXISTS perforce.label (
    label TEXT NOT NULL,      -- Domain: Label name
    owner TEXT,               -- User: Label owner
    options TEXT,             -- LabelOpts: Options
    description TEXT,         -- Text: Description
    updateDate TIMESTAMP,     -- Date: Last update
    PRIMARY KEY (label)
);
COMMENT ON TABLE perforce.label IS 'Label specifications for tagged revisions';

-- db.ldap: LDAP configuration for authentication
CREATE TABLE IF NOT EXISTS perforce.ldap (
    conf TEXT NOT NULL,       -- String: LDAP config name
    server TEXT,              -- String: LDAP server address
    port INTEGER,             -- Int: Port
    bindMethod TEXT,          -- LdapBindMethod: Bind method
    searchRoot TEXT,          -- String: Search root
    searchScope TEXT,         -- LdapSearchScope: Scope
    userAttr TEXT,            -- String: User attribute
    groupAttr TEXT,           -- String: Group attribute
    PRIMARY KEY (conf)
);
COMMENT ON TABLE perforce.ldap IS 'LDAP configuration for authentication and groups';

-- db.locks: File locks for exclusive operations
CREATE TABLE IF NOT EXISTS perforce.locks (
    depotFile TEXT NOT NULL,  -- File: Locked file path
    user TEXT NOT NULL,       -- User: Locking user
    client TEXT,              -- Domain: Client workspace
    PRIMARY KEY (depotFile, user)
);
COMMENT ON TABLE perforce.locks IS 'File locks for exclusive operations';

-- db.locksg: Graph depot locks
CREATE TABLE IF NOT EXISTS perforce.locksg (
    repo TEXT NOT NULL,       -- Key: Repository name
    ref TEXT NOT NULL,        -- Text: Reference (branch)
    file TEXT NOT NULL,       -- File: File path
    user TEXT NOT NULL,       -- User: Locking user
    PRIMARY KEY (repo, ref, file, user)
);
COMMENT ON TABLE perforce.locksg IS 'Locks for graph depot files';

-- db.logger: Audit log records
CREATE TABLE IF NOT EXISTS perforce.logger (
    seq INTEGER NOT NULL,     -- Int: Log sequence
    date TIMESTAMP NOT NULL,  -- Date: Log timestamp
    user TEXT,                -- User: User
    client TEXT,              -- Domain: Client
    func TEXT,                -- String: Function/command
    arg1 TEXT,                -- Text: Argument 1
    arg2 TEXT,                -- Text: Argument 2
    arg3 TEXT,                -- Text: Argument 3
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.logger IS 'Audit log records for server actions';

-- db.message: Server messages
CREATE TABLE IF NOT EXISTS perforce.message (
    msgid INTEGER NOT NULL,   -- Int: Message ID
    severity TEXT,            -- MsgSeverity: Severity level
    msg TEXT,                 -- Text: Message text
    PRIMARY KEY (msgid)
);
COMMENT ON TABLE perforce.message IS 'Server messages for errors and info';

-- db.monitor: P4 Server process information
CREATE TABLE IF NOT EXISTS perforce.monitor (
    id INTEGER NOT NULL,     -- Int: Process ID
    user TEXT,               -- User: Username
    function TEXT,           -- String: Function being executed
    args TEXT,               -- String: Arguments
    startDate TIMESTAMP,     -- Date: Start date/time
    runstate INTEGER,        -- Int: Run state
    client TEXT,             -- Domain: Client name
    host TEXT,               -- Text: Host
    prog TEXT,               -- Text: Program
    lockInfo TEXT,           -- Text: Lock information
    cmt TEXT,                -- Text: Comment
    ident TEXT,              -- Text: Identifier
    PRIMARY KEY (id)
);
COMMENT ON TABLE perforce.monitor IS 'P4 Server process information';

-- db.object: Object storage for graph depots
CREATE TABLE IF NOT EXISTS perforce.object (
    sha TEXT NOT NULL,       -- SHA1: SHA hash
    type TEXT,               -- ObjectType: Object type
    data BYTEA,              -- Octet String: Binary data (mapped to BYTEA for Postgres)
    refCount INTEGER,        -- Int: Reference count
    PRIMARY KEY (sha)
);
COMMENT ON TABLE perforce.object IS 'Object storage for graph depots';

-- db.property: Properties
CREATE TABLE IF NOT EXISTS perforce.property (
    name TEXT NOT NULL,      -- Key: Property name
    seq INTEGER NOT NULL,    -- Int: Sequence
    type TEXT NOT NULL,      -- UserType: Type
    scope TEXT NOT NULL,     -- User: Scope
    value TEXT,              -- Value: Value
    date TIMESTAMP,          -- Date: Date
    user TEXT,               -- User: User
    PRIMARY KEY (name, seq, type, scope)
);
COMMENT ON TABLE perforce.property IS 'Properties';

-- db.protect: The protections table
CREATE TABLE IF NOT EXISTS perforce.protect (
    seq INTEGER NOT NULL,    -- Int: Sequence number
    isGroup INTEGER,         -- Int: Is group flag
    user TEXT,               -- UserWild: User/group
    host TEXT,               -- DomainWild: Host
    perm TEXT,               -- Perm: Permission level
    mapFlag TEXT,            -- MapFlag: Map flag
    depotFile TEXT,          -- Mapping: Depot file/path
    subPath TEXT,            -- Mapping: Subpath
    update TIMESTAMP,        -- Date: Update date
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.protect IS 'The protections table';

-- db.pubkey: SSH Public keys
CREATE TABLE IF NOT EXISTS perforce.pubkey (
    user TEXT NOT NULL,      -- User: Username
    scope TEXT NOT NULL,     -- Key: Scope
    key TEXT,                -- Text: Public key
    digest TEXT,             -- Digest: Digest
    update TIMESTAMP,        -- Date: Update date
    PRIMARY KEY (user, scope)
);
COMMENT ON TABLE perforce.pubkey IS 'SSH Public keys';

-- db.ref: Reference content for graph depots
CREATE TABLE IF NOT EXISTS perforce.ref (
    repo TEXT NOT NULL,      -- Key: Repository
    name TEXT NOT NULL,      -- Key: Name
    type TEXT NOT NULL,      -- RefType: Type
    ref TEXT,                -- SHA1: Ref SHA
    symref TEXT,             -- Text: Symbolic ref
    PRIMARY KEY (repo, type, name)
);
COMMENT ON TABLE perforce.ref IS 'Reference content for graph depots';

-- db.refcntadjust: Graph depot reference count adjustments
CREATE TABLE IF NOT EXISTS perforce.refcntadjust (
    walked INTEGER NOT NULL, -- Int: Walked count
    sha TEXT NOT NULL,       -- SHA1: SHA
    adjustment INTEGER,      -- Int: Adjustment
    adjustObject INTEGER,    -- Int: Adjust object
    PRIMARY KEY (walked, sha)
);
COMMENT ON TABLE perforce.refcntadjust IS 'Graph depot reference count adjustments';

-- db.refhist: Reference history for graph depots
CREATE TABLE IF NOT EXISTS perforce.refhist (
    repo TEXT NOT NULL,      -- Key: Repository
    name TEXT NOT NULL,      -- Key: Name
    type TEXT NOT NULL,      -- RefType: Type
    action TEXT NOT NULL,    -- RefAction: Action
    date TIMESTAMP NOT NULL, -- Date: Date
    user TEXT NOT NULL,      -- User: User
    ref TEXT NOT NULL,       -- SHA1: Ref SHA
    symref TEXT,             -- Text: Symbolic ref
    PRIMARY KEY (repo, type, name, date, action, user, ref)
);
COMMENT ON TABLE perforce.refhist IS 'Reference history for graph depots';

-- db.remote: Remote specifications
CREATE TABLE IF NOT EXISTS perforce.remote (
    id TEXT NOT NULL,        -- RemoteID: Remote ID
    owner TEXT,              -- User: Owner
    options INTEGER,         -- Int: Options
    address TEXT,            -- Text: Address
    desc TEXT,               -- Text: Description
    update TIMESTAMP,        -- Date: Update
    access TIMESTAMP,        -- Date: Access
    fetch BIGINT,            -- Change: Fetch change
    push BIGINT,             -- Change: Push change
    rmtuser TEXT,            -- User: Remote user
    PRIMARY KEY (id)
);
COMMENT ON TABLE perforce.remote IS 'Remote specifications';

-- db.repo: Graph depot repositories
CREATE TABLE IF NOT EXISTS perforce.repo (
    repo TEXT NOT NULL,      -- Key: Repository name
    user TEXT,               -- User: Owner
    date TIMESTAMP,          -- Date: Creation date
    description TEXT,        -- Text: Description
    options INTEGER,         -- Int: Options
    PRIMARY KEY (repo)
);
COMMENT ON TABLE perforce.repo IS 'Graph depot repositories';

-- db.replicate: Replication configuration
CREATE TABLE IF NOT EXISTS perforce.replicate (
    server TEXT NOT NULL,    -- Key: Server ID
    type TEXT,               -- ReplicateType: Replication type
    address TEXT,            -- Text: Address
    options INTEGER,         -- Int: Options
    PRIMARY KEY (server)
);
COMMENT ON TABLE perforce.replicate IS 'Replication configuration for servers';

-- db.replack: Replication acknowledge records
CREATE TABLE IF NOT EXISTS perforce.replack (
    seq BIGINT NOT NULL,     -- Int: Sequence
    server TEXT NOT NULL,    -- Key: Server
    PRIMARY KEY (seq, server)
);
COMMENT ON TABLE perforce.replack IS 'Replication acknowledge records';

-- db.revoke: Revoked licenses or access
CREATE TABLE IF NOT EXISTS perforce.revoke (
    user TEXT NOT NULL,      -- User: User
    date TIMESTAMP,          -- Date: Revoke date
    reason TEXT,             -- Text: Reason
    PRIMARY KEY (user)
);
COMMENT ON TABLE perforce.revoke IS 'Revoked user licenses or access';

-- db.rev: File revision records
CREATE TABLE IF NOT EXISTS perforce.rev (
    depotFile TEXT NOT NULL, -- File: Depot file path
    rev INTEGER NOT NULL,    -- Rev: Revision number
    change BIGINT,           -- Change: Associated changelist
    action TEXT,             -- Action: Action (add, edit, delete)
    type TEXT,               -- FileType: File type
    date TIMESTAMP,          -- Date: Timestamp
    digest TEXT,             -- Digest: Content digest
    fileSize BIGINT,         -- FileSize: Size
    PRIMARY KEY (depotFile, rev)
);
COMMENT ON TABLE perforce.rev IS 'File revision records and history';

-- db.revdx: File revision digest index
CREATE TABLE IF NOT EXISTS perforce.revdx (
    depotFile TEXT NOT NULL, -- File: Depot file
    rev INTEGER NOT NULL,    -- Rev: Revision
    digest TEXT NOT NULL,    -- Digest: Digest
    PRIMARY KEY (depotFile, rev, digest)
);
COMMENT ON TABLE perforce.revdx IS 'Index for file revisions by digest';

-- db.rmtdepots: Remote depots
CREATE TABLE IF NOT EXISTS perforce.rmtdepots (
    remote TEXT NOT NULL,    -- RemoteID: Remote ID
    depot TEXT NOT NULL,     -- Domain: Depot name
    address TEXT,            -- Text: Address
    PRIMARY KEY (remote, depot)
);
COMMENT ON TABLE perforce.rmtdepots IS 'Remote depot specifications';

-- db.rmtview: Remote depot views
CREATE TABLE IF NOT EXISTS perforce.rmtview (
    remote TEXT NOT NULL,    -- RemoteID: Remote
    seq INTEGER NOT NULL,    -- Int: Sequence
    mapFlag TEXT,            -- MapFlag: Map flag
    localSpec TEXT,          -- Mapping: Local spec
    remoteSpec TEXT,         -- Mapping: Remote spec
    PRIMARY KEY (remote, seq)
);
COMMENT ON TABLE perforce.rmtview IS 'Views for remote depots';

-- db.rmtviewx: Remote depot views indexed by local spec
CREATE TABLE IF NOT EXISTS perforce.rmtviewx (
    remote TEXT NOT NULL,    -- RemoteID: Remote
    localSpec TEXT NOT NULL, -- Mapping: Local spec
    seq INTEGER,             -- Int: Sequence
    mapFlag TEXT,            -- MapFlag: Map flag
    remoteSpec TEXT,         -- Mapping: Remote spec
    PRIMARY KEY (remote, localSpec)
);
COMMENT ON TABLE perforce.rmtviewx IS 'Indexed views for remote depots by local spec';

-- db.rmtviews: Remote depot view summaries
CREATE TABLE IF NOT EXISTS perforce.rmtviews (
    remote TEXT NOT NULL,    -- RemoteID: Remote
    view TEXT,               -- Text: View string
    PRIMARY KEY (remote)
);
COMMENT ON TABLE perforce.rmtviews IS 'Summary views for remote depots';

-- db.scanctl: Scan control for large table scans
CREATE TABLE IF NOT EXISTS perforce.scanctl (
    seq INTEGER NOT NULL,    -- Int: Sequence number
    table_name TEXT NOT NULL, -- String: Table name
    flags INTEGER,           -- Int: Control flags
    PRIMARY KEY (seq, table_name)
);
COMMENT ON TABLE perforce.scanctl IS 'ScanCtl for optimizing large scans';

-- db.scandir: Directory scan data for file system
CREATE TABLE IF NOT EXISTS perforce.scandir (
    path TEXT NOT NULL,      -- File: Directory path
    seq INTEGER NOT NULL,    -- Int: Sequence
    mtime TIMESTAMP,         -- Date: Modification time
    size BIGINT,             -- FileSize: Size
    PRIMARY KEY (path, seq)
);
COMMENT ON TABLE perforce.scandir IS 'Scandir for file system directory tracking';

-- db.sendq: Parallel file transmission work queue
CREATE TABLE IF NOT EXISTS perforce.sendq (
    seq BIGINT NOT NULL,     -- Int: Queue sequence
    file TEXT NOT NULL,      -- File: File path
    rev INTEGER,             -- Rev: Revision
    client TEXT,             -- Domain: Client
    host TEXT,               -- Text: Host
    status INTEGER,          -- Int: Status
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.sendq IS 'Parallel file transmission work queue';

-- db.sendq.pt: Per Client transmission work queue
CREATE TABLE IF NOT EXISTS perforce.sendq_pt (
    client TEXT NOT NULL,    -- Domain: Client
    seq BIGINT NOT NULL,     -- Int: Queue sequence
    file TEXT,               -- File: File path
    rev INTEGER,             -- Rev: Revision
    host TEXT,               -- Text: Host
    status INTEGER,          -- Int: Status
    PRIMARY KEY (client, seq)
);
COMMENT ON TABLE perforce.sendq_pt IS 'Per Client transmission work queue';

-- db.server: Server specifications
CREATE TABLE IF NOT EXISTS perforce.server (
    name TEXT NOT NULL,      -- Key: Server name
    type TEXT,               -- ServerType: Server type
    address TEXT,            -- Text: Server address
    options TEXT,            -- ServerOpts: Options
    description TEXT,        -- Text: Description
    update_date TIMESTAMP,   -- Date: Update date
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.server IS 'Server specifications';

-- db.stash: Stash data for unsaved work
CREATE TABLE IF NOT EXISTS perforce.stash (
    stash_id INTEGER NOT NULL, -- Int: Stash ID
    user TEXT,                 -- User: User
    client TEXT,               -- Domain: Client
    date TIMESTAMP,            -- Date: Stash date
    description TEXT,          -- Text: Description
    PRIMARY KEY (stash_id)
);
COMMENT ON TABLE perforce.stash IS 'Stash data for temporary storage';

-- db.storage: Track references to archive files
CREATE TABLE IF NOT EXISTS perforce.storage (
    file TEXT NOT NULL,      -- File: Archive file path
    rev TEXT,                -- String: Revision string
    type TEXT,               -- FileType: Type
    ref_count INTEGER,       -- Int: Reference count
    digest TEXT,             -- Digest: Digest
    size BIGINT,             -- FileSize: Size
    date TIMESTAMP,          -- Date: Timestamp
    PRIMARY KEY (file, rev)
);
COMMENT ON TABLE perforce.storage IS 'Track references to archive files';

-- db.storageg: Track references to Graph Depot archive files (for future use)
CREATE TABLE IF NOT EXISTS perforce.storageg (
    sha TEXT NOT NULL,       -- SHA1: SHA
    type TEXT,               -- ObjectType: Type
    ref_count INTEGER,       -- Int: Reference count
    PRIMARY KEY (sha)
);
COMMENT ON TABLE perforce.storageg IS 'Track references to Graph Depot archive files (for future use)';

-- db.storagesh: Track references to shelved archive files
CREATE TABLE IF NOT EXISTS perforce.storagesh (
    file TEXT NOT NULL,      -- File: Shelved file path
    rev TEXT,                -- String: Revision
    type TEXT,               -- FileType: Type
    ref_count INTEGER,       -- Int: Reference count
    digest TEXT,             -- Digest: Digest
    size BIGINT,             -- FileSize: Size
    date TIMESTAMP,          -- Date: Timestamp
    PRIMARY KEY (file, rev)
);
COMMENT ON TABLE perforce.storagesh IS 'Track references to shelved archive files';

-- db.storagesx: Digest and filesize based index for db.storagesh
CREATE TABLE IF NOT EXISTS perforce.storagesx (
    digest TEXT NOT NULL,    -- Digest: Digest
    size BIGINT NOT NULL,    -- FileSize: Size
    file TEXT,               -- File: File path
    rev TEXT,                -- String: Revision
    PRIMARY KEY (digest, size)
);
COMMENT ON TABLE perforce.storagesx IS 'Digest and filesize based index for db.storagesh';

-- db.stream: Stream specifications
CREATE TABLE IF NOT EXISTS perforce.stream (
    stream TEXT NOT NULL,    -- Domain: Stream name
    parent TEXT,             -- Domain: Parent stream
    title TEXT,              -- Text: Stream title
    type TEXT,               -- StreamType: Stream type (mainline, release, etc.)
    change BIGINT,           -- Change: Last sync change
    status TEXT,             -- StreamStatus: Status
    PRIMARY KEY (stream)
);
COMMENT ON TABLE perforce.stream IS 'Stream specifications for branching workflows';

-- db.streamq: Stream query cache
CREATE TABLE IF NOT EXISTS perforce.streamq (
    stream TEXT NOT NULL,    -- Domain: Stream name
    query TEXT,              -- String: Query string
    results TEXT,            -- Text: Cached results
    PRIMARY KEY (stream, query)
);
COMMENT ON TABLE perforce.streamq IS 'Cache for stream queries';

-- db.streamrelation: Stream relationships and hierarchies
CREATE TABLE IF NOT EXISTS perforce.streamrelation (
    child_stream TEXT NOT NULL,  -- Domain: Child stream
    parent_stream TEXT NOT NULL, -- Domain: Parent stream
    relation_type TEXT,          -- String: Relation type
    PRIMARY KEY (child_stream, parent_stream)
);
COMMENT ON TABLE perforce.streamrelation IS 'Hierarchical relationships between streams';

-- db.streamview: Stream views
CREATE TABLE IF NOT EXISTS perforce.streamview (
    stream TEXT NOT NULL,    -- Domain: Stream name
    seq INTEGER NOT NULL,    -- Int: Sequence number
    map_flag TEXT,           -- MapFlag: Map flag
    view_file TEXT,          -- Mapping: View file spec
    depot_file TEXT,         -- Mapping: Depot file
    comment TEXT,            -- Text: Comment
    PRIMARY KEY (stream, seq)
);
COMMENT ON TABLE perforce.streamview IS 'Views for streams';

-- db.streamviewx: Indexed stream views by depot file
CREATE TABLE IF NOT EXISTS perforce.streamviewx (
    stream TEXT NOT NULL,    -- Domain: Stream name
    depot_file TEXT NOT NULL, -- Mapping: Depot file
    seq INTEGER,             -- Int: Sequence
    map_flag TEXT,           -- MapFlag: Map flag
    view_file TEXT,          -- Mapping: View file spec
    comment TEXT,            -- Text: Comment
    PRIMARY KEY (stream, depot_file)
);
COMMENT ON TABLE perforce.streamviewx IS 'Indexed views for streams by depot file';

-- db.submodule: Submodule tracking for graph depots
CREATE TABLE IF NOT EXISTS perforce.submodule (
    repo TEXT NOT NULL,      -- Key: Repository
    path TEXT NOT NULL,      -- Text: Path
    url TEXT,                -- Text: URL
    PRIMARY KEY (repo, path)
);
COMMENT ON TABLE perforce.submodule IS 'Submodule configurations in graph depots';

-- db.svrview: Server views
CREATE TABLE IF NOT EXISTS perforce.svrview (
    server_id TEXT NOT NULL, -- Key: Server ID
    seq INTEGER NOT NULL,    -- Int: Sequence
    map_flag TEXT,           -- MapFlag: Map flag
    local_spec TEXT,         -- Mapping: Local spec
    remote_spec TEXT,        -- Mapping: Remote spec
    PRIMARY KEY (server_id, seq)
);
COMMENT ON TABLE perforce.svrview IS 'Views for distributed servers';

-- db.template: Template specifications
CREATE TABLE IF NOT EXISTS perforce.template (
    template_name TEXT NOT NULL, -- Domain: Template name
    owner TEXT,                  -- User: Owner
    description TEXT,            -- Text: Description
    update_date TIMESTAMP,       -- Date: Update date
    PRIMARY KEY (template_name)
);
COMMENT ON TABLE perforce.template IS 'Template specifications for forms/jobs';

-- db.templatesx: Indexed templates by field
CREATE TABLE IF NOT EXISTS perforce.templatesx (
    template_name TEXT NOT NULL, -- Domain: Template name
    field TEXT NOT NULL,         -- String: Field name
    value TEXT,                  -- Text: Value
    PRIMARY KEY (template_name, field)
);
COMMENT ON TABLE perforce.templatesx IS 'Index for template fields';

-- db.templatewx: Template views or extensions
CREATE TABLE IF NOT EXISTS perforce.templatewx (
    template_name TEXT NOT NULL, -- Domain: Template name
    seq INTEGER NOT NULL,        -- Int: Sequence
    view_spec TEXT,              -- Mapping: View spec
    PRIMARY KEY (template_name, seq)
);
COMMENT ON TABLE perforce.templatewx IS 'Extended views for templates';

-- db.tiny: Tiny database for small, non-relational data
CREATE TABLE IF NOT EXISTS perforce.tiny (
    key TEXT NOT NULL,       -- Key: Unique key
    value TEXT,              -- Text: Value
    PRIMARY KEY (key)
);
COMMENT ON TABLE perforce.tiny IS 'Tiny database for small key-value pairs';

-- db.tombstone: Tombstone records for deleted entities
CREATE TABLE IF NOT EXISTS perforce.tombstone (
    entity_type TEXT NOT NULL,  -- String: Type (e.g., user, file)
    entity_id TEXT NOT NULL,    -- Key: Entity ID
    deletion_date TIMESTAMP,    -- Date: Deletion date
    reason TEXT,                -- Text: Reason
    PRIMARY KEY (entity_type, entity_id)
);
COMMENT ON TABLE perforce.tombstone IS 'Records for permanently deleted items';

-- db.trait: File trait assignments
CREATE TABLE IF NOT EXISTS perforce.trait (
    depotFile TEXT NOT NULL, -- File: File path
    rev INTEGER,             -- Rev: Revision
    trait TEXT NOT NULL,     -- Trait: Trait name
    value TEXT,              -- Text: Trait value
    PRIMARY KEY (depotFile, rev, trait)
);
COMMENT ON TABLE perforce.trait IS 'Assigned traits to file revisions';

-- db.traits: Trait definitions
CREATE TABLE IF NOT EXISTS perforce.traits (
    trait TEXT NOT NULL,     -- Trait: Trait name
    description TEXT,        -- Text: Description
    PRIMARY KEY (trait)
);
COMMENT ON TABLE perforce.traits IS 'Definitions for custom traits';

-- db.trigger: Trigger execution logs
CREATE TABLE IF NOT EXISTS perforce.trigger (
    seq INTEGER NOT NULL,    -- Int: Sequence
    trigger_name TEXT,       -- String: Trigger name
    exec_date TIMESTAMP,     -- Date: Execution date
    status TEXT,             -- String: Status (success/fail)
    output TEXT,             -- Text: Output
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.trigger IS 'Logs of trigger executions';

-- db.triggers: Trigger specifications
CREATE TABLE IF NOT EXISTS perforce.triggers (
    trigger_name TEXT NOT NULL, -- String: Trigger name
    type TEXT,                  -- TriggerType: Type (pre, post)
    spec TEXT,                  -- Text: Trigger spec
    PRIMARY KEY (trigger_name)
);
COMMENT ON TABLE perforce.triggers IS 'Custom trigger definitions';

-- db.type: File type mappings
CREATE TABLE IF NOT EXISTS perforce.type (
    type TEXT NOT NULL,      -- String: Type name
    spec TEXT,               -- Text: Type spec
    PRIMARY KEY (type)
);
COMMENT ON TABLE perforce.type IS 'File type configurations';

-- db.types: Extended file types
CREATE TABLE IF NOT EXISTS perforce.types (
    seq INTEGER NOT NULL,    -- Int: Sequence
    type TEXT,               -- String: Type
    pattern TEXT,            -- Text: Pattern
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.types IS 'Mappings for file types';

-- db.typetable: Type table for binary/unary types
CREATE TABLE IF NOT EXISTS perforce.typetable (
    name TEXT NOT NULL,      -- String: Name
    type TEXT,               -- String: Type (binary/unary)
    PRIMARY KEY (name)
);
COMMENT ON TABLE perforce.typetable IS 'Table for type handling';

-- db.updates: Update history for entities
CREATE TABLE IF NOT EXISTS perforce.updates (
    entity_type TEXT NOT NULL, -- String: Entity type
    entity_id TEXT NOT NULL,   -- Key: ID
    update_date TIMESTAMP,     -- Date: Update date
    user TEXT,                 -- User: Updater
    PRIMARY KEY (entity_type, entity_id, update_date)
);
COMMENT ON TABLE perforce.updates IS 'History of updates to entities';

-- db.ticket: Login tickets for authentication
CREATE TABLE IF NOT EXISTS perforce.ticket (
    ticket TEXT NOT NULL,    -- Text: Ticket string
    user TEXT,               -- User: Username
    client TEXT,             -- Domain: Client
    type TEXT,               -- TicketType: Ticket type
    expires TIMESTAMP,       -- Date: Expiration date
    PRIMARY KEY (ticket)
);
COMMENT ON TABLE perforce.ticket IS 'Login tickets for user authentication';

-- db.ticket.rp: Replica tickets for distributed servers
CREATE TABLE IF NOT EXISTS perforce.ticket_rp (
    ticket TEXT NOT NULL,    -- Text: Ticket string
    user TEXT,               -- User: Username
    client TEXT,             -- Domain: Client
    type TEXT,               -- TicketType: Ticket type
    expires TIMESTAMP,       -- Date: Expiration date
    PRIMARY KEY (ticket)
);
COMMENT ON TABLE perforce.ticket_rp IS 'Login tickets for replica servers';

-- db.topology: Server topology for distributed environments
CREATE TABLE IF NOT EXISTS perforce.topology (
    server TEXT NOT NULL,    -- Key: Server ID
    type TEXT,               -- TopologyType: Topology type
    parent TEXT,             -- Key: Parent server
    options TEXT,            -- Text: Options
    PRIMARY KEY (server)
);
COMMENT ON TABLE perforce.topology IS 'Server topology configurations';

-- db.upgrades: Server upgrade history
CREATE TABLE IF NOT EXISTS perforce.upgrades (
    seq INTEGER NOT NULL,    -- Int: Sequence
    name TEXT,               -- Text: Upgrade name
    state TEXT,              -- UpgradeState: State
    startdate TIMESTAMP,     -- Date: Start date
    enddate TIMESTAMP,       -- Date: End date
    info TEXT,               -- Text: Info
    PRIMARY KEY (seq)
);
COMMENT ON TABLE perforce.upgrades IS 'Server upgrade history';

-- db.user: User specifications
CREATE TABLE IF NOT EXISTS perforce.user (
    user TEXT NOT NULL,      -- User: Username (PK)
    fullName TEXT,           -- Text: Full name
    email TEXT,              -- Text: Email
    type TEXT,               -- UserLevel: License type
    auth TEXT,               -- UserAuthType: Auth method
    password TEXT,           -- Password: Hashed password
    loginDate TIMESTAMP,     -- Date: Last login
    accessDate TIMESTAMP,    -- Date: Last access
    PRIMARY KEY (user)
);
COMMENT ON TABLE perforce.user IS 'User account specifications';

-- db.user.rp: Replica user info
CREATE TABLE IF NOT EXISTS perforce.user_rp (
    user TEXT NOT NULL,      -- User: Username
    fullName TEXT,           -- Text: Full name
    email TEXT,              -- Text: Email
    type TEXT,               -- UserLevel: License type
    auth TEXT,               -- UserAuthType: Auth method
    loginDate TIMESTAMP,     -- Date: Last login
    accessDate TIMESTAMP,    -- Date: Last access
    PRIMARY KEY (user)
);
COMMENT ON TABLE perforce.user_rp IS 'User info for replica servers';

-- db.uxtext: Indexing for user reviews
CREATE TABLE IF NOT EXISTS perforce.uxtext (
    review_id INTEGER NOT NULL, -- Int: Review ID
    text TEXT NOT NULL,         -- Text: Indexed text
    PRIMARY KEY (review_id, text)
);
COMMENT ON TABLE perforce.uxtext IS 'Full-text index for code reviews';

-- db.view: Client view mappings
CREATE TABLE IF NOT EXISTS perforce.view (
    client TEXT NOT NULL,    -- Domain: Client name
    seq INTEGER NOT NULL,    -- Int: Sequence number
    mapFlag TEXT,            -- MapFlag: Mapping flag
    viewFile TEXT,           -- Mapping: Client-side path
    depotFile TEXT,          -- Mapping: Depot path
    comment TEXT,            -- Text: Comment
    PRIMARY KEY (client, seq)
);
COMMENT ON TABLE perforce.view IS 'Client view mappings for workspaces';

-- db.view.rp: Replica client views
CREATE TABLE IF NOT EXISTS perforce.view_rp (
    client TEXT NOT NULL,    -- Domain: Client name
    seq INTEGER NOT NULL,    -- Int: Sequence number
    mapFlag TEXT,            -- MapFlag: Mapping flag
    viewFile TEXT,           -- Mapping: Client-side path
    depotFile TEXT,          -- Mapping: Depot path
    comment TEXT,            -- Text: Comment
    PRIMARY KEY (client, seq)
);
COMMENT ON TABLE perforce.view_rp IS 'Client views for replica servers';

-- db.working: Working files (open files in workspaces)
CREATE TABLE IF NOT EXISTS perforce.working (
    clientFile TEXT NOT NULL, -- File: Client file path
    depotFile TEXT NOT NULL,  -- File: Depot file path
    rev INTEGER,              -- Rev: Revision
    action TEXT,              -- Action: Open action
    type TEXT,                -- FileType: File type
    change BIGINT,            -- Change: Pending changelist
    user TEXT,                -- User: User
    time TIMESTAMP,           -- Date: Open time
    PRIMARY KEY (clientFile, depotFile)
);
COMMENT ON TABLE perforce.working IS 'Records of open files in client workspaces';

-- db.workingg: Working files for graph depots
CREATE TABLE IF NOT EXISTS perforce.workingg (
    repo TEXT NOT NULL,      -- Key: Repository
    clientFile TEXT NOT NULL, -- File: Client path
    depotFile TEXT NOT NULL,  -- File: Depot path
    action TEXT,              -- Action: Action
    blobSha TEXT,             -- SHA1: Blob SHA
    commitSha TEXT,           -- SHA1: Commit SHA
    user TEXT,                -- User: User
    PRIMARY KEY (repo, clientFile, depotFile)
);
COMMENT ON TABLE perforce.workingg IS 'Open files in graph depot workspaces';

-- db.workingx: Indexed working files by depot path
CREATE TABLE IF NOT EXISTS perforce.workingx (
    depotFile TEXT NOT NULL, -- File: Depot path
    clientFile TEXT,         -- File: Client path
    rev INTEGER,             -- Rev: Revision
    action TEXT,             -- Action: Action
    type TEXT,               -- FileType: Type
    change BIGINT,           -- Change: Changelist
    user TEXT,               -- User: User
    time TIMESTAMP,          -- Date: Time
    PRIMARY KEY (depotFile)
);
COMMENT ON TABLE perforce.workingx IS 'Index of open files by depot path';

-- pdb.lbr: Primary archive library (file content storage)
CREATE TABLE IF NOT EXISTS perforce.pdb_lbr (
    file TEXT NOT NULL,      -- File: Archive file path
    rev TEXT NOT NULL,       -- String: Revision
    content BYTEA,           -- Octet String: Binary file content
    size BIGINT,             -- FileSize: Size
    PRIMARY KEY (file, rev)
);
COMMENT ON TABLE perforce.pdb_lbr IS 'Primary storage for archive file contents';

-- rdb.lbr: Replica archive library
CREATE TABLE IF NOT EXISTS perforce.rdb_lbr (
    file TEXT NOT NULL,      -- File: Archive file path
    rev TEXT NOT NULL,       -- String: Revision
    content BYTEA,           -- Octet String: Binary file content
    size BIGINT,             -- FileSize: Size
    PRIMARY KEY (file, rev)
);
COMMENT ON TABLE perforce.rdb_lbr IS 'Replica storage for archive file contents';

-- tiny.db: Tiny key-value store for miscellaneous data
CREATE TABLE IF NOT EXISTS perforce.tiny_db (
    key TEXT NOT NULL,       -- Key: Unique key
    value TEXT,              -- Text: Value
    PRIMARY KEY (key)
);
COMMENT ON TABLE perforce.tiny_db IS 'Miscellaneous small key-value data';

-- Consolidated Indexes (from batches; deduplicated for perf)
CREATE INDEX IF NOT EXISTS idx_config_server ON perforce.config (server_name);
CREATE INDEX IF NOT EXISTS idx_configh_sname ON perforce.configh (s_name);
CREATE INDEX IF NOT EXISTS idx_counters_value ON perforce.counters (value);
CREATE INDEX IF NOT EXISTS idx_nameval_value ON perforce.nameval (value);
CREATE INDEX IF NOT EXISTS idx_upgrades_date ON perforce.upgrades_rp (startdate, enddate);
CREATE INDEX IF NOT EXISTS idx_depot_extra ON perforce.depot USING GIN (extra);
CREATE INDEX IF NOT EXISTS idx_desc_descKey ON perforce.desc (descKey);
CREATE INDEX IF NOT EXISTS idx_domain_owner ON perforce.domain (owner);
CREATE INDEX IF NOT EXISTS idx_excl_client ON perforce.excl (client);
CREATE INDEX IF NOT EXISTS idx_exclg_user ON perforce.exclg (user);
CREATE INDEX IF NOT EXISTS idx_exclgx_repo ON perforce.exclgx (repo);
CREATE INDEX IF NOT EXISTS idx_fix_change ON perforce.fix (change);
CREATE INDEX IF NOT EXISTS idx_fixrev_job ON perforce.fixrev (job);
CREATE INDEX IF NOT EXISTS idx_graphindex_id ON perforce.graphindex (id);
CREATE INDEX IF NOT EXISTS idx_graphperm_user ON perforce.graphperm (user);
CREATE INDEX IF NOT EXISTS idx_group_group_name ON perforce.group (group_name);
CREATE INDEX IF NOT EXISTS idx_groupx_ldapConf ON perforce.groupx (ldapConf);
CREATE INDEX IF NOT EXISTS idx_have_depot_file ON perforce.have (depotFile);
CREATE INDEX IF NOT EXISTS idx_have_pt_client ON perforce.have_pt (clientFile);
CREATE INDEX IF NOT EXISTS idx_have_rp_type ON perforce.have_rp (type);
CREATE INDEX IF NOT EXISTS idx_haveg_repo ON perforce.haveg (repo);
CREATE INDEX IF NOT EXISTS idx_haveview_name ON perforce.haveview (name);
CREATE INDEX IF NOT EXISTS idx_integed_to_file ON perforce.integed (toFile);
CREATE INDEX IF NOT EXISTS idx_integedss_to_key ON perforce.integedss (toKey);
CREATE INDEX IF NOT EXISTS idx_integtx_from_file ON perforce.integtx (fromFile);
CREATE INDEX IF NOT EXISTS idx_ixtext_descKey ON perforce.ixtext (descKey);
CREATE INDEX IF NOT EXISTS idx_ixtexthx_text ON perforce.ixtexthx (text);
CREATE INDEX IF NOT EXISTS idx_jnlack_server ON perforce.jnlack (server);
CREATE INDEX IF NOT EXISTS idx_job_user ON perforce.job (user);
CREATE INDEX IF NOT EXISTS idx_label_owner ON perforce.label (owner);
CREATE INDEX IF NOT EXISTS idx_ldap_port ON perforce.ldap (port);
CREATE INDEX IF NOT EXISTS idx_locks_client ON perforce.locks (client);
CREATE INDEX IF NOT EXISTS idx_locksg_ref ON perforce.locksg (ref);
CREATE INDEX IF NOT EXISTS idx_logger_date ON perforce.logger (date);
CREATE INDEX IF NOT EXISTS idx_message_severity ON perforce.message (severity);
CREATE INDEX IF NOT EXISTS idx_monitor_user ON perforce.monitor (user);
CREATE INDEX IF NOT EXISTS idx_object_type ON perforce.object (type);
CREATE INDEX IF NOT EXISTS idx_property_name ON perforce.property (name);
CREATE INDEX IF NOT EXISTS idx_protect_user ON perforce.protect (user);
CREATE INDEX IF NOT EXISTS idx_pubkey_user ON perforce.pubkey (user);
CREATE INDEX IF NOT EXISTS idx_ref_repo ON perforce.ref (repo);
CREATE INDEX IF NOT EXISTS idx_refcntadjust_adjustment ON perforce.refcntadjust (adjustment);
CREATE INDEX IF NOT EXISTS idx_refhist_repo ON perforce.refhist (repo);
CREATE INDEX IF NOT EXISTS idx_remote_owner ON perforce.remote (owner);
CREATE INDEX IF NOT EXISTS idx_repo_user ON perforce.repo (user);
CREATE INDEX IF NOT EXISTS idx_replicate_type ON perforce.replicate (type);
CREATE INDEX IF NOT EXISTS idx_replack_seq ON perforce.replack (seq);
CREATE INDEX IF NOT EXISTS idx_revoke_date ON perforce.revoke (date);
CREATE INDEX IF NOT EXISTS idx_rev_change ON perforce.rev (change);
CREATE INDEX IF NOT EXISTS idx_rev_digest ON perforce.rev (digest);
CREATE INDEX IF NOT EXISTS idx_rmtdepots_depot ON perforce.rmtdepots (depot);
CREATE INDEX IF NOT EXISTS idx_rmtview_remote_spec ON perforce.rmtview (remoteSpec);
CREATE INDEX IF NOT EXISTS idx_rmtviewx_localSpec ON perforce.rmtviewx (localSpec);
CREATE INDEX IF NOT EXISTS idx_rmtviews_view ON perforce.rmtviews (view);
CREATE INDEX IF NOT EXISTS idx_scanctl_table ON perforce.scanctl (table_name);
CREATE INDEX IF NOT EXISTS idx_scandir_path ON perforce.scandir (path);
CREATE INDEX IF NOT EXISTS idx_sendq_client ON perforce.sendq (client);
CREATE INDEX IF NOT EXISTS idx_sendq_pt_file ON perforce.sendq_pt (file);
CREATE INDEX IF NOT EXISTS idx_server_type ON perforce.server (type);
CREATE INDEX IF NOT EXISTS idx_stash_user ON perforce.stash (user);
CREATE INDEX IF NOT EXISTS idx_storage_digest ON perforce.storage (digest);
CREATE INDEX IF NOT EXISTS idx_storageg_type ON perforce.storageg (type);
CREATE INDEX IF NOT EXISTS idx_storagesh_digest ON perforce.storagesh (digest);
CREATE INDEX IF NOT EXISTS idx_storagesx_file ON perforce.storagesx (file);
CREATE INDEX IF NOT EXISTS idx_stream_parent ON perforce.stream (parent);
CREATE INDEX IF NOT EXISTS idx_streamq_query ON perforce.streamq (query);
CREATE INDEX IF NOT EXISTS idx_streamrelation_parent ON perforce.streamrelation (parent_stream);
CREATE INDEX IF NOT EXISTS idx_streamview_depot ON perforce.streamview (depot_file);
CREATE INDEX IF NOT EXISTS idx_streamviewx_view_file ON perforce.streamviewx (view_file);
CREATE INDEX IF NOT EXISTS idx_submodule_repo ON perforce.submodule (repo);
CREATE INDEX IF NOT EXISTS idx_svrview_server ON perforce.svrview (server_id);
CREATE INDEX IF NOT EXISTS idx_template_owner ON perforce.template (owner);
CREATE INDEX IF NOT EXISTS idx_templatesx_value ON perforce.templatesx (value);
CREATE INDEX IF NOT EXISTS idx_templatewx_view_spec ON perforce.templatewx (view_spec);
CREATE INDEX IF NOT EXISTS idx_tiny_value ON perforce.tiny (value);
CREATE INDEX IF NOT EXISTS idx_tombstone_date ON perforce.tombstone (deletion_date);
CREATE INDEX IF NOT EXISTS idx_trait_file ON perforce.trait (depotFile);
CREATE INDEX IF NOT EXISTS idx_trigger_name ON perforce.trigger (trigger_name);
CREATE INDEX IF NOT EXISTS idx_triggers_type ON perforce.triggers (type);
CREATE INDEX IF NOT EXISTS idx_type_spec ON perforce.type (spec);
CREATE INDEX IF NOT EXISTS idx_types_pattern ON perforce.types (pattern);
CREATE INDEX IF NOT EXISTS idx_typetable_type ON perforce.typetable (type);
CREATE INDEX IF NOT EXISTS idx_updates_user ON perforce.updates (user);
CREATE INDEX IF NOT EXISTS idx_ticket_user ON perforce.ticket (user);
CREATE INDEX IF NOT EXISTS idx_ticket_rp_expires ON perforce.ticket_rp (expires);
CREATE INDEX IF NOT EXISTS idx_topology_parent ON perforce.topology (parent);
CREATE INDEX IF NOT EXISTS idx_upgrades_state ON perforce.upgrades (state);
CREATE INDEX IF NOT EXISTS idx_user_email ON perforce.user (email);
CREATE INDEX IF NOT EXISTS idx_user_rp_type ON perforce.user_rp (type);
CREATE INDEX IF NOT EXISTS idx_uxtext_review ON perforce.uxtext (review_id);
CREATE INDEX IF NOT EXISTS idx_view_client ON perforce.view (client);
CREATE INDEX IF NOT EXISTS idx_view_rp_depot ON perforce.view_rp (depotFile);
CREATE INDEX IF NOT EXISTS idx_working_user ON perforce.working (user);
CREATE INDEX IF NOT EXISTS idx_workingg_repo ON perforce.workingg (repo);
CREATE INDEX IF NOT EXISTS idx_workingx_change ON perforce.workingx (change);
CREATE INDEX IF NOT EXISTS idx_pdb_lbr_size ON perforce.pdb_lbr (size);
CREATE INDEX IF NOT EXISTS idx_rdb_lbr_file ON perforce.rdb_lbr (file);
CREATE INDEX IF NOT EXISTS idx_tiny_db_value ON perforce.tiny_db (value);

-- End of schema. Total unique tables: ~114 (consolidated from batches).
```
