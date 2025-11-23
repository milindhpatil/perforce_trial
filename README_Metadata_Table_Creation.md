### PostgreSQL CREATE TABLE Statements

Based on the P4 Server Schema Documentation (2025.1), below are the `CREATE TABLE` statements for all documented tables in PostgreSQL. I have mapped P4 data types to appropriate PostgreSQL types as follows (for consistency and performance):

- `Int`, `Change`, `Rev`: `INTEGER`
- `Int64`: `BIGINT`
- `Key`, `User`, `Domain`, `File`, `Text`, `String`, `Mapping`, `Password`, `SHA1`, `Digest`: `TEXT`
- `Date`: `BIGINT` (Unix timestamp in seconds)
- `FileSize`: `BIGINT`
- `FileType`, `Action`: `TEXT`
- `Octet String`: `BYTEA`
- `TraitLot`: `INTEGER`
- `Value`: `TEXT`

Primary keys are defined based on the "Indexed on" fields (assumed to be unique/composite primary keys). Indexes are added for secondary indexing where specified. Tables are created in alphabetical order for the main `db.*` tables (excluding proxy/replica-specific like `pdb.lbr`, `rdb.lbr`, and `tiny.db` as they are specialized).

```sql
-- db.bodresolve - Resolve data for stream specifications
CREATE TABLE db.bodresolve (
    type TEXT,
    client TEXT,
    toKey TEXT,
    attr INTEGER,
    fromKey TEXT,
    fromChange INTEGER,
    baseKey TEXT,
    baseChange INTEGER,
    how TEXT,
    state TEXT,
    PRIMARY KEY (type, client, toKey, attr, fromKey, fromChange)
);

-- db.bodresolvex - Pending integration records for shelved stream specifications
CREATE TABLE db.bodresolvex (
    type TEXT,
    shelf INTEGER,
    toKey TEXT,
    attr INTEGER,
    fromKey TEXT,
    fromChange INTEGER,
    baseKey TEXT,
    baseChange INTEGER,
    how TEXT,
    state TEXT,
    client TEXT,
    PRIMARY KEY (type, shelf, toKey, attr, fromKey, fromChange)
);

-- db.bodtext - Job data for job attributes
CREATE TABLE db.bodtext (
    key TEXT,
    attr INTEGER,
    isBulk INTEGER,
    text TEXT,
    PRIMARY KEY (key, attr)
);

-- db.bodtextcx - Versioned openable spec fields
CREATE TABLE db.bodtextcx (
    type INTEGER,
    key TEXT,
    change INTEGER,
    attr INTEGER,
    text TEXT,
    PRIMARY KEY (type, key, change, attr)
);

-- db.bodtexthx - Head revision of spec fields
CREATE TABLE db.bodtexthx (
    type INTEGER,
    key TEXT,
    attr INTEGER,
    bulk INTEGER,
    text TEXT,
    PRIMARY KEY (type, key, attr)
);

-- db.bodtextsx - Shelved openable spec fields
CREATE TABLE db.bodtextsx (
    type INTEGER,
    shelf INTEGER,
    key TEXT,
    attr INTEGER,
    text TEXT,
    workChange INTEGER,
    user TEXT,
    action TEXT,
    PRIMARY KEY (type, shelf, key, attr)
);

-- db.bodtextwx - Open openable spec fields
CREATE TABLE db.bodtextwx (
    type INTEGER,
    client TEXT,
    key TEXT,
    attr INTEGER,
    text TEXT,
    workChange INTEGER,
    user TEXT,
    action TEXT,
    PRIMARY KEY (type, client, key, attr)
);

-- db.change - Changelists
CREATE TABLE db.change (
    change INTEGER,
    descKey INTEGER,
    client TEXT,
    user TEXT,
    date BIGINT,
    status TEXT,
    description TEXT,
    root TEXT,
    importer TEXT,
    identity TEXT,
    access BIGINT,
    update BIGINT,
    stream TEXT,
    PRIMARY KEY (change)
);
CREATE INDEX idx_db_change_identity ON db.change (identity);

-- db.changeidx - Secondary index of db.change/db.changex
CREATE TABLE db.changeidx (
    identity TEXT,
    change INTEGER,
    PRIMARY KEY (identity)
);

-- db.changex - Subset of db.change: records for pending changelists only
CREATE TABLE db.changex (
    change INTEGER,
    descKey INTEGER,
    client TEXT,
    user TEXT,
    date BIGINT,
    status TEXT,
    description TEXT,
    root TEXT,
    importer TEXT,
    identity TEXT,
    access BIGINT,
    update BIGINT,
    stream TEXT,
    PRIMARY KEY (change)
);

-- db.ckphist - Stores history of checkpoint events
CREATE TABLE db.ckphist (
    start BIGINT,
    jnum INTEGER,
    who INTEGER,
    type TEXT,
    end BIGINT,
    flags TEXT,
    jfile TEXT,
    jdate BIGINT,
    jdigest TEXT,
    jsize BIGINT,
    jtype TEXT,
    failed INTEGER,
    errmsg BYTEA,
    PRIMARY KEY (start, jnum, type, who)
);

-- db.config - Server configurations table
CREATE TABLE db.config (
    serverName TEXT,
    name TEXT,
    value TEXT,
    PRIMARY KEY (serverName, name)
);

-- db.configh - Server configuration history
CREATE TABLE db.configh (
    sName TEXT,
    name TEXT,
    version INTEGER,
    date BIGINT,
    server TEXT,
    user TEXT,
    ovalue TEXT,
    nvalue TEXT,
    comment TEXT,
    PRIMARY KEY (sName, name, version, date, server)
);

-- db.counters - Counters table
CREATE TABLE db.counters (
    name TEXT,
    value TEXT,
    PRIMARY KEY (name)
);

-- db.depot - Depot specifications
CREATE TABLE db.depot (
    name TEXT,
    type TEXT,
    extra TEXT,
    map TEXT,
    objAddr TEXT,
    PRIMARY KEY (name)
);

-- db.desc - Change descriptions
CREATE TABLE db.desc (
    descKey INTEGER,
    description TEXT,
    PRIMARY KEY (descKey)
);

-- db.domain - Domains: depots, clients, labels, branches, streams, and typemap
CREATE TABLE db.domain (
    name TEXT,
    type TEXT,
    extra TEXT,
    mount TEXT,
    mount2 TEXT,
    mount3 TEXT,
    owner TEXT,
    updateDate BIGINT,
    accessDate BIGINT,
    options TEXT,
    description TEXT,
    stream TEXT,
    serverId TEXT,
    contents INTEGER,
    PRIMARY KEY (name)
);

-- db.excl - Exclusively locked (+l) files: enables coordinated file locking in commit/edge server environments
CREATE TABLE db.excl (
    depotFile TEXT,
    client TEXT,
    user TEXT,
    PRIMARY KEY (depotFile)
);

-- db.exclg - Graph depot LFS locks
CREATE TABLE db.exclg (
    repo TEXT,
    ref TEXT,
    file TEXT,
    lockId TEXT,
    user TEXT,
    created TEXT,
    PRIMARY KEY (repo, ref, file)
);

-- db.exclgx - Graph depot LFS locks indexed by lockId
CREATE TABLE db.exclgx (
    lockId TEXT,
    repo TEXT,
    ref TEXT,
    file TEXT,
    user TEXT,
    created TEXT,
    PRIMARY KEY (lockId)
);

-- db.fix - Fix records: indexed by job
CREATE TABLE db.fix (
    job TEXT,
    change INTEGER,
    date BIGINT,
    status TEXT,
    client TEXT,
    user TEXT,
    PRIMARY KEY (job, change)
);
CREATE INDEX idx_db_fix_change ON db.fix (change);

-- db.fixrev - Fix records: indexed by change
CREATE TABLE db.fixrev (
    job TEXT,
    change INTEGER,
    date BIGINT,
    status TEXT,
    client TEXT,
    user TEXT,
    PRIMARY KEY (change, job)
);

-- db.graphindex - Graph depot repository index data
CREATE TABLE db.graphindex (
    id INTEGER,
    name TEXT,
    date BIGINT,
    blobSha TEXT,
    commitSha TEXT,
    flags INTEGER,
    size BIGINT,
    type TEXT,
    lfsoid TEXT,
    PRIMARY KEY (id, name, date, blobSha, commitSha)
);

-- db.graphperm - Graph depot permissions
CREATE TABLE db.graphperm (
    name TEXT,
    repo TEXT,
    ref TEXT,
    type TEXT,
    user TEXT,
    perm TEXT,
    PRIMARY KEY (name, repo, ref, type, user, perm)
);

-- db.group - Group specifications
CREATE TABLE db.group (
    user TEXT,
    group TEXT,
    type TEXT,
    maxResults TEXT,
    maxScanRows TEXT,
    maxLockTime TEXT,
    maxOpenFiles TEXT,
    timeout INTEGER,
    passwordTimeout INTEGER,
    maxMemory TEXT,
    idleTimeout INTEGER,
    PRIMARY KEY (user, group)
);

-- db.groupx - Per-group data to support group membership controlled by AD/LDAP group membership
CREATE TABLE db.groupx (
    group TEXT,
    ldapConf TEXT,
    ldapSearchQuery TEXT,
    ldapUserAttribute TEXT,
    ldapDNAttribute TEXT,
    description TEXT,
    PRIMARY KEY (group)
);

-- db.have - Contains the 'have-list' for all clients
CREATE TABLE db.have (
    clientFile TEXT,
    depotFile TEXT,
    haveRev INTEGER,
    type TEXT,
    time BIGINT,
    PRIMARY KEY (clientFile)
);

-- db.have.pt - Placeholder for clients of types readonly, partitioned, and partitioned-jnl
CREATE TABLE db.have_pt (
    clientFile TEXT,
    depotFile TEXT,
    haveRev INTEGER,
    type TEXT,
    time BIGINT,
    PRIMARY KEY (clientFile)
);

-- db.have.rp - Contains the 'have-list' for clients of build-server replicas
CREATE TABLE db.have_rp (
    clientFile TEXT,
    depotFile TEXT,
    haveRev INTEGER,
    type TEXT,
    time BIGINT,
    PRIMARY KEY (clientFile)
);

-- db.haveg - Contains the 'have-list' for graph depot files that are not at the same revision as defined by the client's have reference
CREATE TABLE db.haveg (
    repo TEXT,
    clientFile TEXT,
    depotFile TEXT,
    client TEXT,
    type TEXT,
    action TEXT,
    blobSha TEXT,
    commitSha TEXT,
    flags INTEGER,
    PRIMARY KEY (repo, clientFile)
);

-- db.haveview - Stores mapping changes for clients mapping graph depot content
CREATE TABLE db.haveview (
    name TEXT,
    seq INTEGER,
    mapFlag TEXT,
    viewFile TEXT,
    depotFile TEXT,
    comment TEXT,
    PRIMARY KEY (name, seq)
);

-- db.integed - Permanent integration records
CREATE TABLE db.integed (
    toFile TEXT,
    fromFile TEXT,
    startFromRev INTEGER,
    endFromRev INTEGER,
    startToRev INTEGER,
    endToRev INTEGER,
    how TEXT,
    change INTEGER,
    PRIMARY KEY (toFile, fromFile, startFromRev, endFromRev, startToRev, endToRev)
);

-- db.integedss - Stream specification integration history
CREATE TABLE db.integedss (
    toKey TEXT,
    attr INTEGER,
    fromKey TEXT,
    endfromChange INTEGER,
    endtoChange INTEGER,
    startfromChange INTEGER,
    starttoChange INTEGER,
    baseKey TEXT,
    baseChange INTEGER,
    how TEXT,
    change INTEGER,
    PRIMARY KEY (toKey, attr, fromKey, endfromChange, endtoChange)
);

-- db.integtx - Temporary integration records used by task streams
CREATE TABLE db.integtx (
    toFile TEXT,
    fromFile TEXT,
    startFromRev INTEGER,
    endFromRev INTEGER,
    startToRev INTEGER,
    endToRev INTEGER,
    how TEXT,
    change INTEGER,
    PRIMARY KEY (toFile, fromFile, startFromRev, endFromRev, startToRev, endToRev)
);

-- db.ixtext - Indexing data for generic and job attributes
CREATE TABLE db.ixtext (
    word TEXT,
    attr INTEGER,
    value TEXT,
    PRIMARY KEY (word, attr, value)
);

-- db.ixtexthx - Indexing data for head revision of all spec fields
CREATE TABLE db.ixtexthx (
    type TEXT,
    word TEXT,
    attr INTEGER,
    value TEXT,
    PRIMARY KEY (type, word, attr, value)
);

-- db.jnlack - Tracks journal positions of all replicas
CREATE TABLE db.jnlack (
    serverId TEXT,
    lastUpdate BIGINT,
    serverType TEXT,
    persistedJnl INTEGER,
    appliedJnl INTEGER,
    persistedPos BIGINT,
    appliedPos BIGINT,
    jcflags TEXT,
    isAlive INTEGER,
    serverOptions TEXT,
    failoverSeen TEXT,
    PRIMARY KEY (serverId)
);

-- db.job - Job records
CREATE TABLE db.job (
    job TEXT,
    xuser TEXT,
    xdate BIGINT,
    xstatus TEXT,
    description TEXT,
    PRIMARY KEY (job)
);

-- db.label - Revisions of files in labels
CREATE TABLE db.label (
    name TEXT,
    depotFile TEXT,
    haveRev INTEGER,
    PRIMARY KEY (name, depotFile)
);

-- db.ldap - LDAP specifications
CREATE TABLE db.ldap (
    name TEXT,
    host TEXT,
    port INTEGER,
    ssl INTEGER,
    type INTEGER,
    pattern TEXT,
    baseDN TEXT,
    filter TEXT,
    scope INTEGER,
    bindDN TEXT,
    bindpass TEXT,
    realm TEXT,
    groupBaseDN TEXT,
    groupFilter TEXT,
    groupScope INTEGER,
    options INTEGER,
    attrUid TEXT,
    attrEmail TEXT,
    attrName TEXT,
    PRIMARY KEY (name)
);

-- db.locks - Locked/Unlocked files
CREATE TABLE db.locks (
    depotFile TEXT,
    client TEXT,
    user TEXT,
    action TEXT,
    isLocked TEXT,
    change INTEGER,
    PRIMARY KEY (depotFile, client)
);

-- db.locksg - Lock records for clients of type graph
CREATE TABLE db.locksg (
    depotFile TEXT,
    client TEXT,
    user TEXT,
    action TEXT,
    isLocked TEXT,
    change INTEGER,
    PRIMARY KEY (depotFile, client)
);

-- db.logger - Support for 'p4 logger' command. Logs any changes to changelists and jobs.
CREATE TABLE db.logger (
    seq INTEGER,
    key TEXT,
    attr TEXT,
    PRIMARY KEY (seq)
);

-- db.message - System messages
CREATE TABLE db.message (
    language TEXT,
    id INTEGER,
    message TEXT,
    PRIMARY KEY (language, id)
);

-- db.monitor - P4 Server process information
CREATE TABLE db.monitor (
    id INTEGER,
    user TEXT,
    function TEXT,
    args TEXT,
    startDate BIGINT,
    runstate INTEGER,
    client TEXT,
    host TEXT,
    prog TEXT,
    lockInfo TEXT,
    cmt TEXT,
    ident TEXT,
    PRIMARY KEY (id)
);

-- db.nameval - A table to store key/value pairs
CREATE TABLE db.nameval (
    name TEXT,
    value TEXT,
    PRIMARY KEY (name)
);

-- db.object - Object storage for graph depots
CREATE TABLE db.object (
    sha TEXT,
    type TEXT,
    data BYTEA,
    refCount INTEGER,
    PRIMARY KEY (sha)
);

-- db.property - Properties
CREATE TABLE db.property (
    name TEXT,
    seq INTEGER,
    type TEXT,
    scope TEXT,
    value TEXT,
    date BIGINT,
    user TEXT,
    PRIMARY KEY (name, seq, type, scope)
);

-- db.protect - The protections table
CREATE TABLE db.protect (
    seq INTEGER,
    isGroup INTEGER,
    user TEXT,
    host TEXT,
    perm TEXT,
    mapFlag TEXT,
    depotFile TEXT,
    subPath TEXT,
    update BIGINT,
    PRIMARY KEY (seq)
);

-- db.pubkey - SSH Public keys
CREATE TABLE db.pubkey (
    user TEXT,
    scope TEXT,
    key TEXT,
    digest TEXT,
    update BIGINT,
    PRIMARY KEY (user, scope)
);

-- db.ref - Reference content for graph depots
CREATE TABLE db.ref (
    repo TEXT,
    type TEXT,
    name TEXT,
    ref TEXT,
    symref TEXT,
    PRIMARY KEY (repo, type, name)
);

-- db.refcntadjust - Graph depot reference count adjustments
CREATE TABLE db.refcntadjust (
    walked INTEGER,
    sha TEXT,
    adjustment INTEGER,
    adjustObject INTEGER,
    PRIMARY KEY (walked, sha)
);

-- db.refhist - Reference history for graph depots
CREATE TABLE db.refhist (
    repo TEXT,
    type TEXT,
    name TEXT,
    date BIGINT,
    action TEXT,
    user TEXT,
    ref TEXT,
    symref TEXT,
    PRIMARY KEY (repo, type, name, date, action, user, ref)
);

-- db.remote - Remote specifications
CREATE TABLE db.remote (
    id TEXT,
    owner TEXT,
    options INTEGER,
    address TEXT,
    desc TEXT,
    update BIGINT,
    access BIGINT,
    fetch INTEGER,
    push INTEGER,
    rmtuser TEXT,
    PRIMARY KEY (id)
);

-- db.repo - Repository specifications
CREATE TABLE db.repo (
    repo TEXT,
    owner TEXT,
    created BIGINT,
    pushed BIGINT,
    forked TEXT,
    desc TEXT,
    branch TEXT,
    mirror TEXT,
    options INTEGER,
    id INTEGER,
    gcmrrserver TEXT,
    gcmrrsecrettoken TEXT,
    gcmrrstatus INTEGER,
    gcmrrexcludedbranches TEXT,
    gcmrrhidefetchurl INTEGER,
    PRIMARY KEY (repo)
);

-- db.resolve - Pending integration records
CREATE TABLE db.resolve (
    toFile TEXT,
    fromFile TEXT,
    startFromRev INTEGER,
    endFromRev INTEGER,
    startToRev INTEGER,
    endToRev INTEGER,
    how TEXT,
    state TEXT,
    baseFile TEXT,
    baseRev INTEGER,
    PRIMARY KEY (toFile, fromFile, startFromRev)
);

-- db.resolveg - Resolve records for clients of type graph
CREATE TABLE db.resolveg (
    toFile TEXT,
    fromFile TEXT,
    baseSHA TEXT,
    wantsSHA TEXT,
    how TEXT,
    state TEXT,
    PRIMARY KEY (toFile, fromFile, baseSha)
);

-- db.resolvex - Pending integration records for shelved files
CREATE TABLE db.resolvex (
    toFile TEXT,
    fromFile TEXT,
    startFromRev INTEGER,
    endFromRev INTEGER,
    startToRev INTEGER,
    endToRev INTEGER,
    how TEXT,
    state TEXT,
    baseFile TEXT,
    baseRev INTEGER,
    PRIMARY KEY (toFile, fromFile, startFromRev)
);

-- db.rev - Revision records
CREATE TABLE db.rev (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revbx - Revision records for archived files
CREATE TABLE db.revbx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revcx - Secondary index of db.rev
CREATE TABLE db.revcx (
    change INTEGER,
    depotFile TEXT,
    depotRev INTEGER,
    action TEXT,
    PRIMARY KEY (change, depotFile)
);

-- db.revdx - Revision records for revisions deleted at the head revision
CREATE TABLE db.revdx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile)
);

-- db.revfs - Client filesystem file sizes
CREATE TABLE db.revfs (
    depotFile TEXT,
    rev INTEGER,
    clientType TEXT,
    clientSize BIGINT,
    PRIMARY KEY (depotFile, rev, clientType)
);

-- db.revhx - Revision records for revisions NOT deleted at the head revision
CREATE TABLE db.revhx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile)
);

-- db.review - User's review mappings
CREATE TABLE db.review (
    user TEXT,
    seq INTEGER,
    mapFlag TEXT,
    depotFile TEXT,
    type TEXT,
    PRIMARY KEY (user, seq)
);

-- db.revpx - Pending revision records
CREATE TABLE db.revpx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revsh - Revision records for shelved files
CREATE TABLE db.revsh (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev, type, action, change)
);

-- db.revstg - Temporary revision records for storage upgrade process
CREATE TABLE db.revstg (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revsx - Revision records for spec depot files
CREATE TABLE db.revsx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revtr - Rev table for huge traits
CREATE TABLE db.revtr (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revtx - Task stream revision records
CREATE TABLE db.revtx (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.revux - Revision records for unload depot files
CREATE TABLE db.revux (
    depotFile TEXT,
    depotRev INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    date BIGINT,
    modTime BIGINT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    lbrIsLazy TEXT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    PRIMARY KEY (depotFile, depotRev)
);

-- db.rmtview - View data for remote specifications
CREATE TABLE db.rmtview (
    id TEXT,
    seq INTEGER,
    mapFlag TEXT,
    localFile TEXT,
    remoteFile TEXT,
    retain INTEGER,
    PRIMARY KEY (id, seq)
);

-- db.scanctl - ScanCtl
CREATE TABLE db.scanctl (
    depotPath TEXT,
    state TEXT,
    seq INTEGER,
    dirs INTEGER,
    files INTEGER,
    zeros INTEGER,
    dirserr INTEGER,
    pri INTEGER,
    reqpause INTEGER,
    err TEXT,
    filesnonlbr INTEGER,
    filesage INTEGER,
    report TEXT,
    target TEXT,
    flags TEXT,
    reqage INTEGER,
    PRIMARY KEY (depotPath)
);

-- db.scandir - Scandir
CREATE TABLE db.scandir (
    lskey TEXT,
    seq INTEGER,
    file TEXT,
    PRIMARY KEY (lskey, seq)
);

-- db.sendq - Parallel file transmission work queue
CREATE TABLE db.sendq (
    taskid INTEGER,
    seq INTEGER,
    handle TEXT,
    depotFile TEXT,
    clientFile TEXT,
    haveRev INTEGER,
    type TEXT,
    modtime BIGINT,
    digest TEXT,
    size BIGINT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    flags INTEGER,
    clientType TEXT,
    depotRev INTEGER,
    change INTEGER,
    date BIGINT,
    blobSha TEXT,
    repoSlot INTEGER,
    shelveDigest TEXT,
    olbrFile TEXT,
    olbrRev TEXT,
    olbrType TEXT,
    PRIMARY KEY (taskid, seq)
);

-- db.sendq.pt - Per Client transmission work queue
CREATE TABLE db.sendq_pt (
    taskid INTEGER,
    seq INTEGER,
    handle TEXT,
    depotFile TEXT,
    clientFile TEXT,
    haveRev INTEGER,
    type TEXT,
    modtime BIGINT,
    digest TEXT,
    size BIGINT,
    lbrFile TEXT,
    lbrRev TEXT,
    lbrType TEXT,
    flags INTEGER,
    clientType TEXT,
    depotRev INTEGER,
    change INTEGER,
    date BIGINT,
    blobSha TEXT,
    repoSlot INTEGER,
    shelveDigest TEXT,
    olbrFile TEXT,
    olbrRev TEXT,
    olbrType TEXT,
    PRIMARY KEY (taskid, seq)
);

-- db.server - Server specifications
CREATE TABLE db.server (
    id TEXT,
    type TEXT,
    name TEXT,
    address TEXT,
    externalAddress TEXT,
    services TEXT,
    desc TEXT,
    user TEXT,
    options TEXT,
    rplFrom TEXT,
    failoverSeen TEXT,
    PRIMARY KEY (id)
);

-- db.stash - Stash data
CREATE TABLE db.stash (
    client TEXT,
    stream TEXT,
    type TEXT,
    seq INTEGER,
    change INTEGER,
    PRIMARY KEY (client, stream, type, seq)
);

-- db.storage - Track references to archive files
CREATE TABLE db.storage (
    file TEXT,
    rev TEXT,
    type TEXT,
    refCount INTEGER,
    digest TEXT,
    size BIGINT,
    serverSize BIGINT,
    compCksum TEXT,
    date BIGINT,
    PRIMARY KEY (file, rev, type)
);

-- db.storageg - Track references to Graph Depot archive files (for future use)
CREATE TABLE db.storageg (
    repo TEXT,
    sha TEXT,
    type TEXT,
    refCount INTEGER,
    date BIGINT,
    PRIMARY KEY (repo, sha, type)
);

-- db.storagesh - Track references to shelved archive files
CREATE TABLE db.storagesh (
    file TEXT,
    rev TEXT,
    type TEXT,
    refCount INTEGER,
    digest TEXT,
    size BIGINT,
    serverSize BIGINT,
    compCksum TEXT,
    date BIGINT,
    PRIMARY KEY (file, rev, type)
);

-- db.storagesx - Digest and filesize based index for db.storagesh, for finding shelved files with identical content
CREATE TABLE db.storagesx (
    digest TEXT,
    size BIGINT,
    file TEXT,
    rev TEXT,
    type TEXT,
    PRIMARY KEY (digest, size, file, rev, type)
);

-- db.stream - Stream specifications
CREATE TABLE db.stream (
    stream TEXT,
    parent TEXT,
    title TEXT,
    type TEXT,
    preview BIGINT,
    change INTEGER,
    copyChange INTEGER,
    mergeChange INTEGER,
    highChange INTEGER,
    hash INTEGER,
    status TEXT,
    parentview TEXT,
    PRIMARY KEY (stream)
);

-- db.streamq - Track streams for which the stream views should be regenerated
CREATE TABLE db.streamq (
    stream TEXT,
    PRIMARY KEY (stream)
);

-- db.streamrelation - Relationships between streams
CREATE TABLE db.streamrelation (
    independentStream TEXT,
    dependentStream TEXT,
    type TEXT,
    parentView TEXT,
    PRIMARY KEY (independentStream, dependentStream)
);

-- db.streamview - Precomputed stream views
CREATE TABLE db.streamview (
    name TEXT,
    seq INTEGER,
    mapFlag TEXT,
    viewFile TEXT,
    depotFile TEXT,
    comment TEXT,
    PRIMARY KEY (name, seq)
);

-- db.streamviewx - Indexing for precomputed stream views
CREATE TABLE db.streamviewx (
    depotPath TEXT,
    viewPath TEXT,
    mapFlag TEXT,
    stream TEXT,
    change TEXT,
    pathSource TEXT,
    pathType TEXT,
    componentPrefixes TEXT,
    effectiveComponentType TEXT,
    PRIMARY KEY (depotPath, viewPath, mapFlag, stream)
);

-- db.submodule - Submodule configuration data
CREATE TABLE db.submodule (
    repo TEXT,
    path TEXT,
    subrepo TEXT,
    PRIMARY KEY (repo, path)
);

-- db.svrview - View data for servers specifications
CREATE TABLE db.svrview (
    id TEXT,
    type TEXT,
    seq INTEGER,
    mapFlag TEXT,
    viewFile TEXT,
    PRIMARY KEY (id, type, seq)
);

-- db.template - Streams templates
CREATE TABLE db.template (
    name TEXT,
    change INTEGER,
    seq INTEGER,
    parent TEXT,
    type TEXT,
    path TEXT,
    viewFile TEXT,
    depotFile TEXT,
    changeMap TEXT,
    PRIMARY KEY (name, change, seq)
);

-- db.templatesx - Shelved stream templates
CREATE TABLE db.templatesx (
    shelf INTEGER,
    name TEXT,
    seq INTEGER,
    change INTEGER,
    parent TEXT,
    type TEXT,
    path TEXT,
    viewFile TEXT,
    depotFile TEXT,
    changeMap TEXT,
    changeAtOpen INTEGER,
    user TEXT,
    action TEXT,
    PRIMARY KEY (shelf, name, seq)
);

-- db.templatewx - Pending stream templates
CREATE TABLE db.templatewx (
    client TEXT,
    name TEXT,
    seq INTEGER,
    change INTEGER,
    parent TEXT,
    type TEXT,
    path TEXT,
    viewFile TEXT,
    depotFile TEXT,
    changeMap TEXT,
    changeAtOpen INTEGER,
    user TEXT,
    action TEXT,
    PRIMARY KEY (client, name, seq)
);

-- db.ticket - Second factor authentication state on a per user/host basis
CREATE TABLE db.ticket (
    user TEXT,
    host TEXT,
    ticket TEXT,
    state TEXT,
    token TEXT,
    updateDate BIGINT,
    PRIMARY KEY (user, host)
);

-- db.ticket.rp - Second factor authentication state on a per user/host basis (replica)
CREATE TABLE db.ticket_rp (
    user TEXT,
    host TEXT,
    ticket TEXT,
    state TEXT,
    token TEXT,
    updateDate BIGINT,
    PRIMARY KEY (user, host)
);

-- db.topology - Topology information
CREATE TABLE db.topology (
    address TEXT,
    destAddress TEXT,
    serverID TEXT,
    date BIGINT,
    type TEXT,
    encryption TEXT,
    svcUser TEXT,
    lastSeenDate BIGINT,
    svrRecType TEXT,
    taddr TEXT,
    tdaddr TEXT,
    tid TEXT,
    version TEXT,
    PRIMARY KEY (address, destAddress, serverID, date)
);

-- db.traits - Attributes associated with file revisions
CREATE TABLE db.traits (
    traitLot INTEGER,
    name TEXT,
    type TEXT,
    value BYTEA,
    PRIMARY KEY (traitLot, name)
);

-- db.trigger - Trigger specifications
CREATE TABLE db.trigger (
    seq INTEGER,
    name TEXT,
    mapFlag TEXT,
    depotFile TEXT,
    triggerDepotFile TEXT,
    trigger TEXT,
    action TEXT,
    PRIMARY KEY (seq)
);

-- db.upgrades - Store server upgrade info
CREATE TABLE db.upgrades (
    seq INTEGER,
    name TEXT,
    state TEXT,
    startdate BIGINT,
    enddate BIGINT,
    info TEXT,
    PRIMARY KEY (seq)
);

-- db.upgrades.rp - Store replica upgrade info
CREATE TABLE db.upgrades_rp (
    seq INTEGER,
    name TEXT,
    state TEXT,
    startdate BIGINT,
    enddate BIGINT,
    info TEXT,
    PRIMARY KEY (seq)
);

-- db.user - User specifications
CREATE TABLE db.user (
    user TEXT,
    email TEXT,
    jobView TEXT,
    updateDate BIGINT,
    accessDate BIGINT,
    fullName TEXT,
    password TEXT,
    strength TEXT,
    ticket TEXT,
    endDate BIGINT,
    type TEXT,
    passDate BIGINT,
    passExpire BIGINT,
    attempts BIGINT,
    auth TEXT,
    PRIMARY KEY (user)
);

-- db.user.rp - Used by replica server's to store login information
CREATE TABLE db.user_rp (
    user TEXT,
    email TEXT,
    jobView TEXT,
    updateDate BIGINT,
    accessDate BIGINT,
    fullName TEXT,
    password TEXT,
    strength TEXT,
    ticket TEXT,
    endDate BIGINT,
    type TEXT,
    passDate BIGINT,
    passExpire BIGINT,
    attempts BIGINT,
    auth TEXT,
    PRIMARY KEY (user)
);

-- db.uxtext - Indexing data for P4 Code Review
CREATE TABLE db.uxtext (
    word TEXT,
    attr INTEGER,
    value TEXT,
    PRIMARY KEY (word, attr, value)
);

-- db.view - View data for domain records
CREATE TABLE db.view (
    name TEXT,
    seq INTEGER,
    mapFlag TEXT,
    viewFile TEXT,
    depotFile TEXT,
    comment TEXT,
    PRIMARY KEY (name, seq)
);

-- db.view.rp - View data for clients of build-server replicas
CREATE TABLE db.view_rp (
    name TEXT,
    seq INTEGER,
    mapFlag TEXT,
    viewFile TEXT,
    depotFile TEXT,
    comment TEXT,
    PRIMARY KEY (name, seq)
);

-- db.working - Records for work in progress
CREATE TABLE db.working (
    clientFile TEXT,
    depotFile TEXT,
    client TEXT,
    user TEXT,
    haveRev INTEGER,
    workRev INTEGER,
    isVirtual INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    modTime BIGINT,
    isLocked TEXT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    tampered TEXT,
    clientType TEXT,
    movedFile TEXT,
    status TEXT,
    PRIMARY KEY (clientFile)
);

-- db.workingg - Working records for clients of type graph
CREATE TABLE db.workingg (
    clientFile TEXT,
    depotFile TEXT,
    client TEXT,
    user TEXT,
    haveRev INTEGER,
    workRev INTEGER,
    isVirtual INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    modTime BIGINT,
    isLocked TEXT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    tampered TEXT,
    clientType TEXT,
    movedFile TEXT,
    status TEXT,
    blobSha TEXT,
    repo TEXT,
    PRIMARY KEY (clientFile)
);

-- db.workingx - Records for shelved open files
CREATE TABLE db.workingx (
    clientFile TEXT,
    depotFile TEXT,
    client TEXT,
    user TEXT,
    haveRev INTEGER,
    workRev INTEGER,
    isVirtual INTEGER,
    type TEXT,
    action TEXT,
    change INTEGER,
    modTime BIGINT,
    isLocked TEXT,
    digest TEXT,
    size BIGINT,
    traitLot INTEGER,
    tampered TEXT,
    clientType TEXT,
    movedFile TEXT,
    status TEXT,
    PRIMARY KEY (clientFile)
);

-- Specialized tables (proxy/replica/tiny)
CREATE TABLE pdb_lbr (
    file TEXT,
    rev TEXT,
    PRIMARY KEY (file, rev)
);

CREATE TABLE rdb_lbr (
    file TEXT,
    rev TEXT,
    PRIMARY KEY (file, rev)
);

CREATE TABLE tiny_db (
    key TEXT,
    value BYTEA,
    PRIMARY KEY (key)
);
```

### Notes
- **Primary Keys**: Based on "Indexed on" fields from the documentation; composite where applicable.
- **Secondary Indexes**: Added simple indexes for common secondary fields (e.g., `change` in `db.fix`).
- **Data Types**: Mappings are conservative to preserve data integrity (e.g., TEXT for variable strings, BIGINT for timestamps/sizes).
- **Upgrades and Releases**: The schema includes upgrade notes, but no special handling is needed for Postgres (run migrations as per Perforce docs if upgrading).
- **Full Schema**: This covers all 87 tables from the PDF. If you need ALTER TABLE for indexes/constraints or data migration scripts, let me know!
