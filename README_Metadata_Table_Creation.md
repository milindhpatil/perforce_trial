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

### Updated PostgreSQL Schema Creation Script

Below is the modified SQL script incorporating:
1. `CREATE SCHEMA IF NOT EXISTS perforce;` at the beginning.
2. `CREATE TABLE IF NOT EXISTS` for all tables 

This ensures idempotency (safe to run multiple times without errors).

```sql
-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS perforce;

-- perforce.bodresolve - Resolve data for stream specifications
CREATE TABLE IF NOT EXISTS perforce.bodresolve (
    "type" TEXT,
    "client" TEXT,
    "toKey" TEXT,
    "attr" INTEGER,
    "fromKey" TEXT,
    "fromChange" INTEGER,
    "baseKey" TEXT,
    "baseChange" INTEGER,
    "how" TEXT,
    "state" TEXT,
    PRIMARY KEY ("type", "client", "toKey", "attr", "fromKey", "fromChange")
);

-- perforce.bodresolvex - Pending integration records for shelved stream specifications
CREATE TABLE IF NOT EXISTS perforce.bodresolvex (
    "type" TEXT,
    "shelf" INTEGER,
    "toKey" TEXT,
    "attr" INTEGER,
    "fromKey" TEXT,
    "fromChange" INTEGER,
    "baseKey" TEXT,
    "baseChange" INTEGER,
    "how" TEXT,
    "state" TEXT,
    "client" TEXT,
    PRIMARY KEY ("type", "shelf", "toKey", "attr", "fromKey", "fromChange")
);

-- perforce.bodtext - Job data for job attributes
CREATE TABLE IF NOT EXISTS perforce.bodtext (
    "key" TEXT,
    "attr" INTEGER,
    "isBulk" INTEGER,
    "text" TEXT,
    PRIMARY KEY ("key", "attr")
);

-- perforce.bodtextcx - Versioned openable spec fields
CREATE TABLE IF NOT EXISTS perforce.bodtextcx (
    "type" INTEGER,
    "key" TEXT,
    "change" INTEGER,
    "attr" INTEGER,
    "text" TEXT,
    PRIMARY KEY ("type", "key", "change", "attr")
);

-- perforce.bodtexthx - Head revision of spec fields
CREATE TABLE IF NOT EXISTS perforce.bodtexthx (
    "type" INTEGER,
    "key" TEXT,
    "attr" INTEGER,
    "bulk" INTEGER,
    "text" TEXT,
    PRIMARY KEY ("type", "key", "attr")
);

-- perforce.bodtextsx - Shelved openable spec fields
CREATE TABLE IF NOT EXISTS perforce.bodtextsx (
    "type" INTEGER,
    "shelf" INTEGER,
    "key" TEXT,
    "attr" INTEGER,
    "text" TEXT,
    "workChange" INTEGER,
    "user" TEXT,
    "action" TEXT,
    PRIMARY KEY ("type", "shelf", "key", "attr")
);

-- perforce.bodtextwx - Open openable spec fields
CREATE TABLE IF NOT EXISTS perforce.bodtextwx (
    "type" INTEGER,
    "client" TEXT,
    "key" TEXT,
    "attr" INTEGER,
    "text" TEXT,
    "workChange" INTEGER,
    "user" TEXT,
    "action" TEXT,
    PRIMARY KEY ("type", "client", "key", "attr")
);

-- perforce.change - Changelists
CREATE TABLE IF NOT EXISTS perforce.change (
    "change" INTEGER,
    "descKey" INTEGER,
    "client" TEXT,
    "user" TEXT,
    "date" BIGINT,
    "status" TEXT,
    "description" TEXT,
    "root" TEXT,
    "importer" TEXT,
    "identity" TEXT,
    "access" BIGINT,
    "update" BIGINT,
    "stream" TEXT,
    PRIMARY KEY ("change")
);
CREATE INDEX IF NOT EXISTS idx_perforce_change_identity ON perforce.change ("identity");

-- perforce.changeidx - Secondary index of perforce.change/perforce.changex
CREATE TABLE IF NOT EXISTS perforce.changeidx (
    "identity" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("identity")
);

-- perforce.changex - Subset of perforce.change: records for pending changelists only
CREATE TABLE IF NOT EXISTS perforce.changex (
    "change" INTEGER,
    "descKey" INTEGER,
    "client" TEXT,
    "user" TEXT,
    "date" BIGINT,
    "status" TEXT,
    "description" TEXT,
    "root" TEXT,
    "importer" TEXT,
    "identity" TEXT,
    "access" BIGINT,
    "update" BIGINT,
    "stream" TEXT,
    PRIMARY KEY ("change")
);

-- perforce.ckphist - Stores history of checkpoint events
CREATE TABLE IF NOT EXISTS perforce.ckphist (
    "start" BIGINT,
    "jnum" INTEGER,
    "who" INTEGER,
    "type" TEXT,
    "end" BIGINT,
    "flags" TEXT,
    "jfile" TEXT,
    "jdate" BIGINT,
    "jdigest" TEXT,
    "jsize" BIGINT,
    "jtype" TEXT,
    "failed" INTEGER,
    "errmsg" BYTEA,
    PRIMARY KEY ("start", "jnum", "type", "who")
);

-- perforce.config - Server configurations table
CREATE TABLE IF NOT EXISTS perforce.config (
    "serverName" TEXT,
    "name" TEXT,
    "value" TEXT,
    PRIMARY KEY ("serverName", "name")
);

-- perforce.configh - Server configuration history
CREATE TABLE IF NOT EXISTS perforce.configh (
    "sName" TEXT,
    "name" TEXT,
    "version" INTEGER,
    "date" BIGINT,
    "server" TEXT,
    "user" TEXT,
    "ovalue" TEXT,
    "nvalue" TEXT,
    "comment" TEXT,
    PRIMARY KEY ("sName", "name", "version", "date", "server")
);

-- perforce.counters - Counters table
CREATE TABLE IF NOT EXISTS perforce.counters (
    "name" TEXT,
    "value" TEXT,
    PRIMARY KEY ("name")
);

-- perforce.depot - Depot specifications
CREATE TABLE IF NOT EXISTS perforce.depot (
    "name" TEXT,
    "type" TEXT,
    "extra" TEXT,
    "map" TEXT,
    "objAddr" TEXT,
    PRIMARY KEY ("name")
);

-- perforce.desc - Change descriptions
CREATE TABLE IF NOT EXISTS perforce.desc (
    "descKey" INTEGER,
    "description" TEXT,
    PRIMARY KEY ("descKey")
);

-- perforce.domain - Domains: depots, clients, labels, branches, streams, and typemap
CREATE TABLE IF NOT EXISTS perforce.domain (
    "name" TEXT,
    "type" TEXT,
    "extra" TEXT,
    "mount" TEXT,
    "mount2" TEXT,
    "mount3" TEXT,
    "owner" TEXT,
    "updateDate" BIGINT,
    "accessDate" BIGINT,
    "options" TEXT,
    "description" TEXT,
    "stream" TEXT,
    "serverId" TEXT,
    "contents" INTEGER,
    PRIMARY KEY ("name")
);

-- perforce.excl - Exclusively locked (+l) files: enables coordinated file locking in commit/edge server environments
CREATE TABLE IF NOT EXISTS perforce.excl (
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    PRIMARY KEY ("depotFile")
);

-- perforce.exclg - Graph depot LFS locks
CREATE TABLE IF NOT EXISTS perforce.exclg (
    "repo" TEXT,
    "ref" TEXT,
    "file" TEXT,
    "lockId" TEXT,
    "user" TEXT,
    "created" TEXT,
    PRIMARY KEY ("repo", "ref", "file")
);

-- perforce.exclgx - Graph depot LFS locks indexed by lockId
CREATE TABLE IF NOT EXISTS perforce.exclgx (
    "lockId" TEXT,
    "repo" TEXT,
    "ref" TEXT,
    "file" TEXT,
    "user" TEXT,
    "created" TEXT,
    PRIMARY KEY ("lockId")
);

-- perforce.fix - Fix records: indexed by job
CREATE TABLE IF NOT EXISTS perforce.fix (
    "job" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "status" TEXT,
    "client" TEXT,
    "user" TEXT,
    PRIMARY KEY ("job", "change")
);
CREATE INDEX IF NOT EXISTS idx_perforce_fix_change ON perforce.fix ("change");

-- perforce.fixrev - Fix records: indexed by change
CREATE TABLE IF NOT EXISTS perforce.fixrev (
    "job" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "status" TEXT,
    "client" TEXT,
    "user" TEXT,
    PRIMARY KEY ("change", "job")
);

-- perforce.graphindex - Graph depot repository index data
CREATE TABLE IF NOT EXISTS perforce.graphindex (
    "id" INTEGER,
    "name" TEXT,
    "date" BIGINT,
    "blobSha" TEXT,
    "commitSha" TEXT,
    "flags" INTEGER,
    "size" BIGINT,
    "type" TEXT,
    "lfsoid" TEXT,
    PRIMARY KEY ("id", "name", "date", "blobSha", "commitSha")
);

-- perforce.graphperm - Graph depot permissions
CREATE TABLE IF NOT EXISTS perforce.graphperm (
    "name" TEXT,
    "repo" TEXT,
    "ref" TEXT,
    "type" TEXT,
    "user" TEXT,
    "perm" TEXT,
    PRIMARY KEY ("name", "repo", "ref", "type", "user", "perm")
);

-- perforce.group - Group specifications
CREATE TABLE IF NOT EXISTS perforce.group (
    "user" TEXT,
    "group" TEXT,
    "type" TEXT,
    "maxResults" TEXT,
    "maxScanRows" TEXT,
    "maxLockTime" TEXT,
    "maxOpenFiles" TEXT,
    "timeout" INTEGER,
    "passwordTimeout" INTEGER,
    "maxMemory" TEXT,
    "idleTimeout" INTEGER,
    PRIMARY KEY ("user", "group")
);

-- perforce.groupx - Per-group data to support group membership controlled by AD/LDAP group membership
CREATE TABLE IF NOT EXISTS perforce.groupx (
    "group" TEXT,
    "ldapConf" TEXT,
    "ldapSearchQuery" TEXT,
    "ldapUserAttribute" TEXT,
    "ldapDNAttribute" TEXT,
    "description" TEXT,
    PRIMARY KEY ("group")
);

-- perforce.have - Contains the 'have-list' for all clients
CREATE TABLE IF NOT EXISTS perforce.have (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "haveRev" INTEGER,
    "type" TEXT,
    "time" BIGINT,
    PRIMARY KEY ("clientFile")
);

-- perforce.have_pt - Placeholder for clients of types readonly, partitioned, and partitioned-jnl
CREATE TABLE IF NOT EXISTS perforce.have_pt (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "haveRev" INTEGER,
    "type" TEXT,
    "time" BIGINT,
    PRIMARY KEY ("clientFile")
);

-- perforce.have_rp - Contains the 'have-list' for clients of build-server replicas
CREATE TABLE IF NOT EXISTS perforce.have_rp (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "haveRev" INTEGER,
    "type" TEXT,
    "time" BIGINT,
    PRIMARY KEY ("clientFile")
);

-- perforce.haveg - Contains the 'have-list' for graph depot files that are not at the same revision as defined by the client's have reference
CREATE TABLE IF NOT EXISTS perforce.haveg (
    "repo" TEXT,
    "clientFile" TEXT,
    "depotFile" TEXT,
    "client" TEXT,
    "type" TEXT,
    "action" TEXT,
    "blobSha" TEXT,
    "commitSha" TEXT,
    "flags" INTEGER,
    PRIMARY KEY ("repo", "clientFile")
);

-- perforce.haveview - Stores mapping changes for clients mapping graph depot content
CREATE TABLE IF NOT EXISTS perforce.haveview (
    "name" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "comment" TEXT,
    PRIMARY KEY ("name", "seq")
);

-- perforce.integed - Permanent integration records
CREATE TABLE IF NOT EXISTS perforce.integed (
    "toFile" TEXT,
    "fromFile" TEXT,
    "startFromRev" INTEGER,
    "endFromRev" INTEGER,
    "startToRev" INTEGER,
    "endToRev" INTEGER,
    "how" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("toFile", "fromFile", "startFromRev", "endFromRev", "startToRev", "endToRev")
);

-- perforce.integedss - Stream specification integration history
CREATE TABLE IF NOT EXISTS perforce.integedss (
    "toKey" TEXT,
    "attr" INTEGER,
    "fromKey" TEXT,
    "endfromChange" INTEGER,
    "endtoChange" INTEGER,
    "startfromChange" INTEGER,
    "starttoChange" INTEGER,
    "baseKey" TEXT,
    "baseChange" INTEGER,
    "how" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("toKey", "attr", "fromKey", "endfromChange", "endtoChange")
);

-- perforce.integtx - Temporary integration records used by task streams
CREATE TABLE IF NOT EXISTS perforce.integtx (
    "toFile" TEXT,
    "fromFile" TEXT,
    "startFromRev" INTEGER,
    "endFromRev" INTEGER,
    "startToRev" INTEGER,
    "endToRev" INTEGER,
    "how" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("toFile", "fromFile", "startFromRev", "endFromRev", "startToRev", "endToRev")
);

-- perforce.ixtext - Indexing data for generic and job attributes
CREATE TABLE IF NOT EXISTS perforce.ixtext (
    "word" TEXT,
    "attr" INTEGER,
    "value" TEXT,
    PRIMARY KEY ("word", "attr", "value")
);

-- perforce.ixtexthx - Indexing data for head revision of all spec fields
CREATE TABLE IF NOT EXISTS perforce.ixtexthx (
    "type" TEXT,
    "word" TEXT,
    "attr" INTEGER,
    "value" TEXT,
    PRIMARY KEY ("type", "word", "attr", "value")
);

-- perforce.jnlack - Tracks journal positions of all replicas
CREATE TABLE IF NOT EXISTS perforce.jnlack (
    "serverId" TEXT,
    "lastUpdate" BIGINT,
    "serverType" TEXT,
    "persistedJnl" INTEGER,
    "appliedJnl" INTEGER,
    "persistedPos" BIGINT,
    "appliedPos" BIGINT,
    "jcflags" TEXT,
    "isAlive" INTEGER,
    "serverOptions" TEXT,
    "failoverSeen" TEXT,
    PRIMARY KEY ("serverId")
);

-- perforce.job - Job records
CREATE TABLE IF NOT EXISTS perforce.job (
    "job" TEXT,
    "xuser" TEXT,
    "xdate" BIGINT,
    "xstatus" TEXT,
    "description" TEXT,
    PRIMARY KEY ("job")
);

-- perforce.label - Revisions of files in labels
CREATE TABLE IF NOT EXISTS perforce.label (
    "name" TEXT,
    "depotFile" TEXT,
    "haveRev" INTEGER,
    PRIMARY KEY ("name", "depotFile")
);

-- perforce.ldap - LDAP specifications
CREATE TABLE IF NOT EXISTS perforce.ldap (
    "name" TEXT,
    "host" TEXT,
    "port" INTEGER,
    "ssl" INTEGER,
    "type" INTEGER,
    "pattern" TEXT,
    "baseDN" TEXT,
    "filter" TEXT,
    "scope" INTEGER,
    "bindDN" TEXT,
    "bindpass" TEXT,
    "realm" TEXT,
    "groupBaseDN" TEXT,
    "groupFilter" TEXT,
    "groupScope" INTEGER,
    "options" INTEGER,
    "attrUid" TEXT,
    "attrEmail" TEXT,
    "attrName" TEXT,
    PRIMARY KEY ("name")
);

-- perforce.locks - Locked/Unlocked files
CREATE TABLE IF NOT EXISTS perforce.locks (
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    "action" TEXT,
    "isLocked" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("depotFile", "client")
);

-- perforce.locksg - Lock records for clients of type graph
CREATE TABLE IF NOT EXISTS perforce.locksg (
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    "action" TEXT,
    "isLocked" TEXT,
    "change" INTEGER,
    PRIMARY KEY ("depotFile", "client")
);

-- perforce.logger - Support for 'p4 logger' command. Logs any changes to changelists and jobs.
CREATE TABLE IF NOT EXISTS perforce.logger (
    "seq" INTEGER,
    "key" TEXT,
    "attr" TEXT,
    PRIMARY KEY ("seq")
);

-- perforce.message - System messages
CREATE TABLE IF NOT EXISTS perforce.message (
    "language" TEXT,
    "id" INTEGER,
    "message" TEXT,
    PRIMARY KEY ("language", "id")
);

-- perforce.monitor - P4 Server process information
CREATE TABLE IF NOT EXISTS perforce.monitor (
    "id" INTEGER,
    "user" TEXT,
    "function" TEXT,
    "args" TEXT,
    "startDate" BIGINT,
    "runstate" INTEGER,
    "client" TEXT,
    "host" TEXT,
    "prog" TEXT,
    "lockInfo" TEXT,
    "cmt" TEXT,
    "ident" TEXT,
    PRIMARY KEY ("id")
);

-- perforce.nameval - A table to store key/value pairs
CREATE TABLE IF NOT EXISTS perforce.nameval (
    "name" TEXT,
    "value" TEXT,
    PRIMARY KEY ("name")
);

-- perforce.object - Object storage for graph depots
CREATE TABLE IF NOT EXISTS perforce.object (
    "sha" TEXT,
    "type" TEXT,
    "data" BYTEA,
    "refCount" INTEGER,
    PRIMARY KEY ("sha")
);

-- perforce.property - Properties
CREATE TABLE IF NOT EXISTS perforce.property (
    "name" TEXT,
    "seq" INTEGER,
    "type" TEXT,
    "scope" TEXT,
    "value" TEXT,
    "date" BIGINT,
    "user" TEXT,
    PRIMARY KEY ("name", "seq", "type", "scope")
);

-- perforce.protect - The protections table
CREATE TABLE IF NOT EXISTS perforce.protect (
    "seq" INTEGER,
    "isGroup" INTEGER,
    "user" TEXT,
    "host" TEXT,
    "perm" TEXT,
    "mapFlag" TEXT,
    "depotFile" TEXT,
    "subPath" TEXT,
    "update" BIGINT,
    PRIMARY KEY ("seq")
);

-- perforce.pubkey - SSH Public keys
CREATE TABLE IF NOT EXISTS perforce.pubkey (
    "user" TEXT,
    "scope" TEXT,
    "key" TEXT,
    "digest" TEXT,
    "update" BIGINT,
    PRIMARY KEY ("user", "scope")
);

-- perforce.ref - Reference content for graph depots
CREATE TABLE IF NOT EXISTS perforce.ref (
    "repo" TEXT,
    "type" TEXT,
    "name" TEXT,
    "ref" TEXT,
    "symref" TEXT,
    PRIMARY KEY ("repo", "type", "name")
);

-- perforce.refcntadjust - Graph depot reference count adjustments
CREATE TABLE IF NOT EXISTS perforce.refcntadjust (
    "walked" INTEGER,
    "sha" TEXT,
    "adjustment" INTEGER,
    "adjustObject" INTEGER,
    PRIMARY KEY ("walked", "sha")
);

-- perforce.refhist - Reference history for graph depots
CREATE TABLE IF NOT EXISTS perforce.refhist (
    "repo" TEXT,
    "type" TEXT,
    "name" TEXT,
    "date" BIGINT,
    "action" TEXT,
    "user" TEXT,
    "ref" TEXT,
    "symref" TEXT,
    PRIMARY KEY ("repo", "type", "name", "date", "action", "user", "ref")
);

-- perforce.remote - Remote specifications
CREATE TABLE IF NOT EXISTS perforce.remote (
    "id" TEXT,
    "owner" TEXT,
    "options" INTEGER,
    "address" TEXT,
    "desc" TEXT,
    "update" BIGINT,
    "access" BIGINT,
    "fetch" INTEGER,
    "push" INTEGER,
    "rmtuser" TEXT,
    PRIMARY KEY ("id")
);

-- perforce.repo - Repository specifications
CREATE TABLE IF NOT EXISTS perforce.repo (
    "repo" TEXT,
    "owner" TEXT,
    "created" BIGINT,
    "pushed" BIGINT,
    "forked" TEXT,
    "desc" TEXT,
    "branch" TEXT,
    "mirror" TEXT,
    "options" INTEGER,
    "id" INTEGER,
    "gcmrrserver" TEXT,
    "gcmrrsecrettoken" TEXT,
    "gcmrrstatus" INTEGER,
    "gcmrrexcludedbranches" TEXT,
    "gcmrrhidefetchurl" INTEGER,
    PRIMARY KEY ("repo")
);

-- perforce.resolve - Pending integration records
CREATE TABLE IF NOT EXISTS perforce.resolve (
    "toFile" TEXT,
    "fromFile" TEXT,
    "startFromRev" INTEGER,
    "endFromRev" INTEGER,
    "startToRev" INTEGER,
    "endToRev" INTEGER,
    "how" TEXT,
    "state" TEXT,
    "baseFile" TEXT,
    "baseRev" INTEGER,
    PRIMARY KEY ("toFile", "fromFile", "startFromRev")
);

-- perforce.resolveg - Resolve records for clients of type graph
CREATE TABLE IF NOT EXISTS perforce.resolveg (
    "toFile" TEXT,
    "fromFile" TEXT,
    "baseSHA" TEXT,
    "wantsSHA" TEXT,
    "how" TEXT,
    "state" TEXT,
    PRIMARY KEY ("toFile", "fromFile", "baseSHA")
);

-- perforce.resolvex - Pending integration records for shelved files
CREATE TABLE IF NOT EXISTS perforce.resolvex (
    "toFile" TEXT,
    "fromFile" TEXT,
    "startFromRev" INTEGER,
    "endFromRev" INTEGER,
    "startToRev" INTEGER,
    "endToRev" INTEGER,
    "how" TEXT,
    "state" TEXT,
    "baseFile" TEXT,
    "baseRev" INTEGER,
    PRIMARY KEY ("toFile", "fromFile", "startFromRev")
);

-- perforce.rev - Revision records
CREATE TABLE IF NOT EXISTS perforce.rev (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revbx - Revision records for archived files
CREATE TABLE IF NOT EXISTS perforce.revbx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revcx - Secondary index of perforce.rev
CREATE TABLE IF NOT EXISTS perforce.revcx (
    "change" INTEGER,
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "action" TEXT,
    PRIMARY KEY ("change", "depotFile")
);

-- perforce.revdx - Revision records for revisions deleted at the head revision
CREATE TABLE IF NOT EXISTS perforce.revdx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile")
);

-- perforce.revfs - Client filesystem file sizes
CREATE TABLE IF NOT EXISTS perforce.revfs (
    "depotFile" TEXT,
    "rev" INTEGER,
    "clientType" TEXT,
    "clientSize" BIGINT,
    PRIMARY KEY ("depotFile", "rev", "clientType")
);

-- perforce.revhx - Revision records for revisions NOT deleted at the head revision
CREATE TABLE IF NOT EXISTS perforce.revhx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile")
);

-- perforce.review - User's review mappings
CREATE TABLE IF NOT EXISTS perforce.review (
    "user" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "depotFile" TEXT,
    "type" TEXT,
    PRIMARY KEY ("user", "seq")
);

-- perforce.revpx - Pending revision records
CREATE TABLE IF NOT EXISTS perforce.revpx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revsh - Revision records for shelved files
CREATE TABLE IF NOT EXISTS perforce.revsh (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev", "type", "action", "change")
);

-- perforce.revstg - Temporary revision records for storage upgrade process
CREATE TABLE IF NOT EXISTS perforce.revstg (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revsx - Revision records for spec depot files
CREATE TABLE IF NOT EXISTS perforce.revsx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revtr - Rev table for huge traits
CREATE TABLE IF NOT EXISTS perforce.revtr (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revtx - Task stream revision records
CREATE TABLE IF NOT EXISTS perforce.revtx (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.revux - Revision records for unload depot files
CREATE TABLE IF NOT EXISTS perforce.revux (
    "depotFile" TEXT,
    "depotRev" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "date" BIGINT,
    "modTime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "lbrIsLazy" TEXT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    PRIMARY KEY ("depotFile", "depotRev")
);

-- perforce.rmtview - View data for remote specifications
CREATE TABLE IF NOT EXISTS perforce.rmtview (
    "id" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "localFile" TEXT,
    "remoteFile" TEXT,
    "retain" INTEGER,
    PRIMARY KEY ("id", "seq")
);

-- perforce.scanctl - ScanCtl
CREATE TABLE IF NOT EXISTS perforce.scanctl (
    "depotPath" TEXT,
    "state" TEXT,
    "seq" INTEGER,
    "dirs" INTEGER,
    "files" INTEGER,
    "zeros" INTEGER,
    "dirserr" INTEGER,
    "pri" INTEGER,
    "reqpause" INTEGER,
    "err" TEXT,
    "filesnonlbr" INTEGER,
    "filesage" INTEGER,
    "report" TEXT,
    "target" TEXT,
    "flags" TEXT,
    "reqage" INTEGER,
    PRIMARY KEY ("depotPath")
);

-- perforce.scandir - Scandir
CREATE TABLE IF NOT EXISTS perforce.scandir (
    "lskey" TEXT,
    "seq" INTEGER,
    "file" TEXT,
    PRIMARY KEY ("lskey", "seq")
);

-- perforce.sendq - Parallel file transmission work queue
CREATE TABLE IF NOT EXISTS perforce.sendq (
    "taskid" INTEGER,
    "seq" INTEGER,
    "handle" TEXT,
    "depotFile" TEXT,
    "clientFile" TEXT,
    "haveRev" INTEGER,
    "type" TEXT,
    "modtime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    "flags" INTEGER,
    "clientType" TEXT,
    "depotRev" INTEGER,
    "change" INTEGER,
    "date" BIGINT,
    "blobSha" TEXT,
    "repoSlot" INTEGER,
    "shelveDigest" TEXT,
    "olbrFile" TEXT,
    "olbrRev" TEXT,
    "olbrType" TEXT,
    PRIMARY KEY ("taskid", "seq")
);

-- perforce.sendq_pt - Per Client transmission work queue
CREATE TABLE IF NOT EXISTS perforce.sendq_pt (
    "taskid" INTEGER,
    "seq" INTEGER,
    "handle" TEXT,
    "depotFile" TEXT,
    "clientFile" TEXT,
    "haveRev" INTEGER,
    "type" TEXT,
    "modtime" BIGINT,
    "digest" TEXT,
    "size" BIGINT,
    "lbrFile" TEXT,
    "lbrRev" TEXT,
    "lbrType" TEXT,
    "flags" INTEGER,
    "clientType" TEXT,
    "depotRev" INTEGER,
    "change" INTEGER,
    "date" BIGINT,
    "blobSha" TEXT,
    "repoSlot" INTEGER,
    "shelveDigest" TEXT,
    "olbrFile" TEXT,
    "olbrRev" TEXT,
    "olbrType" TEXT,
    PRIMARY KEY ("taskid", "seq")
);

-- perforce.server - Server specifications
CREATE TABLE IF NOT EXISTS perforce.server (
    "id" TEXT,
    "type" TEXT,
    "name" TEXT,
    "address" TEXT,
    "externalAddress" TEXT,
    "services" TEXT,
    "desc" TEXT,
    "user" TEXT,
    "options" TEXT,
    "rplFrom" TEXT,
    "failoverSeen" TEXT,
    PRIMARY KEY ("id")
);

-- perforce.stash - Stash data
CREATE TABLE IF NOT EXISTS perforce.stash (
    "client" TEXT,
    "stream" TEXT,
    "type" TEXT,
    "seq" INTEGER,
    "change" INTEGER,
    PRIMARY KEY ("client", "stream", "type", "seq")
);

-- perforce.storage - Track references to archive files
CREATE TABLE IF NOT EXISTS perforce.storage (
    "file" TEXT,
    "rev" TEXT,
    "type" TEXT,
    "refCount" INTEGER,
    "digest" TEXT,
    "size" BIGINT,
    "serverSize" BIGINT,
    "compCksum" TEXT,
    "date" BIGINT,
    PRIMARY KEY ("file", "rev", "type")
);

-- perforce.storageg - Track references to Graph Depot archive files (for future use)
CREATE TABLE IF NOT EXISTS perforce.storageg (
    "repo" TEXT,
    "sha" TEXT,
    "type" TEXT,
    "refCount" INTEGER,
    "date" BIGINT,
    PRIMARY KEY ("repo", "sha", "type")
);

-- perforce.storagesh - Track references to shelved archive files
CREATE TABLE IF NOT EXISTS perforce.storagesh (
    "file" TEXT,
    "rev" TEXT,
    "type" TEXT,
    "refCount" INTEGER,
    "digest" TEXT,
    "size" BIGINT,
    "serverSize" BIGINT,
    "compCksum" TEXT,
    "date" BIGINT,
    PRIMARY KEY ("file", "rev", "type")
);

-- perforce.storagesx - Digest and filesize based index for perforce.storagesh, for finding shelved files with identical content
CREATE TABLE IF NOT EXISTS perforce.storagesx (
    "digest" TEXT,
    "size" BIGINT,
    "file" TEXT,
    "rev" TEXT,
    "type" TEXT,
    PRIMARY KEY ("digest", "size", "file", "rev", "type")
);

-- perforce.stream - Stream specifications
CREATE TABLE IF NOT EXISTS perforce.stream (
    "stream" TEXT,
    "parent" TEXT,
    "title" TEXT,
    "type" TEXT,
    "preview" BIGINT,
    "change" INTEGER,
    "copyChange" INTEGER,
    "mergeChange" INTEGER,
    "highChange" INTEGER,
    "hash" INTEGER,
    "status" TEXT,
    "parentview" TEXT,
    PRIMARY KEY ("stream")
);

-- perforce.streamq - Track streams for which the stream views should be regenerated
CREATE TABLE IF NOT EXISTS perforce.streamq (
    "stream" TEXT,
    PRIMARY KEY ("stream")
);

-- perforce.streamrelation - Relationships between streams
CREATE TABLE IF NOT EXISTS perforce.streamrelation (
    "independentStream" TEXT,
    "dependentStream" TEXT,
    "type" TEXT,
    "parentView" TEXT,
    PRIMARY KEY ("independentStream", "dependentStream")
);

-- perforce.streamview - Precomputed stream views
CREATE TABLE IF NOT EXISTS perforce.streamview (
    "name" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "comment" TEXT,
    PRIMARY KEY ("name", "seq")
);

-- perforce.streamviewx - Indexing for precomputed stream views
CREATE TABLE IF NOT EXISTS perforce.streamviewx (
    "depotPath" TEXT,
    "viewPath" TEXT,
    "mapFlag" TEXT,
    "stream" TEXT,
    "change" TEXT,
    "pathSource" TEXT,
    "pathType" TEXT,
    "componentPrefixes" TEXT,
    "effectiveComponentType" TEXT,
    PRIMARY KEY ("depotPath", "viewPath", "mapFlag", "stream")
);

-- perforce.submodule - Submodule configuration data
CREATE TABLE IF NOT EXISTS perforce.submodule (
    "repo" TEXT,
    "path" TEXT,
    "subrepo" TEXT,
    PRIMARY KEY ("repo", "path")
);

-- perforce.svrview - View data for servers specifications
CREATE TABLE IF NOT EXISTS perforce.svrview (
    "id" TEXT,
    "type" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "viewFile" TEXT,
    PRIMARY KEY ("id", "type", "seq")
);

-- perforce.template - Streams templates
CREATE TABLE IF NOT EXISTS perforce.template (
    "name" TEXT,
    "change" INTEGER,
    "seq" INTEGER,
    "parent" TEXT,
    "type" TEXT,
    "path" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "changeMap" TEXT,
    PRIMARY KEY ("name", "change", "seq")
);

-- perforce.templatesx - Shelved stream templates
CREATE TABLE IF NOT EXISTS perforce.templatesx (
    "shelf" INTEGER,
    "name" TEXT,
    "seq" INTEGER,
    "change" INTEGER,
    "parent" TEXT,
    "type" TEXT,
    "path" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "changeMap" TEXT,
    "changeAtOpen" INTEGER,
    "user" TEXT,
    "action" TEXT,
    PRIMARY KEY ("shelf", "name", "seq")
);

-- perforce.templatewx - Pending stream templates
CREATE TABLE IF NOT EXISTS perforce.templatewx (
    "client" TEXT,
    "name" TEXT,
    "seq" INTEGER,
    "change" INTEGER,
    "parent" TEXT,
    "type" TEXT,
    "path" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "changeMap" TEXT,
    "changeAtOpen" INTEGER,
    "user" TEXT,
    "action" TEXT,
    PRIMARY KEY ("client", "name", "seq")
);

-- perforce.ticket - Second factor authentication state on a per user/host basis
CREATE TABLE IF NOT EXISTS perforce.ticket (
    "user" TEXT,
    "host" TEXT,
    "ticket" TEXT,
    "state" TEXT,
    "token" TEXT,
    "updateDate" BIGINT,
    PRIMARY KEY ("user", "host")
);

-- perforce.ticket_rp - Second factor authentication state on a per user/host basis (replica)
CREATE TABLE IF NOT EXISTS perforce.ticket_rp (
    "user" TEXT,
    "host" TEXT,
    "ticket" TEXT,
    "state" TEXT,
    "token" TEXT,
    "updateDate" BIGINT,
    PRIMARY KEY ("user", "host")
);

-- perforce.topology - Topology information
CREATE TABLE IF NOT EXISTS perforce.topology (
    "address" TEXT,
    "destAddress" TEXT,
    "serverID" TEXT,
    "date" BIGINT,
    "type" TEXT,
    "encryption" TEXT,
    "svcUser" TEXT,
    "lastSeenDate" BIGINT,
    "svrRecType" TEXT,
    "taddr" TEXT,
    "tdaddr" TEXT,
    "tid" TEXT,
    "version" TEXT,
    PRIMARY KEY ("address", "destAddress", "serverID", "date")
);

-- perforce.traits - Attributes associated with file revisions
CREATE TABLE IF NOT EXISTS perforce.traits (
    "traitLot" INTEGER,
    "name" TEXT,
    "type" TEXT,
    "value" BYTEA,
    PRIMARY KEY ("traitLot", "name")
);

-- perforce.trigger - Trigger specifications
CREATE TABLE IF NOT EXISTS perforce.trigger (
    "seq" INTEGER,
    "name" TEXT,
    "mapFlag" TEXT,
    "depotFile" TEXT,
    "triggerDepotFile" TEXT,
    "trigger" TEXT,
    "action" TEXT,
    PRIMARY KEY ("seq")
);

-- perforce.upgrades - Store server upgrade info
CREATE TABLE IF NOT EXISTS perforce.upgrades (
    "seq" INTEGER,
    "name" TEXT,
    "state" TEXT,
    "startdate" BIGINT,
    "enddate" BIGINT,
    "info" TEXT,
    PRIMARY KEY ("seq")
);

-- perforce.upgrades_rp - Store replica upgrade info
CREATE TABLE IF NOT EXISTS perforce.upgrades_rp (
    "seq" INTEGER,
    "name" TEXT,
    "state" TEXT,
    "startdate" BIGINT,
    "enddate" BIGINT,
    "info" TEXT,
    PRIMARY KEY ("seq")
);

-- perforce.user - User specifications
CREATE TABLE IF NOT EXISTS perforce.user (
    "user" TEXT,
    "email" TEXT,
    "jobView" TEXT,
    "updateDate" BIGINT,
    "accessDate" BIGINT,
    "fullName" TEXT,
    "password" TEXT,
    "strength" TEXT,
    "ticket" TEXT,
    "endDate" BIGINT,
    "type" TEXT,
    "passDate" BIGINT,
    "passExpire" BIGINT,
    "attempts" BIGINT,
    "auth" TEXT,
    PRIMARY KEY ("user")
);

-- perforce.user_rp - Used by replica server's to store login information
CREATE TABLE IF NOT EXISTS perforce.user_rp (
    "user" TEXT,
    "email" TEXT,
    "jobView" TEXT,
    "updateDate" BIGINT,
    "accessDate" BIGINT,
    "fullName" TEXT,
    "password" TEXT,
    "strength" TEXT,
    "ticket" TEXT,
    "endDate" BIGINT,
    "type" TEXT,
    "passDate" BIGINT,
    "passExpire" BIGINT,
    "attempts" BIGINT,
    "auth" TEXT,
    PRIMARY KEY ("user")
);

-- perforce.uxtext - Indexing data for P4 Code Review
CREATE TABLE IF NOT EXISTS perforce.uxtext (
    "word" TEXT,
    "attr" INTEGER,
    "value" TEXT,
    PRIMARY KEY ("word", "attr", "value")
);

-- perforce.view - View data for domain records
CREATE TABLE IF NOT EXISTS perforce.view (
    "name" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "comment" TEXT,
    PRIMARY KEY ("name", "seq")
);

-- perforce.view_rp - View data for clients of build-server replicas
CREATE TABLE IF NOT EXISTS perforce.view_rp (
    "name" TEXT,
    "seq" INTEGER,
    "mapFlag" TEXT,
    "viewFile" TEXT,
    "depotFile" TEXT,
    "comment" TEXT,
    PRIMARY KEY ("name", "seq")
);

-- perforce.working - Records for work in progress
CREATE TABLE IF NOT EXISTS perforce.working (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    "haveRev" INTEGER,
    "workRev" INTEGER,
    "isVirtual" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "modTime" BIGINT,
    "isLocked" TEXT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "tampered" TEXT,
    "clientType" TEXT,
    "movedFile" TEXT,
    "status" TEXT,
    PRIMARY KEY ("clientFile")
);

-- perforce.workingg - Working records for clients of type graph
CREATE TABLE IF NOT EXISTS perforce.workingg (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    "haveRev" INTEGER,
    "workRev" INTEGER,
    "isVirtual" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "modTime" BIGINT,
    "isLocked" TEXT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "tampered" TEXT,
    "clientType" TEXT,
    "movedFile" TEXT,
    "status" TEXT,
    "blobSha" TEXT,
    "repo" TEXT,
    PRIMARY KEY ("clientFile")
);

-- perforce.workingx - Records for shelved open files
CREATE TABLE IF NOT EXISTS perforce.workingx (
    "clientFile" TEXT,
    "depotFile" TEXT,
    "client" TEXT,
    "user" TEXT,
    "haveRev" INTEGER,
    "workRev" INTEGER,
    "isVirtual" INTEGER,
    "type" TEXT,
    "action" TEXT,
    "change" INTEGER,
    "modTime" BIGINT,
    "isLocked" TEXT,
    "digest" TEXT,
    "size" BIGINT,
    "traitLot" INTEGER,
    "tampered" TEXT,
    "clientType" TEXT,
    "movedFile" TEXT,
    "status" TEXT,
    PRIMARY KEY ("clientFile")
);

-- Specialized tables (proxy/replica/tiny)
CREATE TABLE IF NOT EXISTS perforce.pdb_lbr (
    "file" TEXT,
    "rev" TEXT,
    PRIMARY KEY ("file", "rev")
);

CREATE TABLE IF NOT EXISTS perforce.rdb_lbr (
    "file" TEXT,
    "rev" TEXT,
    PRIMARY KEY ("file", "rev")
);

CREATE TABLE IF NOT EXISTS perforce.tiny_db (
    "key" TEXT,
    "value" BYTEA,
    PRIMARY KEY ("key")
);
```

### Summary
3. **Number of tables being created**: 111 tables (including specialized ones like `pdb_lbr`, `rdb_lbr`, and `tiny_db`).

4. **Duplicate table DDL statements**: None found. All table names are unique.### Notes
- **Primary Keys**: Based on "Indexed on" fields from the documentation; composite where applicable.
- **Secondary Indexes**: Added simple indexes for common secondary fields (e.g., `change` in `db.fix`).
- **Data Types**: Mappings are conservative to preserve data integrity (e.g., TEXT for variable strings, BIGINT for timestamps/sizes).
- **Upgrades and Releases**: The schema includes upgrade notes, but no special handling is needed for Postgres (run migrations as per Perforce docs if upgrading).
- **Full Schema**: This covers all 87 tables from the PDF. If you need ALTER TABLE for indexes/constraints or data migration scripts, let me know!
