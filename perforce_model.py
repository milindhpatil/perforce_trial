from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, DateTime, ForeignKey, Binary, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# db.bodresolve - Resolve data for stream specifications
class Bodresolve(Base):
    __tablename__ = 'db.bodresolve'
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

# db.bodresolvex - Pending integration records for shelved stream specifications
class Bodresolvex(Base):
    __tablename__ = 'db.bodresolvex'
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

# db.bodtext - Job data for job attributes
class Bodtext(Base):
    __tablename__ = 'db.bodtext'
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    isBulk = Column(Integer)
    text = Column(Text)

# db.bodtextcx - Versioned openable spec fields
class Bodtextcx(Base):
    __tablename__ = 'db.bodtextcx'
    type = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)

# db.bodtexthx - Head revision of spec fields
class Bodtexthx(Base):
    __tablename__ = 'db.bodtexthx'
    type = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    bulk = Column(Integer)
    text = Column(Text)

# db.bodtextsx - Shelved openable spec fields
class Bodtextsx(Base):
    __tablename__ = 'db.bodtextsx'
    type = Column(Integer, primary_key=True)
    shelf = Column(Integer, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)
    workChange = Column(Integer)
    user = Column(String)
    action = Column(String)

# db.bodtextwx - Open openable spec fields
class Bodtextwx(Base):
    __tablename__ = 'db.bodtextwx'
    type = Column(Integer, primary_key=True)
    client = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    text = Column(Text)
    workChange = Column(Integer)
    user = Column(String)
    action = Column(String)

# db.change - Changelists
class Change(Base):
    __tablename__ = 'db.change'
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

# db.changeidx - Secondary index of db.change/db.changex
class Changeidx(Base):
    __tablename__ = 'db.changeidx'
    identity = Column(String, primary_key=True)
    change = Column(Integer)

# db.changex - Subset of db.change: records for pending changelists only
class Changex(Base):
    __tablename__ = 'db.changex'
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

# db.ckphist - Stores history of checkpoint events
class Ckphist(Base):
    __tablename__ = 'db.ckphist'
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

# db.config - Server configurations table
class Config(Base):
    __tablename__ = 'db.config'
    serverName = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    value = Column(String)

# db.configh - Server configuration history
class Configh(Base):
    __tablename__ = 'db.configh'
    sName = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    version = Column(Integer, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    server = Column(String, primary_key=True)
    user = Column(String)
    ovalue = Column(String)
    nvalue = Column(String)
    comment = Column(String)

# db.counters - Counters table
class Counters(Base):
    __tablename__ = 'db.counters'
    name = Column(String, primary_key=True)
    value = Column(String)

# db.depot - Depot specifications
class Depot(Base):
    __tablename__ = 'db.depot'
    name = Column(String, primary_key=True)
    type = Column(String)
    extra = Column(String)
    map = Column(String)
    objAddr = Column(String)

# db.desc - Change descriptions
class Desc(Base):
    __tablename__ = 'db.desc'
    descKey = Column(Integer, primary_key=True)
    description = Column(Text)

# db.domain - Domains: depots, clients, labels, branches, streams, and typemap
class Domain(Base):
    __tablename__ = 'db.domain'
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

# db.excl - Exclusively locked (+l) files: enables coordinated file locking in commit/edge server environments
class Excl(Base):
    __tablename__ = 'db.excl'
    depotFile = Column(String, primary_key=True)
    client = Column(String)
    user = Column(String)

# db.exclg - Graph depot LFS locks
class Exclg(Base):
    __tablename__ = 'db.exclg'
    repo = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    file = Column(String, primary_key=True)
    lockId = Column(String)
    user = Column(String)
    created = Column(String)

# db.exclgx - Graph depot LFS locks indexed by lockId
class Exclgx(Base):
    __tablename__ = 'db.exclgx'
    lockId = Column(String, primary_key=True)
    repo = Column(String)
    ref = Column(String)
    file = Column(String)
    user = Column(String)
    created = Column(String)

# db.fix - Fix records: indexed by job
class Fix(Base):
    __tablename__ = 'db.fix'
    job = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    date = Column(BigInteger)
    status = Column(String)
    client = Column(String)
    user = Column(String)

# db.fixrev - Fix records: indexed by change
class Fixrev(Base):
    __tablename__ = 'db.fixrev'
    change = Column(Integer, primary_key=True)
    job = Column(String, primary_key=True)
    date = Column(BigInteger)
    status = Column(String)
    client = Column(String)
    user = Column(String)

# db.graphindex - Graph depot repository index data
class Graphindex(Base):
    __tablename__ = 'db.graphindex'
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    blobSha = Column(String, primary_key=True)
    commitSha = Column(String, primary_key=True)
    flags = Column(Integer)
    size = Column(BigInteger)
    type = Column(String)
    lfsoid = Column(String)

# db.graphperm - Graph depot permissions
class Graphperm(Base):
    __tablename__ = 'db.graphperm'
    name = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    user = Column(String, primary_key=True)
    perm = Column(String, primary_key=True)

# db.group - Group specifications
class Group(Base):
    __tablename__ = 'db.group'
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

# db.groupx - Per-group data to support group membership controlled by AD/LDAP group membership
class Groupx(Base):
    __tablename__ = 'db.groupx'
    group = Column(String, primary_key=True)
    ldapConf = Column(String)
    ldapSearchQuery = Column(String)
    ldapUserAttribute = Column(String)
    ldapDNAttribute = Column(String)
    description = Column(String)

# db.have - Contains the 'have-list' for all clients
class Have(Base):
    __tablename__ = 'db.have'
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# db.have.pt - Placeholder for clients of types readonly, partitioned, and partitioned-jnl
class HavePt(Base):
    __tablename__ = 'db.have.pt'
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# db.have.rp - Contains the 'have-list' for clients of build-server replicas
class HaveRp(Base):
    __tablename__ = 'db.have.rp'
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    haveRev = Column(Integer)
    type = Column(String)
    time = Column(BigInteger)

# db.haveg - Contains the 'have-list' for graph depot files that are not at the same revision as defined by the client's have reference
class Haveg(Base):
    __tablename__ = 'db.haveg'
    repo = Column(String, primary_key=True)
    clientFile = Column(String, primary_key=True)
    depotFile = Column(String)
    client = Column(String)
    type = Column(String)
    action = Column(String)
    blobSha = Column(String)
    commitSha = Column(String)
    flags = Column(Integer)

# db.haveview - Stores mapping changes for clients mapping graph depot content
class Haveview(Base):
    __tablename__ = 'db.haveview'
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# db.integed - Permanent integration records
class IntegEd(Base):
    __tablename__ = 'db.integed'
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer, primary_key=True)
    startToRev = Column(Integer, primary_key=True)
    endToRev = Column(Integer, primary_key=True)
    how = Column(String)
    change = Column(Integer)

# db.integedss - Stream specification integration history
class IntegEdss(Base):
    __tablename__ = 'db.integedss'
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

# db.integtx - Temporary integration records used by task streams
class Integtx(Base):
    __tablename__ = 'db.integtx'
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    startFromRev = Column(Integer, primary_key=True)
    endFromRev = Column(Integer, primary_key=True)
    startToRev = Column(Integer, primary_key=True)
    endToRev = Column(Integer, primary_key=True)
    how = Column(String)
    change = Column(Integer)

# db.ixtext - Indexing data for generic and job attributes
class Ixtext(Base):
    __tablename__ = 'db.ixtext'
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# db.ixtexthx - Indexing data for head revision of all spec fields
class Ixtexthx(Base):
    __tablename__ = 'db.ixtexthx'
    type = Column(String, primary_key=True)
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# db.jnlack - Tracks journal positions of all replicas
class Jnlack(Base):
    __tablename__ = 'db.jnlack'
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

# db.job - Job records
class Job(Base):
    __tablename__ = 'db.job'
    job = Column(String, primary_key=True)
    xuser = Column(String)
    xdate = Column(BigInteger)
    xstatus = Column(String)
    description = Column(Text)

# db.label - Revisions of files in labels
class Label(Base):
    __tablename__ = 'db.label'
    name = Column(String, primary_key=True)
    depotFile = Column(String, primary_key=True)
    haveRev = Column(Integer)

# db.ldap - LDAP specifications
class Ldap(Base):
    __tablename__ = 'db.ldap'
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

# db.locks - Locked/Unlocked files
class Locks(Base):
    __tablename__ = 'db.locks'
    depotFile = Column(String, primary_key=True)
    client = Column(String, primary_key=True)
    user = Column(String)
    action = Column(String)
    isLocked = Column(String)
    change = Column(Integer)

# db.locksg - Lock records for clients of type graph
class Locksg(Base):
    __tablename__ = 'db.locksg'
    depotFile = Column(String, primary_key=True)
    client = Column(String, primary_key=True)
    user = Column(String)
    action = Column(String)
    isLocked = Column(String)
    change = Column(Integer)

# db.logger - Support for 'p4 logger' command. Logs any changes to changelists and jobs.
class Logger(Base):
    __tablename__ = 'db.logger'
    seq = Column(Integer, primary_key=True)
    key = Column(String)
    attr = Column(String)

# db.message - System messages
class Message(Base):
    __tablename__ = 'db.message'
    language = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    message = Column(Text)

# db.monitor - P4 Server process information
class Monitor(Base):
    __tablename__ = 'db.monitor'
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

# db.nameval - A table to store key/value pairs
class Nameval(Base):
    __tablename__ = 'db.nameval'
    name = Column(String, primary_key=True)
    value = Column(String)

# db.object - Object storage for graph depots
class Object(Base):
    __tablename__ = 'db.object'
    sha = Column(String, primary_key=True)
    type = Column(String)
    data = Column(Binary)
    refCount = Column(Integer)

# db.property - Properties
class Property(Base):
    __tablename__ = 'db.property'
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    type = Column(String, primary_key=True)
    scope = Column(String, primary_key=True)
    value = Column(String)
    date = Column(BigInteger)
    user = Column(String)

# db.protect - The protections table
class Protect(Base):
    __tablename__ = 'db.protect'
    seq = Column(Integer, primary_key=True)
    isGroup = Column(Integer)
    user = Column(String)
    host = Column(String)
    perm = Column(String)
    mapFlag = Column(String)
    depotFile = Column(String)
    subPath = Column(String)
    update = Column(BigInteger)

# db.pubkey - SSH Public keys
class Pubkey(Base):
    __tablename__ = 'db.pubkey'
    user = Column(String, primary_key=True)
    scope = Column(String, primary_key=True)
    key = Column(String)
    digest = Column(String)
    update = Column(BigInteger)

# db.ref - Reference content for graph depots
class Ref(Base):
    __tablename__ = 'db.ref'
    repo = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    ref = Column(String)
    symref = Column(String)

# db.refcntadjust - Graph depot reference count adjustments
class Refcntadjust(Base):
    __tablename__ = 'db.refcntadjust'
    walked = Column(Integer, primary_key=True)
    sha = Column(String, primary_key=True)
    adjustment = Column(Integer)
    adjustObject = Column(Integer)

# db.refhist - Reference history for graph depots
class Refhist(Base):
    __tablename__ = 'db.refhist'
    repo = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    date = Column(BigInteger, primary_key=True)
    action = Column(String, primary_key=True)
    user = Column(String, primary_key=True)
    ref = Column(String, primary_key=True)
    symref = Column(String)

# db.remote - Remote specifications
class Remote(Base):
    __tablename__ = 'db.remote'
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

# db.repo - Repository specifications
class Repo(Base):
    __tablename__ = 'db.repo'
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

# db.resolve - Pending integration records
class Resolve(Base):
    __tablename__ = 'db.resolve'
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

# db.resolveg - Resolve records for clients of type graph
class Resolveg(Base):
    __tablename__ = 'db.resolveg'
    toFile = Column(String, primary_key=True)
    fromFile = Column(String, primary_key=True)
    baseSHA = Column(String, primary_key=True)
    wantsSHA = Column(String)
    how = Column(String)
    state = Column(String)

# db.resolvex - Pending integration records for shelved files
class Resolvex(Base):
    __tablename__ = 'db.resolvex'
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

# db.rev - Revision records
class Rev(Base):
    __tablename__ = 'db.rev'
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

# db.revbx - Revision records for archived files
class Revbx(Base):
    __tablename__ = 'db.revbx'
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

# db.revcx - Secondary index of db.rev
class Revcx(Base):
    __tablename__ = 'db.revcx'
    change = Column(Integer, primary_key=True)
    depotFile = Column(String, primary_key=True)
    depotRev = Column(Integer)
    action = Column(String)

# db.revdx - Revision records for revisions deleted at the head revision
class Revdx(Base):
    __tablename__ = 'db.revdx'
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

# db.revfs - Client filesystem file sizes
class Revfs(Base):
    __tablename__ = 'db.revfs'
    depotFile = Column(String, primary_key=True)
    rev = Column(Integer, primary_key=True)
    clientType = Column(String, primary_key=True)
    clientSize = Column(BigInteger)

# db.revhx - Revision records for revisions NOT deleted at the head revision
class Revhx(Base):
    __tablename__ = 'db.revhx'
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

# db.review - User's review mappings
class Review(Base):
    __tablename__ = 'db.review'
    user = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    depotFile = Column(String)
    type = Column(String)

# db.revpx - Pending revision records
class Revpx(Base):
    __tablename__ = 'db.revpx'
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

# db.revsh - Revision records for shelved files
class Revsh(Base):
    __tablename__ = 'db.revsh'
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

# db.revstg - Temporary revision records for storage upgrade process
class Revstg(Base):
    __tablename__ = 'db.revstg'
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

# db.revsx - Revision records for spec depot files
class Revsx(Base):
    __tablename__ = 'db.revsx'
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

# db.revtr - Rev table for huge traits
class Revtr(Base):
    __tablename__ = 'db.revtr'
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

# db.revtx - Task stream revision records
class Revtx(Base):
    __tablename__ = 'db.revtx'
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

# db.revux - Revision records for unload depot files
class Revux(Base):
    __tablename__ = 'db.revux'
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

# db.rmtview - View data for remote specifications
class Rmtview(Base):
    __tablename__ = 'db.rmtview'
    id = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    localFile = Column(String)
    remoteFile = Column(String)
    retain = Column(Integer)

# db.scanctl - ScanCtl
class Scanctl(Base):
    __tablename__ = 'db.scanctl'
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

# db.scandir - Scandir
class Scandir(Base):
    __tablename__ = 'db.scandir'
    lskey = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    file = Column(String)

# db.sendq - Parallel file transmission work queue
class Sendq(Base):
    __tablename__ = 'db.sendq'
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

# db.sendq.pt - Per Client transmission work queue
class SendqPt(Base):
    __tablename__ = 'db.sendq.pt'
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

# db.server - Server specifications
class Server(Base):
    __tablename__ = 'db.server'
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

# db.stash - Stash data
class Stash(Base):
    __tablename__ = 'db.stash'
    client = Column(String, primary_key=True)
    stream = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    change = Column(Integer)

# db.storage - Track references to archive files
class Storage(Base):
    __tablename__ = 'db.storage'
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    digest = Column(String)
    size = Column(BigInteger)
    serverSize = Column(BigInteger)
    compCksum = Column(String)
    date = Column(BigInteger)

# db.storageg - Track references to Graph Depot archive files (for future use)
class Storageg(Base):
    __tablename__ = 'db.storageg'
    repo = Column(String, primary_key=True)
    sha = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    date = Column(BigInteger)

# db.storagesh - Track references to shelved archive files
class Storagesh(Base):
    __tablename__ = 'db.storagesh'
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    refCount = Column(Integer)
    digest = Column(String)
    size = Column(BigInteger)
    serverSize = Column(BigInteger)
    compCksum = Column(String)
    date = Column(BigInteger)

# db.storagesx - Digest and filesize based index for db.storagesh, for finding shelved files with identical content
class Storagesx(Base):
    __tablename__ = 'db.storagesx'
    digest = Column(String, primary_key=True)
    size = Column(BigInteger, primary_key=True)
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)
    type = Column(String, primary_key=True)

# db.stream - Stream specifications
class Stream(Base):
    __tablename__ = 'db.stream'
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

# db.streamq - Track streams for which the stream views should be regenerated
class Streamq(Base):
    __tablename__ = 'db.streamq'
    stream = Column(String, primary_key=True)

# db.streamrelation - Relationships between streams
class Streamrelation(Base):
    __tablename__ = 'db.streamrelation'
    independentStream = Column(String, primary_key=True)
    dependentStream = Column(String, primary_key=True)
    type = Column(String)
    parentView = Column(String)

# db.streamview - Precomputed stream views
class Streamview(Base):
    __tablename__ = 'db.streamview'
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# db.streamviewx - Indexing for precomputed stream views
class Streamviewx(Base):
    __tablename__ = 'db.streamviewx'
    depotPath = Column(String, primary_key=True)
    viewPath = Column(String, primary_key=True)
    mapFlag = Column(String, primary_key=True)
    stream = Column(String, primary_key=True)
    change = Column(String)
    pathSource = Column(String)
    pathType = Column(String)
    componentPrefixes = Column(String)
    effectiveComponentType = Column(String)

# db.submodule - Submodule configuration data
class Submodule(Base):
    __tablename__ = 'db.submodule'
    repo = Column(String, primary_key=True)
    path = Column(String, primary_key=True)
    subrepo = Column(String)

# db.svrview - View data for servers specifications
class Svrview(Base):
    __tablename__ = 'db.svrview'
    id = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)

# db.template - Streams templates
class Template(Base):
    __tablename__ = 'db.template'
    name = Column(String, primary_key=True)
    change = Column(Integer, primary_key=True)
    seq = Column(Integer, primary_key=True)
    parent = Column(String)
    type = Column(String)
    path = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    changeMap = Column(String)

# db.templatesx - Shelved stream templates
class Templatesx(Base):
    __tablename__ = 'db.templatesx'
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

# db.templatewx - Pending stream templates
class Templatewx(Base):
    __tablename__ = 'db.templatewx'
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

# db.ticket - Second factor authentication state on a per user/host basis
class Ticket(Base):
    __tablename__ = 'db.ticket'
    user = Column(String, primary_key=True)
    host = Column(String, primary_key=True)
    ticket = Column(String)
    state = Column(String)
    token = Column(String)
    updateDate = Column(BigInteger)

# db.ticket.rp - Second factor authentication state on a per user/host basis (replica)
class TicketRp(Base):
    __tablename__ = 'db.ticket.rp'
    user = Column(String, primary_key=True)
    host = Column(String, primary_key=True)
    ticket = Column(String)
    state = Column(String)
    token = Column(String)
    updateDate = Column(BigInteger)

# db.topology - Topology information
class Topology(Base):
    __tablename__ = 'db.topology'
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

# db.traits - Attributes associated with file revisions
class Traits(Base):
    __tablename__ = 'db.traits'
    traitLot = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    type = Column(String)
    value = Column(Binary)

# db.trigger - Trigger specifications
class Trigger(Base):
    __tablename__ = 'db.trigger'
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    mapFlag = Column(String)
    depotFile = Column(String)
    triggerDepotFile = Column(String)
    trigger = Column(String)
    action = Column(String)

# db.upgrades - Store server upgrade info
class Upgrades(Base):
    __tablename__ = 'db.upgrades'
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    startdate = Column(BigInteger)
    enddate = Column(BigInteger)
    info = Column(String)

# db.upgrades.rp - Store replica upgrade info
class UpgradesRp(Base):
    __tablename__ = 'db.upgrades.rp'
    seq = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    startdate = Column(BigInteger)
    enddate = Column(BigInteger)
    info = Column(String)

# db.user - User specifications
class User(Base):
    __tablename__ = 'db.user'
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

# db.user.rp - Used by replica server's to store login information
class UserRp(Base):
    __tablename__ = 'db.user.rp'
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

# db.uxtext - Indexing data for P4 Code Review
class Uxtext(Base):
    __tablename__ = 'db.uxtext'
    word = Column(String, primary_key=True)
    attr = Column(Integer, primary_key=True)
    value = Column(String, primary_key=True)

# db.view - View data for domain records
class View(Base):
    __tablename__ = 'db.view'
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# db.view.rp - View data for clients of build-server replicas
class ViewRp(Base):
    __tablename__ = 'db.view.rp'
    name = Column(String, primary_key=True)
    seq = Column(Integer, primary_key=True)
    mapFlag = Column(String)
    viewFile = Column(String)
    depotFile = Column(String)
    comment = Column(String)

# db.working - Records for work in progress
class Working(Base):
    __tablename__ = 'db.working'
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

# db.workingg - Working records for clients of type graph
class Workingg(Base):
    __tablename__ = 'db.workingg'
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

# db.workingx - Records for shelved open files
class Workingx(Base):
    __tablename__ = 'db.workingx'
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
    __tablename__ = 'pdb.lbr'
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)

class RdbLbr(Base):
    __tablename__ = 'rdb.lbr'
    file = Column(String, primary_key=True)
    rev = Column(String, primary_key=True)

class TinyDb(Base):
    __tablename__ = 'tiny.db'
    key = Column(String, primary_key=True)
    value = Column(Binary)
