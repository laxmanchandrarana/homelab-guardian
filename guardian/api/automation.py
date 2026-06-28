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


@router.post("/run/{rule_id}")
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


@router.post("/enable/{rule_id}")
def enable_rule(rule_id: int):

    conn = get_connection()

    conn.execute(
        "UPDATE automation_rules SET enabled=1 WHERE id=?",
        (rule_id,),
    )

    conn.commit()

    conn.close()

    return {"success": True}


@router.post("/disable/{rule_id}")
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

