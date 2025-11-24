```python
from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, DateTime, ForeignKey, Binary, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# perforce.bodresolve - Resolve data for stream specifications
class Bodresolve(Base):
    __tablename__ = 'bodresolve'
    __table_args__ = {'schema': 'perforce'}
    type = Column(String, primary_key=True)
    client = Column(String, primary_key=True)
    toKey = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    fromKey = Column(String, primary_key=True)
    fromChange = Column(Integer, primary_key=True)
    baseKey = Column(String)
    baseChange = Column(Integer)
    how = Column(String)
    state = Column(String)

# perforce.bodresolvex - Pending integration records for shelved stream specifications
class Bodresolvex(Base):
    __tablename__ = 'bodresolvex'
    __table_args__ = {'schema': 'perforce'}
    type = Column(String, primary_key=True)
    shelf = Column(Integer, primary_key=True)
    toKey = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    fromKey = Column(String, primary_key=True)
    fromChange = Column(Integer, primary_key=True)
    baseKey = Column(String)
    baseChange = Column(Integer)
    how = Column(String)
    state = Column(String)
    client = Column(String)

# perforce.bodtext - Job data for job attributes
class Bodtext(Base):
    __tablename__ = 'bodtext'
    __table_args__ = {'schema': 'perforce'}
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    isBulk = Column(Integer)
    text = Column(Text)

# perforce.bodtextcx - Versioned openable spec fields
class Bodtextcx(Base):
    __tablename__ = 'bodtextcx'
    __table_args__ = {'schema': 'perforce'}
    type = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)

# perforce.bodtexthx - Head revision of spec fields
class Bodtexthx(Base):
    __tablename__ = 'bodtexthx'
    __table_args__ = {'schema': 'perforce'}
    type = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    bulk = Column(Integer)
    text = Column(Text)

# perforce.bodtextsx - Shelved openable spec fields
class Bodtextsx(Base):
    __tablename__ = 'bodtextsx'
    __table_args__ = {'schema': 'perforce'}
    type = Column(Integer, primary_key=True)
    shelf = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)
    workChange = Column(Integer)
    user = Column(String)
    action = Column(String)

# perforce.bodtextwx - Open openable spec fields
class Bodtextwx(Base):
    __tablename__ = 'bodtextwx'
    __table_args__ = {'schema': 'perforce'}
    type = Column(Integer, primary_key=True)
    client = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)
    workChange = Column(Integer)
    user = Column(String)
    action = Column(String)

# perforce.change - Changelists
class Change(Base):
    __tablename__ = 'change'
    __table_args__ = {'schema': 'perforce'}
    change = Column(Integer, primary_key=True)
    descKey = Column(Integer)
    client = Column(String)
    user = Column(String)
    date = Column(BigInteger)
    status = Column(String)
    description = Column(Text)
    root = Column(String)
    importer = Column(String)
    identity = Column(String)
    access = Column(BigInteger)
    update = Column(BigInteger)
    stream = Column(String)

# perforce.changeidx - Secondary index of perforce.change/perforce.changex
class Changeidx(Base):
    __tablename__ = 'changeidx'
    __table_args__ = {'schema': 'perforce'}
    identity = Column(String, primary_key=True)
    change = Column(Integer)

# perforce.changex - Subset of perforce.change: records for pending changelists only
class Changex(Base):
    __tablename__ = 'changex'
    __table_args__ = {'schema': 'perforce'}
    change = Column(Integer, primary_key=True)
    descKey = Column(Integer)
    client = Column(String)
    user = Column(String)
    date = Column(BigInteger)
    status = Column(String)
    description = Column(Text)
    root = Column(String)
    importer = Column(String)
    identity = Column(String)
    access = Column(BigInteger)
    update = Column(BigInteger)
    stream = Column(String)

# perforce.ckphist - Stores history of checkpoint events
class Ckphist(Base):
    __tablename__ = 'ckphist'
    __table_args__ = {'schema': 'perforce'}
    start = Column(BigInteger, primary_key=True)
    jnum = Column(Integer, primary_key=True)
    who = Column(Integer, primary_key=True)
    type = Column(String, primary_key=True)
    end = Column(BigInteger)
    flags = Column(String)
    jfile = Column(String)
    jdate = Column(BigInteger)
    jdigest = Column(String)
    jsize = Column(BigInteger)
    jtype = Column(String)
    failed = Column(Integer)
    errmsg = Column(Binary)

# perforce.config - Server configurations table
class Config(Base):
    __tablename__ = 'config'
    __table_args__ = {'schema': 'perforce'}
    serverName = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    value = Column(String)

# perforce.configh - Server configuration history
class Configh(Base):
    __tablename__ = 'configh'
    __table_args__ = {'schema': 'perforce'}
    sName = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    server = Column(String, primary_key=True)
    user = Column(String)
    ovalue = Column(String)
    nvalue = Column(String)
    comment = Column(String)

# perforce.counters - Counters table
class Counters(Base):
    __tablename__ = 'counters'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    value = Column(String)

# perforce.depot - Depot specifications
class Depot(Base):
    __tablename__ = 'depot'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    type = Column(String)
    extra = Column(String)
    map = Column(String)
    objAddr = Column(String)

# perforce.desc - Change descriptions
class Desc(Base):
    __tablename__ = 'desc'
    __table_args__ = {'schema': 'perforce'}
    descKey = Column(Integer, primary_key=True)
    description = Column(Text)

# perforce.domain - Domains: depots, clients, labels, branches, streams, and typemap
class Domain(Base):
    __tablename__ = 'domain'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    type = Column(String)
    extra = Column(String)
    mount = Column(String)
    mount2 = Column(String)
    mount3 = Column(String)
    owner = Column(String)
    updateDate = Column(BigInteger)
    accessDate = Column(BigInteger)
    options = Column(String)
    description = Column(String)
    stream = Column(String)
    serverId = Column(String)
    contents = Column(Integer)

# perforce.excl - Exclusively locked (+l) files: enables coordinated file locking in commit/edge server environments
class Excl(Base):
    __tablename__ = 'excl'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    client = Column(String)
    user = Column(String)

# perforce.exclg - Graph depot LFS locks
class Exclg(Base):
    __tablename__ = 'exclg'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    file = Column(String, primary_key=True)
    lockId = Column(String)
    user = Column(String)
    created = Column(String)

# perforce.exclgx - Graph depot LFS locks indexed by lockId
class Exclgx(Base):
    __tablename__ = 'exclgx'
    __table_args__ = {'schema': 'perforce'}
    lockId = Column(String, primary_key=True)
    repo = Column(String)
    ref = Column(String)
    file = Column(String)
    user = Column(String)
    created = Column(String)

# perforce.fix - Fix records: indexed by job
class Fix(Base):
    __tablename__ = 'fix'
    __table_args__ = {'schema': 'perforce'}
    job = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    date = Column(BigInteger)
    status = Column(String)
    client = Column(String)
    user = Column(String)

# perforce.fixrev - Fix records: indexed by change
class Fixrev(Base):
    __tablename__ = 'fixrev'
    __table_args__ = {'schema': 'perforce'}
    change = Column(Integer, primary_key=True)
    job = Column(String, primary_key=True)
    date = Column(BigInteger)
    status = Column(String)
    client = Column(String)
    user = Column(String)

# perforce.graphindex - Graph depot repository index data
class Graphindex(Base):
    __tablename__ = 'graphindex'
    __table_args__ = {'schema': 'perforce'}
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    blobSha = Column(String, primary_key=True)
    commitSha = Column(String, primary_key=True)
    flags = Column(Integer)
    size = Column(BigInteger)
    type = Column(String)
    lfsoid = Column(String)

# perforce.graphperm - Graph depot permissions
class Graphperm(Base):
    __tablename__ = 'graphperm'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    user = Column(String, primary_key=True)
    perm = Column(String, primary_key=True)

# perforce.group - Group specifications
class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    group = Column(String, primary_key=True)
    type = Column(String)
    maxResults = Column(String)
    maxScanRows = Column(String)
    maxLockTime = Column(String)
    maxOpenFiles = Column(String)
    timeout = Column(Integer)
    passwordTimeout = Column(Integer)
    maxMemory = Column(String)
    idleTimeout = Column(Integer)

# perforce.groupx - Per-group data to support group membership controlled by AD/LDAP group membership
class Groupx(Base):
    __tablename__ = 'groupx'
    __table_args__ = {'schema': 'perforce'}
    group = Column(String, primary_key=True)
    ldapConf = Column(String)
    ldapSearchQuery = Column(String)
    ldapUserAttribute = Column(String)
    ldapDNAttribute = Column(String)
    description = Column(String)

# perforce.have - Contains the 'have-list' for all clients
class Have(Base):
    __tablename__ = 'have'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# perforce.have_pt - Placeholder for clients of types readonly, partitioned, and partitioned-jnl
class HavePt(Base):
    __tablename__ = 'have_pt'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# perforce.have_rp - Contains the 'have-list' for clients of build-server replicas
class HaveRp(Base):
    __tablename__ = 'have_rp'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# perforce.haveg - Contains the 'have-list' for graph depot files that are not at the same revision as defined by the client's have reference
class Haveg(Base):
    __tablename__ = 'haveg'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    client = Column(String)
    type = Column(String)
    action = Column(String)
    blobSha = Column(String)
    commitSha = Column(String)
    flags = Column(Integer)

# perforce.haveview - Stores mapping changes for clients mapping graph depot content
class Haveview(Base):
    __tablename__ = 'haveview'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# perforce.integed - Permanent integration records
class IntegEd(Base):
    __tablename__ = 'integed'
    __table_args__ = {'schema': 'perforce'}
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer, primary_key=True)
    startToRev = Column(Integer, primary_key=True)
    endToRev = Column(Integer, primary_key=True)
    how = Column(String)
    change = Column(Integer)

# perforce.integedss - Stream specification integration history
class IntegEdss(Base):
    __tablename__ = 'integedss'
    __table_args__ = {'schema': 'perforce'}
    toKey = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    fromKey = Column(String, primary_key=True)
    endfromChange = Column(Integer, primary_key=True)
    endtoChange = Column(Integer, primary_key=True)
    startfromChange = Column(Integer)
    starttoChange = Column(Integer)
    baseKey = Column(String)
    baseChange = Column(Integer)
    how = Column(String)
    change = Column(Integer)

# perforce.integtx - Temporary integration records used by task streams
class Integtx(Base):
    __tablename__ = 'integtx'
    __table_args__ = {'schema': 'perforce'}
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer, primary_key=True)
    startToRev = Column(Integer, primary_key=True)
    endToRev = Column(Integer, primary_key=True)
    how = Column(String)
    change = Column(Integer)

# perforce.ixtext - Indexing data for generic and job attributes
class Ixtext(Base):
    __tablename__ = 'ixtext'
    __table_args__ = {'schema': 'perforce'}
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# perforce.ixtexthx - Indexing data for head revision of all spec fields
class Ixtexthx(Base):
    __tablename__ = 'ixtexthx'
    __table_args__ = {'schema': 'perforce'}
    type = Column(String, primary_key=True)
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# perforce.jnlack - Tracks journal positions of all replicas
class Jnlack(Base):
    __tablename__ = 'jnlack'
    __table_args__ = {'schema': 'perforce'}
    serverId = Column(String, primary_key=True)
    lastUpdate = Column(BigInteger)
    serverType = Column(String)
    persistedJnl = Column(Integer)
    appliedJnl = Column(Integer)
    persistedPos = Column(BigInteger)
    appliedPos = Column(BigInteger)
    jcflags = Column(String)
    isAlive = Column(Integer)
    serverOptions = Column(String)
    failoverSeen = Column(String)

# perforce.job - Job records
class Job(Base):
    __tablename__ = 'job'
    __table_args__ = {'schema': 'perforce'}
    job = Column(String, primary_key=True)
    xuser = Column(String)
    xdate = Column(BigInteger)
    xstatus = Column(String)
    description = Column(Text)

# perforce.label - Revisions of files in labels
class Label(Base):
    __tablename__ = 'label'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    depotFile = Column(String, primary_key=True)
    haveRev = Column(Integer)

# perforce.ldap - LDAP specifications
class Ldap(Base):
    __tablename__ = 'ldap'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    ssl = Column(Integer)
    type = Column(Integer)
    pattern = Column(String)
    baseDN = Column(String)
    filter = Column(String)
    scope = Column(Integer)
    bindDN = Column(String)
    bindpass = Column(String)
    realm = Column(String)
    groupBaseDN = Column(String)
    groupFilter = Column(String)
    groupScope = Column(Integer)
    options = Column(Integer)
    attrUid = Column(String)
    attrEmail = Column(String)
    attrName = Column(String)

# perforce.locks - Locked/Unlocked files
class Locks(Base):
    __tablename__ = 'locks'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    client = Column(String, primary_key=True)
    user = Column(String)
    action = Column(String)
    isLocked = Column(String)
    change = Column(Integer)

# perforce.locksg - Lock records for clients of type graph
class Locksg(Base):
    __tablename__ = 'locksg'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    client = Column(String, primary_key=True)
    user = Column(String)
    action = Column(String)
    isLocked = Column(String)
    change = Column(Integer)

# perforce.logger - Support for 'p4 logger' command. Logs any changes to changelists and jobs.
class Logger(Base):
    __tablename__ = 'logger'
    __table_args__ = {'schema': 'perforce'}
    seq = Column(Integer, primary_key=True)
    key = Column(String)
    attr = Column(String)

# perforce.message - System messages
class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'schema': 'perforce'}
    language = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    message = Column(Text)

# perforce.monitor - P4 Server process information
class Monitor(Base):
    __tablename__ = 'monitor'
    __table_args__ = {'schema': 'perforce'}
    id = Column(Integer, primary_key=True)
    user = Column(String)
    function = Column(String)
    args = Column(String)
    startDate = Column(BigInteger)
    runstate = Column(Integer)
    client = Column(String)
    host = Column(String)
    prog = Column(String)
    lockInfo = Column(String)
    cmt = Column(String)
    ident = Column(String)

# perforce.nameval - A table to store key/value pairs
class Nameval(Base):
    __tablename__ = 'nameval'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    value = Column(String)

# perforce.object - Object storage for graph depots
class Object(Base):
    __tablename__ = 'object'
    __table_args__ = {'schema': 'perforce'}
    sha = Column(String, primary_key=True)
    type = Column(String)
    data = Column(Binary)
    refCount = Column(Integer)

# perforce.property - Properties
class Property(Base):
    __tablename__ = 'property'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    type = Column(String, primary_key=True)
    scope = Column(String, primary_key=True)
    value = Column(String)
    date = Column(BigInteger)
    user = Column(String)

# perforce.protect - The protections table
class Protect(Base):
    __tablename__ = 'protect'
    __table_args__ = {'schema': 'perforce'}
    seq = Column(Integer, primary_key=True)
    isGroup = Column(Integer)
    user = Column(String)
    host = Column(String)
    perm = Column(String)
    mapFlag = Column(String)
    depotFile = Column(String)
    subPath = Column(String)
    update = Column(BigInteger)

# perforce.pubkey - SSH Public keys
class Pubkey(Base):
    __tablename__ = 'pubkey'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    scope = Column(String, primary_key=True)
    key = Column(String)
    digest = Column(String)
    update = Column(BigInteger)

# perforce.ref - Reference content for graph depots
class Ref(Base):
    __tablename__ = 'ref'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    ref = Column(String)
    symref = Column(String)

# perforce.refcntadjust - Graph depot reference count adjustments
class Refcntadjust(Base):
    __tablename__ = 'refcntadjust'
    __table_args__ = {'schema': 'perforce'}
    walked = Column(Integer, primary_key=True)
    sha = Column(String, primary_key=True)
    adjustment = Column(Integer)
    adjustObject = Column(Integer)

# perforce.refhist - Reference history for graph depots
class Refhist(Base):
    __tablename__ = 'refhist'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    action = Column(String, primary_key=True)
    user = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    symref = Column(String)

# perforce.remote - Remote specifications
class Remote(Base):
    __tablename__ = 'remote'
    __table_args__ = {'schema': 'perforce'}
    id = Column(String, primary_key=True)
    owner = Column(String)
    options = Column(Integer)
    address = Column(String)
    desc = Column(String)
    update = Column(BigInteger)
    access = Column(BigInteger)
    fetch = Column(Integer)
    push = Column(Integer)
    rmtuser = Column(String)

# perforce.repo - Repository specifications
class Repo(Base):
    __tablename__ = 'repo'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    owner = Column(String)
    created = Column(BigInteger)
    pushed = Column(BigInteger)
    forked = Column(String)
    desc = Column(String)
    branch = Column(String)
    mirror = Column(String)
    options = Column(Integer)
    id = Column(Integer)
    gcmrrserver = Column(String)
    gcmrrsecrettoken = Column(String)
    gcmrrstatus = Column(Integer)
    gcmrrexcludedbranches = Column(String)
    gcmrrhidefetchurl = Column(Integer)

# perforce.resolve - Pending integration records
class Resolve(Base):
    __tablename__ = 'resolve'
    __table_args__ = {'schema': 'perforce'}
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer)
    startToRev = Column(Integer)
    endToRev = Column(Integer)
    how = Column(String)
    state = Column(String)
    baseFile = Column(String)
    baseRev = Column(Integer)

# perforce.resolveg - Resolve records for clients of type graph
class Resolveg(Base):
    __tablename__ = 'resolveg'
    __table_args__ = {'schema': 'perforce'}
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    baseSHA = Column(String, primary_key=True)
    wantsSHA = Column(String)
    how = Column(String)
    state = Column(String)

# perforce.resolvex - Pending integration records for shelved files
class Resolvex(Base):
    __tablename__ = 'resolvex'
    __table_args__ = {'schema': 'perforce'}
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer)
    startToRev = Column(Integer)
    endToRev = Column(Integer)
    how = Column(String)
    state = Column(String)
    baseFile = Column(String)
    baseRev = Column(Integer)

# perforce.rev - Revision records
class Rev(Base):
    __tablename__ = 'rev'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revbx - Revision records for archived files
class Revbx(Base):
    __tablename__ = 'revbx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revcx - Secondary index of perforce.rev
class Revcx(Base):
    __tablename__ = 'revcx'
    __table_args__ = {'schema': 'perforce'}
    change = Column(Integer, primary_key=True)
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer)
    action = Column(String)

# perforce.revdx - Revision records for revisions deleted at the head revision
class Revdx(Base):
    __tablename__ = 'revdx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revfs - Client filesystem file sizes
class Revfs(Base):
    __tablename__ = 'revfs'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    rev = Column(Integer, primary_key=True)
    clientType = Column(String, primary_key=True)
    clientSize = Column(BigInteger)

# perforce.revhx - Revision records for revisions NOT deleted at the head revision
class Revhx(Base):
    __tablename__ = 'revhx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.review - User's review mappings
class Review(Base):
    __tablename__ = 'review'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    depotFile = Column(String)
    type = Column(String)

# perforce.revpx - Pending revision records
class Revpx(Base):
    __tablename__ = 'revpx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revsh - Revision records for shelved files
class Revsh(Base):
    __tablename__ = 'revsh'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String, primary_key=True)
    action = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revstg - Temporary revision records for storage upgrade process
class Revstg(Base):
    __tablename__ = 'revstg'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revsx - Revision records for spec depot files
class Revsx(Base):
    __tablename__ = 'revsx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revtr - Rev table for huge traits
class Revtr(Base):
    __tablename__ = 'revtr'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revtx - Task stream revision records
class Revtx(Base):
    __tablename__ = 'revtx'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.revux - Revision records for unload depot files
class Revux(Base):
    __tablename__ = 'revux'
    __table_args__ = {'schema': 'perforce'}
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer, primary_key=True)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    date = Column(BigInteger)
    modTime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    lbrIsLazy = Column(String)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)

# perforce.rmtview - View data for remote specifications
class Rmtview(Base):
    __tablename__ = 'rmtview'
    __table_args__ = {'schema': 'perforce'}
    id = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    localFile = Column(String)
    remoteFile = Column(String)
    retain = Column(Integer)

# perforce.scanctl - ScanCtl
class Scanctl(Base):
    __tablename__ = 'scanctl'
    __table_args__ = {'schema': 'perforce'}
    depotPath = Column(String, primary_key=True)
    state = Column(String)
    seq = Column(Integer)
    dirs = Column(Integer)
    files = Column(Integer)
    zeros = Column(Integer)
    dirserr = Column(Integer)
    pri = Column(Integer)
    reqpause = Column(Integer)
    err = Column(String)
    filesnonlbr = Column(Integer)
    filesage = Column(Integer)
    report = Column(String)
    target = Column(String)
    flags = Column(String)
    reqage = Column(Integer)

# perforce.scandir - Scandir
class Scandir(Base):
    __tablename__ = 'scandir'
    __table_args__ = {'schema': 'perforce'}
    lskey = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    file = Column(String)

# perforce.sendq - Parallel file transmission work queue
class Sendq(Base):
    __tablename__ = 'sendq'
    __table_args__ = {'schema': 'perforce'}
    taskid = Column(Integer, primary_key=True)
    seq = Column(Integer, primary_key=True)
    handle = Column(String)
    depotFile = Column(String)
    clientFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    modtime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)
    flags = Column(Integer)
    clientType = Column(String)
    depotRev = Column(Integer)
    change = Column(Integer)
    date = Column(BigInteger)
    blobSha = Column(String)
    repoSlot = Column(Integer)
    shelveDigest = Column(String)
    olbrFile = Column(String)
    olbrRev = Column(String)
    olbrType = Column(String)

# perforce.sendq_pt - Per Client transmission work queue
class SendqPt(Base):
    __tablename__ = 'sendq_pt'
    __table_args__ = {'schema': 'perforce'}
    taskid = Column(Integer, primary_key=True)
    seq = Column(Integer, primary_key=True)
    handle = Column(String)
    depotFile = Column(String)
    clientFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    modtime = Column(BigInteger)
    digest = Column(String)
    size = Column(BigInteger)
    lbrFile = Column(String)
    lbrRev = Column(String)
    lbrType = Column(String)
    flags = Column(Integer)
    clientType = Column(String)
    depotRev = Column(Integer)
    change = Column(Integer)
    date = Column(BigInteger)
    blobSha = Column(String)
    repoSlot = Column(Integer)
    shelveDigest = Column(String)
    olbrFile = Column(String)
    olbrRev = Column(String)
    olbrType = Column(String)

# perforce.server - Server specifications
class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'schema': 'perforce'}
    id = Column(String, primary_key=True)
    type = Column(String)
    name = Column(String)
    address = Column(String)
    externalAddress = Column(String)
    services = Column(String)
    desc = Column(String)
    user = Column(String)
    options = Column(String)
    rplFrom = Column(String)
    failoverSeen = Column(String)

# perforce.stash - Stash data
class Stash(Base):
    __tablename__ = 'stash'
    __table_args__ = {'schema': 'perforce'}
    client = Column(String, primary_key=True)
    stream = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    change = Column(Integer)

# perforce.storage - Track references to archive files
class Storage(Base):
    __tablename__ = 'storage'
    __table_args__ = {'schema': 'perforce'}
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    digest = Column(String)
    size = Column(BigInteger)
    serverSize = Column(BigInteger)
    compCksum = Column(String)
    date = Column(BigInteger)

# perforce.storageg - Track references to Graph Depot archive files (for future use)
class Storageg(Base):
    __tablename__ = 'storageg'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    sha = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    date = Column(BigInteger)

# perforce.storagesh - Track references to shelved archive files
class Storagesh(Base):
    __tablename__ = 'storagesh'
    __table_args__ = {'schema': 'perforce'}
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    digest = Column(String)
    size = Column(BigInteger)
    serverSize = Column(BigInteger)
    compCksum = Column(String)
    date = Column(BigInteger)

# perforce.storagesx - Digest and filesize based index for perforce.storagesh, for finding shelved files with identical content
class Storagesx(Base):
    __tablename__ = 'storagesx'
    __table_args__ = {'schema': 'perforce'}
    digest = Column(String, primary_key=True)
    size = Column(BigInteger, primary_key=True)
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)

# perforce.stream - Stream specifications
class Stream(Base):
    __tablename__ = 'stream'
    __table_args__ = {'schema': 'perforce'}
    stream = Column(String, primary_key=True)
    parent = Column(String)
    title = Column(String)
    type = Column(String)
    preview = Column(BigInteger)
    change = Column(Integer)
    copyChange = Column(Integer)
    mergeChange = Column(Integer)
    highChange = Column(Integer)
    hash = Column(Integer)
    status = Column(String)
    parentview = Column(String)

# perforce.streamq - Track streams for which the stream views should be regenerated
class Streamq(Base):
    __tablename__ = 'streamq'
    __table_args__ = {'schema': 'perforce'}
    stream = Column(String, primary_key=True)

# perforce.streamrelation - Relationships between streams
class Streamrelation(Base):
    __tablename__ = 'streamrelation'
    __table_args__ = {'schema': 'perforce'}
    independentStream = Column(String, primary_key=True)
    dependentStream = Column(String, primary_key=True)
    type = Column(String)
    parentView = Column(String)

# perforce.streamview - Precomputed stream views
class Streamview(Base):
    __tablename__ = 'streamview'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# perforce.streamviewx - Indexing for precomputed stream views
class Streamviewx(Base):
    __tablename__ = 'streamviewx'
    __table_args__ = {'schema': 'perforce'}
    depotPath = Column(String, primary_key=True)
    viewPath = Column(String, primary_key=True)
    mapFlag = Column(String, primary_key=True)
    stream = Column(String, primary_key=True)
    change = Column(String)
    pathSource = Column(String)
    pathType = Column(String)
    componentPrefixes = Column(String)
    effectiveComponentType = Column(String)

# perforce.submodule - Submodule configuration data
class Submodule(Base):
    __tablename__ = 'submodule'
    __table_args__ = {'schema': 'perforce'}
    repo = Column(String, primary_key=True)
    path = Column(String, primary_key=True)
    subrepo = Column(String)

# perforce.svrview - View data for servers specifications
class Svrview(Base):
    __tablename__ = 'svrview'
    __table_args__ = {'schema': 'perforce'}
    id = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)

# perforce.template - Streams templates
class Template(Base):
    __tablename__ = 'template'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    seq = Column(Integer, primary_key=True)
    parent = Column(String)
    type = Column(String)
    path = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    changeMap = Column(String)

# perforce.templatesx - Shelved stream templates
class Templatesx(Base):
    __tablename__ = 'templatesx'
    __table_args__ = {'schema': 'perforce'}
    shelf = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    change = Column(Integer)
    parent = Column(String)
    type = Column(String)
    path = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    changeMap = Column(String)
    changeAtOpen = Column(Integer)
    user = Column(String)
    action = Column(String)

# perforce.templatewx - Pending stream templates
class Templatewx(Base):
    __tablename__ = 'templatewx'
    __table_args__ = {'schema': 'perforce'}
    client = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    change = Column(Integer)
    parent = Column(String)
    type = Column(String)
    path = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    changeMap = Column(String)
    changeAtOpen = Column(Integer)
    user = Column(String)
    action = Column(String)

# perforce.ticket - Second factor authentication state on a per user/host basis
class Ticket(Base):
    __tablename__ = 'ticket'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    host = Column(String, primary_key=True)
    ticket = Column(String)
    state = Column(String)
    token = Column(String)
    updateDate = Column(BigInteger)

# perforce.ticket_rp - Second factor authentication state on a per user/host basis (replica)
class TicketRp(Base):
    __tablename__ = 'ticket_rp'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    host = Column(String, primary_key=True)
    ticket = Column(String)
    state = Column(String)
    token = Column(String)
    updateDate = Column(BigInteger)

# perforce.topology - Topology information
class Topology(Base):
    __tablename__ = 'topology'
    __table_args__ = {'schema': 'perforce'}
    address = Column(String, primary_key=True)
    destAddress = Column(String, primary_key=True)
    serverID = Column(String, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    type = Column(String)
    encryption = Column(String)
    svcUser = Column(String)
    lastSeenDate = Column(BigInteger)
    svrRecType = Column(String)
    taddr = Column(String)
    tdaddr = Column(String)
    tid = Column(String)
    version = Column(String)

# perforce.traits - Attributes associated with file revisions
class Traits(Base):
    __tablename__ = 'traits'
    __table_args__ = {'schema': 'perforce'}
    traitLot = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    type = Column(String)
    value = Column(Binary)

# perforce.trigger - Trigger specifications
class Trigger(Base):
    __tablename__ = 'trigger'
    __table_args__ = {'schema': 'perforce'}
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    mapFlag = Column(String)
    depotFile = Column(String)
    triggerDepotFile = Column(String)
    trigger = Column(String)
    action = Column(String)

# perforce.upgrades - Store server upgrade info
class Upgrades(Base):
    __tablename__ = 'upgrades'
    __table_args__ = {'schema': 'perforce'}
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    startdate = Column(BigInteger)
    enddate = Column(BigInteger)
    info = Column(String)

# perforce.upgrades_rp - Store replica upgrade info
class UpgradesRp(Base):
    __tablename__ = 'upgrades_rp'
    __table_args__ = {'schema': 'perforce'}
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    startdate = Column(BigInteger)
    enddate = Column(BigInteger)
    info = Column(String)

# perforce.user - User specifications
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    email = Column(String)
    jobView = Column(String)
    updateDate = Column(BigInteger)
    accessDate = Column(BigInteger)
    fullName = Column(String)
    password = Column(String)
    strength = Column(String)
    ticket = Column(String)
    endDate = Column(BigInteger)
    type = Column(String)
    passDate = Column(BigInteger)
    passExpire = Column(BigInteger)
    attempts = Column(BigInteger)
    auth = Column(String)

# perforce.user_rp - Used by replica server's to store login information
class UserRp(Base):
    __tablename__ = 'user_rp'
    __table_args__ = {'schema': 'perforce'}
    user = Column(String, primary_key=True)
    email = Column(String)
    jobView = Column(String)
    updateDate = Column(BigInteger)
    accessDate = Column(BigInteger)
    fullName = Column(String)
    password = Column(String)
    strength = Column(String)
    ticket = Column(String)
    endDate = Column(BigInteger)
    type = Column(String)
    passDate = Column(BigInteger)
    passExpire = Column(BigInteger)
    attempts = Column(BigInteger)
    auth = Column(String)

# perforce.uxtext - Indexing data for P4 Code Review
class Uxtext(Base):
    __tablename__ = 'uxtext'
    __table_args__ = {'schema': 'perforce'}
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# perforce.view - View data for domain records
class View(Base):
    __tablename__ = 'view'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# perforce.view_rp - View data for clients of build-server replicas
class ViewRp(Base):
    __tablename__ = 'view_rp'
    __table_args__ = {'schema': 'perforce'}
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# perforce.working - Records for work in progress
class Working(Base):
    __tablename__ = 'working'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    client = Column(String)
    user = Column(String)
    haveRev = Column(Integer)
    workRev = Column(Integer)
    isVirtual = Column(Integer)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    modTime = Column(BigInteger)
    isLocked = Column(String)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    tampered = Column(String)
    clientType = Column(String)
    movedFile = Column(String)
    status = Column(String)

# perforce.workingg - Working records for clients of type graph
class Workingg(Base):
    __tablename__ = 'workingg'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    client = Column(String)
    user = Column(String)
    haveRev = Column(Integer)
    workRev = Column(Integer)
    isVirtual = Column(Integer)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    modTime = Column(BigInteger)
    isLocked = Column(String)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    tampered = Column(String)
    clientType = Column(String)
    movedFile = Column(String)
    status = Column(String)
    blobSha = Column(String)
    repo = Column(String)

# perforce.workingx - Records for shelved open files
class Workingx(Base):
    __tablename__ = 'workingx'
    __table_args__ = {'schema': 'perforce'}
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    client = Column(String)
    user = Column(String)
    haveRev = Column(Integer)
    workRev = Column(Integer)
    isVirtual = Column(Integer)
    type = Column(String)
    action = Column(String)
    change = Column(Integer)
    modTime = Column(BigInteger)
    isLocked = Column(String)
    digest = Column(String)
    size = Column(BigInteger)
    traitLot = Column(Integer)
    tampered = Column(String)
    clientType = Column(String)
    movedFile = Column(String)
    status = Column(String)

# Specialized tables (proxy/replica/tiny)
class PdbLbr(Base):
    __tablename__ = 'pdb_lbr'
    __table_args__ = {'schema': 'perforce'}
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)

class RdbLbr(Base):
    __tablename__ = 'rdb_lbr'
    __table_args__ = {'schema': 'perforce'}
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)

class TinyDb(Base):
    __tablename__ = 'tiny_db'
    __table_args__ = {'schema': 'perforce'}
    key = Column(String, primary_key=True)
    value = Column(Binary)
```
