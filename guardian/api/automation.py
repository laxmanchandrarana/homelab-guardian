from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from guardian.automation.storage import get_connection
from guardian.automation.engine import engine

router = APIRouter(prefix="/automation", tags=["Automation"])


class RuleCreate(BaseModel):
    name: str
    trigger: str
    target: str
    action: str
    cooldown: int = 300
    retries: int = 3
    timeout: int = 60
    priority: int = 5


@router.get("/rules")
def get_rules():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM automation_rules ORDER BY priority,id"
    ).fetchall()
    conn.close()

    return [dict(r) for r in rows]


@router.post("/rules")
def create_rule(rule: RuleCreate):
    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO automation_rules
        (
            name,
            trigger,
            target,
            action,
            cooldown,
            retries,
            timeout,
            priority,
            enabled,
            created_at,
            updated_at
        )
        VALUES
        (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            rule.name,
            rule.trigger,
            rule.target,
            rule.action,
            rule.cooldown,
            rule.retries,
            rule.timeout,
            rule.priority,
            1,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()

    new_id = cur.lastrowid

    conn.close()

    return {
        "success": True,
        "id": new_id,
    }


@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule: RuleCreate):

    conn = get_connection()

    conn.execute(
        """
        UPDATE automation_rules
        SET
            name=?,
            trigger=?,
            target=?,
            action=?,
            cooldown=?,
            retries=?,
            timeout=?,
            priority=?,
            updated_at=?
        WHERE id=?
        """,
        (
            rule.name,
            rule.trigger,
            rule.target,
            rule.action,
            rule.cooldown,
            rule.retries,
            rule.timeout,
            rule.priority,
            datetime.utcnow().isoformat(),
            rule_id,
        ),
    )

    conn.commit()

    conn.close()

    return {"success": True}


@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int):

    conn = get_connection()

    conn.execute(
        "DELETE FROM automation_rules WHERE id=?",
        (rule_id,),
    )

    conn.commit()

    conn.close()

    return {"success": True}


@router.post("/rules/{rule_id}/run")
def run_rule(rule_id: int):

    conn = get_connection()

    rule = conn.execute(
        "SELECT * FROM automation_rules WHERE id=?",
        (rule_id,),
    ).fetchone()

    conn.close()

    if not rule:
        raise HTTPException(404, "Rule not found")

    result = engine.execute(rule)

    return result


@router.post("/rules/{rule_id}/enable")
def enable_rule(rule_id: int):

    conn = get_connection()

    conn.execute(
        "UPDATE automation_rules SET enabled=1 WHERE id=?",
        (rule_id,),
    )

    conn.commit()

    conn.close()

    return {"success": True}


@router.post("/rules/{rule_id}/disable")
def disable_rule(rule_id: int):

    conn = get_connection()

    conn.execute(
        "UPDATE automation_rules SET enabled=0 WHERE id=?",
        (rule_id,),
    )

    conn.commit()

    conn.close()

    return {"success": True}


@router.get("/jobs")
def jobs():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM automation_jobs
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


@router.get("/logs")
def logs():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM automation_logs
        ORDER BY id DESC
        LIMIT 500
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]

@router.get("/summary")
def automation_summary():

    conn = get_connection()

    rules = conn.execute(
        "SELECT COUNT(*) FROM automation_rules"
    ).fetchone()[0]

    enabled = conn.execute(
        "SELECT COUNT(*) FROM automation_rules WHERE enabled=1"
    ).fetchone()[0]

    jobs = conn.execute(
        "SELECT COUNT(*) FROM automation_jobs"
    ).fetchone()[0]

    failed = conn.execute(
        "SELECT COUNT(*) FROM automation_jobs WHERE status='failed'"
    ).fetchone()[0]

    conn.close()

    return {
        "total_rules": rules,
        "enabled_rules": enabled,
        "jobs": jobs,
        "failed_jobs": failed
    }

@router.get("/rules/{rule_id}")
def rule_details(rule_id:int):

    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM automation_rules WHERE id=?",
        (rule_id,)
    ).fetchone()

    conn.close()

    if not row:
        raise HTTPException(404,"Rule not found")

    return dict(row)

@router.get("/rules/{rule_id}/history")
def rule_history(rule_id:int):

    conn=get_connection()

    rows=conn.execute(
        """
        SELECT *
        FROM automation_jobs
        WHERE rule_id=?
        ORDER BY id DESC
        LIMIT 100
        """,
        (rule_id,)
    ).fetchall()

    conn.close()

    return [dict(x) for x in rows]

@router.get("/health")
def health():

    conn=get_connection()

    rules=conn.execute(
        "SELECT COUNT(*) FROM automation_rules"
    ).fetchone()[0]

    conn.close()

    return {

        "status":"healthy",

        "rules":rules,

        "engine":"running"

    }

@router.post("/rules/{rule_id}/toggle")
def toggle_rule(rule_id: int):

    conn = get_connection()

    row = conn.execute(
        "SELECT enabled FROM automation_rules WHERE id=?",
        (rule_id,)
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(404, "Rule not found")

    enabled = 0 if row["enabled"] else 1

    conn.execute(
        """
        UPDATE automation_rules
        SET enabled=?
        WHERE id=?
        """,
        (enabled, rule_id),
    )

    conn.commit()

    conn.close()

    return {
        "success": True,
        "enabled": bool(enabled),
    }

@router.delete("/rules/{rule_id}")
def delete_rule(rule_id:int):

    conn=get_connection()

    conn.execute(
        "DELETE FROM automation_rules WHERE id=?",
        (rule_id,)
    )

    conn.commit()

    conn.close()

    return {"success":True}

@router.get("/jobs/{job_id}")
def job(job_id:int):

    conn=get_connection()

    row=conn.execute(
        """
        SELECT *
        FROM automation_jobs
        WHERE id=?
        """,
        (job_id,)
    ).fetchone()

    conn.close()

    if not row:
        raise HTTPException(404,"Job not found")

    return dict(row)

@router.post("/rules/{rule_id}/run")
def run_rule(rule_id:int):

    conn=get_connection()

    conn.execute(
        """
        INSERT INTO automation_jobs
        (
            rule_id,
            service,
            status,
            progress
        )
        VALUES
        (
            ?,
            'manual',
            'running',
            0
        )
        """,
        (rule_id,)
    )

    job_id=conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    conn.commit()

    conn.close()

    return {
        "success":True,
        "job_id":job_id
    }

@router.get("/logs")
def logs():

    conn=get_connection()

    rows=conn.execute(
        """
        SELECT *
        FROM automation_logs
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    conn.close()

    return [dict(x) for x in rows]

@router.get("/jobs")
def jobs():

    conn=get_connection()

    rows=conn.execute(
        """
        SELECT *
        FROM automation_jobs
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return [dict(x) for x in rows]


